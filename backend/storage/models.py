import uuid
from pydantic import Field
from enum import StrEnum
from common.base_model import BaseModel
from common.models import UpgradePlanArgs


class PlanEnum(StrEnum):
    basic = "basic"
    silver = "silver"
    gold = "gold"
    unlimited = "unlimited"


class UserModel(BaseModel):
    user_id: str
    user_name: str
    user_plan: int | None = 0


class FileModel(BaseModel):
    file_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    file_name: str
    file_size: float


class FileInsertModel(BaseModel):
    file_name: str
    file_size: float


class UserIdResponse(BaseModel):
    user_id: str


class FileIdModel(BaseModel):
    file_id: uuid.UUID


class FileRenameModel(BaseModel):
    file_name: str | None = None


class UpgradePlan(UpgradePlanArgs):
    current_plan_name: str


class AccessFileModel(BaseModel):
    file_access_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    owner_user_id: str
    file_id: str
    
    