import uuid
from pydantic import Field
from enum import StrEnum
from common.base_model import BaseModel


class UserModel(BaseModel):
    user_id: str
    user_name: str
    user_plan: int | None = 0
    user_email: str

class UserIdResponse(BaseModel):
    user_id: str

