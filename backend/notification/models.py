from common.base_model import BaseModel
from common.models import UpgradePlanArgs


class UserModel(BaseModel):
    user_id: str
    user_name: str

class UserIdResponse(BaseModel):
    user_id: str

class UpgradePlan(UpgradePlanArgs):
    current_plan_name: str

class SharingFile(BaseModel):
    timestamp: str
    user_id: str
    owner_user_id: str
    file_id: str
    status: bool

class FileModel(BaseModel):
    file_id: str
    file_name: str