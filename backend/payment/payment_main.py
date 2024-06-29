from fastapi import FastAPI, Depends, HTTPException, Request, Header, BackgroundTasks
from typing import Annotated

from starlette.middleware.cors import CORSMiddleware

from common.dependencies import verify_token
from common.models import UrlResponseModel, UpgradePlanArgs
from common.origins import origins
from payment.repository import PaymentRepository
from payment.models import PaymentModel, PaymentSuccessModel
from payment.exceptions import PaymentDataBaseError, StripePaymentError
from payment.payment_services.stripe import create_checkout_session
import stripe
from starlette.responses import RedirectResponse
import datetime
from requests import patch


payment_app = FastAPI()
payment_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def upgrade_plan_in_storage(upgrade_plan_name, user_id):
    response = patch(f'http://localhost:8000/storage/upgrade_plan?user_id={user_id}', json={"upgrade_plan_name": upgrade_plan_name})
    if response.status_code == 200:
        print("Żądanie zostało pomyślnie wysłane.")
    else:
        print("Wystąpił problem podczas wysyłania żądania. Kod statusu:", response.status_code)

@payment_app.get("/payment_success")
async def payment_success(user_id: str, upgrade_plan_name: str, background_tasks: BackgroundTasks) -> RedirectResponse:
    try:
        payment_repo = PaymentRepository()
        user_payments = payment_repo.get_payments(user_id=user_id, status="pending")
        stripe_events = stripe.Event.list(limit=10, type="checkout.session.completed", created={"gt": datetime.datetime.now(tz=None)-datetime.timedelta(seconds=15)})
        for event in stripe_events:
            checkout_id = event['data']['object'].get('id')
            if checkout_id in [u.payment_id for u in user_payments]:
                payment_repo.update_payment_status(payment_id=checkout_id, new_status="completed")
    except PaymentDataBaseError as e:
        raise HTTPException(status_code=500, detail=f'Payment database returned an error: {str(e)}')
    
    background_tasks.add_task(upgrade_plan_in_storage, upgrade_plan_name, user_id)

    return RedirectResponse("http://localhost:3000")

@payment_app.get("/payment_cancel")
async def payment_cancel(user_id: str):
    # TODO: UDERZYĆ DO NOTIFICATION --> @notification_app.get("/upgrade_plan_fail")
    return{"Payment cancelled"}


@payment_app.post("/create_payment")
async def create_payment(data: UpgradePlanArgs, info: Annotated[str, Depends(verify_token)]) -> RedirectResponse:
    payment_repo = PaymentRepository()
    price_id = payment_repo.get_stripe_product(data.upgrade_plan_name)
    try:
        checkout_session = create_checkout_session(price_id=price_id, user_id=info['sub'], upgrade_plan_name=data.upgrade_plan_name)
    except StripePaymentError:
        raise HTTPException(status_code=500, detail="Could not create new payment in Stripe.")
    
    payment = PaymentModel(
        payment_id=checkout_session.id,
        user_id=info["sub"],
        status="pending",
    )
    
    try:
        payment_repo.insert_payment(payment)
    except PaymentDataBaseError:
        raise HTTPException(status_code=400, detail="Could not register a new payment in database.")
    print(f"Link to payment: {checkout_session.url}")
    return {
        "payment_url": checkout_session.url
    }
