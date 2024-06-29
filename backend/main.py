from uuid import uuid4

from fastapi import FastAPI, Depends, Request, Response
from starlette.responses import RedirectResponse, JSONResponse

from gateway.api_router import (
    call_api_gateway,
    RedirectAuthServiceException,
    RedirectStorageServiceException,
    RedirectNotificationServiceException,
    RedirectPaymentServiceException,
)
from authentication import authentication_main
from storage import storage_main
from notification import notification_main
from payment import payment_main
from controller import main
from loguru import logger

app = FastAPI()
app.include_router(main.router, dependencies=[Depends(call_api_gateway)])

app.mount("/auth", authentication_main.auth_app)
app.mount("/storage", storage_main.storage_app)
app.mount("/notification", notification_main.notification_app)
app.mount("/payment", payment_main.payment_app)

logger.add(
    "info.log",
    format="Log: [{extra[log_id]}: {time} - {level} - {message} ",
    level="INFO",
    enqueue=True,
)


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        logger.info("Request to access " + request.url.path)
        try:
            response = await call_next(request)
        except Exception:
            logger.error("Request to " + request.url.path + " failed: {ex}")
            response = JSONResponse(content={"success": False}, status_code=500)
        finally:
            logger.info("Successfully accessed " + request.url.path)
            return response


@app.exception_handler(RedirectAuthServiceException)
def exception_handler_auth(
    request: Request, exc: RedirectAuthServiceException
) -> Response:
    return RedirectResponse(url="http://localhost:8000/auth/hello")


@app.exception_handler(RedirectStorageServiceException)
def exception_handler_storage(
    request: Request, exc: RedirectStorageServiceException
) -> Response:
    return RedirectResponse(url="http://localhost:8000/storage/hello")


@app.exception_handler(RedirectNotificationServiceException)
def exception_handler_notification(
    request: Request, exc: RedirectNotificationServiceException
) -> Response:
    return RedirectResponse(url="http://localhost:8000/notification/hello")


@app.exception_handler(RedirectPaymentServiceException)
def exception_handler_payment(
    request: Request, exc: RedirectPaymentServiceException
) -> Response:
    return RedirectResponse(url="http://localhost:8000/payment/hello")


@app.get("/hello")
async def say_hello():
    return {"message": "Hello main"}
