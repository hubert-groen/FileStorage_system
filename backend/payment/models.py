from enum import StrEnum
from common.base_model import BaseModel
from common.models import UrlResponseModel


class StatusEnum(StrEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class PaymentModel(BaseModel):
    payment_id: str
    user_id: str
    status: StatusEnum


class PaymentSuccessModel(BaseModel):
    notification_url: UrlResponseModel
    storage_url: UrlResponseModel
