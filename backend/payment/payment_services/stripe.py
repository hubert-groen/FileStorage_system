import stripe
from payment.exceptions import StripePaymentError

# test api key
stripe.api_key = "sk_test_51PATYu089JUuVWC5gd49xLoAkxyGGVYgPevTFjOYpRCaTodm7Fr12sfLvpQXHWzkxcxHvjB8fsRa0UAy7jsgJ9BV00AFn9GUfL"


def create_checkout_session(price_id: str, user_id: str, upgrade_plan_name: str) -> stripe.checkout.Session:
    try:
        return stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'http://localhost:8000/payment/payment_success?user_id={user_id}&upgrade_plan_name={upgrade_plan_name}',
            cancel_url=f'http://localhost:8000/payment/payment_cancel?user_id={user_id}',
        )
    except stripe.error.StripeError as e:
        raise StripePaymentError(str(e)) from None
