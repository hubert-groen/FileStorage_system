import uuid
import sys
from datetime import datetime
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from requests import post
from starlette.middleware.cors import CORSMiddleware

from authentication.authentication_main import origins
from common.dependencies import verify_token
from storage.models import UserIdResponse, UserModel, FileModel, FileIdModel, FileInsertModel, FileRenameModel, UpgradePlan, AccessFileModel
from storage.repository import StorageRepository
from storage.file_manager import FileManager
from storage.exceptions import UserAlreadyExists, UserDoesNotExist, FileDoesNotExist, StorageLimitExceeded, CannotGetPlan, CannotUpgradePlan, FileSaveError, CannotShareFile
from common.models import UrlResponseModel, UpgradePlanArgs

storage_app = FastAPI()

storage_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@storage_app.get("/hello")
async def root():
    return {"message": "hello storage"}


def add_user_in_notification(user_id, user_name):
    response = post(f'http://localhost:8000/notification/test_user', json={"user_id": user_id, "user_name": user_name})
    if response.status_code == 200:
        print("Żądanie zostało pomyślnie wysłane.")
    else:
        print("Wystąpił problem podczas wysyłania żądania. Kod statusu:", response.status_code)

@storage_app.post("/user")
async def add_user(token: Annotated[str, Depends(verify_token)], background_tasks: BackgroundTasks) -> UserIdResponse:
    storage_repo = StorageRepository()
    user = UserModel(user_id=token["sub"], user_name=token["given_name"])
    try:
        user_id = storage_repo.insert_user(user)
    except UserAlreadyExists:
        existing_user_name = token["given_name"]
        raise HTTPException(status_code=400, detail=f"User {existing_user_name} already exists!")
    
    background_tasks.add_task(add_user_in_notification, user.user_id, user.user_name)

    return UserIdResponse(user_id=user_id)


def add_file_in_notification(file_id, file_name):
    response = post(f'http://localhost:8000/notification/test_file', json={"file_id": file_id, "file_name": file_name})
    if response.status_code == 200:
        print("Żądanie zostało pomyślnie wysłane.")
    else:
        print("Wystąpił problem podczas wysyłania żądania. Kod statusu:", response.status_code)

@storage_app.post("/files")
async def add_file(file_input: UploadFile, token: Annotated[str, Depends(verify_token)], background_tasks: BackgroundTasks) -> FileIdModel:
    storage_repo = StorageRepository()
    file_manager = FileManager(user_id=token["sub"])
    contents = await file_input.read()
    contents_mb_size = sys.getsizeof(contents)/1024 ** 2
    file = FileModel(
                    user_id=token["sub"],
                    file_name=file_input.filename,
                    file_size=contents_mb_size)
    limit_exceeded = False
    try:
        file_id = storage_repo.insert_file(file)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    except StorageLimitExceeded as e:
        limit_exceeded = True
        requested_total_storage = e.new_total_size
        current_plan_name = e.current_plan_name
        required_space = e.required_space
    except FileSaveError:
        raise HTTPException(status_code=500, detail="An unexpected error ocurred when trying to save the file")

    if not limit_exceeded:
        file_manager.insert_file(file_id, contents)
        return FileIdModel(file_id=file_id)

    try:
        upgrade_plan_name = storage_repo.get_required_plan(requested_total_storage)
    except CannotGetPlan:
        raise HTTPException(status_code=500, detail="Cannot get user's current plan!")

    upgrade_details = UpgradePlan(current_plan_name=current_plan_name, upgrade_plan_name=upgrade_plan_name)
    detail_message = (
        f"Storage limit exceded. Currently your plan is {current_plan_name}. You lack {required_space} Mb."
    )
    detail_data = UrlResponseModel(url='http://localhost:8000/notification/upgrade_plan', data=upgrade_details.model_dump())

    background_tasks.add_task(add_file_in_notification, file_id, file_input.filename)

    raise HTTPException(status_code=413, detail={"message": detail_message, "data": detail_data.model_dump()})


@storage_app.get("/files")
async def get_files_for_user(info: Annotated[str, Depends(verify_token)]) -> list[FileModel]:
    storage_repo = StorageRepository()
    user_id = info['sub']
    try:
        files = storage_repo.get_files(user_id=user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    return files


@storage_app.get("/shared_files")
async def get_shared_files_for_user(info: Annotated[str, Depends(verify_token)]) -> list[FileModel]:
    storage_repo = StorageRepository()
    user_id = info['sub']
    try:
        files = storage_repo.get_shared_files(user_id=user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User has no shared files.")
    return files


@storage_app.get("/file/{file_id}")
async def get_file_by_id(file_id: str, token: Annotated[str, Depends(verify_token)]) -> FileResponse:
    storage_repo = StorageRepository()
    user_id = token["sub"]
    file_manager = FileManager(user_id)
    try:
        file = storage_repo.get_file_by_id(user_id=user_id, file_id=file_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    filename = file.file_name
    filepath = file_manager.get_path_to_file(file_id=file.file_id)
    return FileResponse(filename=filename, path=filepath)


@storage_app.patch("/files")
async def rename_file(file_id: uuid.UUID, file_rename: FileRenameModel, token: Annotated[str, Depends(verify_token)]) -> FileIdModel:
    storage_repo = StorageRepository()
    try:
        updated_file_id = storage_repo.rename_file(file_id=file_id, new_file=file_rename)
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    return FileIdModel(file_id=updated_file_id)


@storage_app.delete("/files")
async def delete_file(file_id: uuid.UUID, token: Annotated[str, Depends(verify_token)]) -> FileIdModel:
    storage_repo = StorageRepository()
    file_manager = FileManager(user_id=token["sub"])
    try:
        deleted_file_id = storage_repo.delete_file(file_id=file_id)
        file_manager.delete_file(file_id=file_id)
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    return FileIdModel(file_id=deleted_file_id)


@storage_app.patch("/upgrade_plan")
async def upgrade_plan(data: UpgradePlanArgs, user_id: str):
    storage_repo = StorageRepository()
    try:
        storage_repo.upgrade_plan(user_id=user_id, upgrade_plan_name=data.upgrade_plan_name)
    except CannotGetPlan:
        raise HTTPException(status_code=400, detail="Cannot access PlanTable!")
    except CannotUpgradePlan:
        raise HTTPException(status_code=400, detail="Cannot upgrade user's plan!")
    return {"message": f"Plan of user {user_id} was upgraded to {data.upgrade_plan_name} in storage DB."}


def sharing_notification(timestamp, user_id, owner_user_id, file_id, status):
    response = post(f'http://localhost:8000/notification/sharing_notification', json={"timestamp": timestamp, "user_id": user_id, "owner_user_id": owner_user_id, "file_id": file_id, "status": status})
    if response.status_code == 200:
        print("Żądanie zostało pomyślnie wysłane.")
    else:
        print("Wystąpił problem podczas wysyłania żądania. Kod statusu:", response.status_code)

@storage_app.post("/shared_files")
async def share_file(share_input: AccessFileModel, background_tasks: BackgroundTasks):
    storage_repo = StorageRepository()
    try:
        storage_repo.share_file(share_input=share_input)
    except CannotShareFile:
        raise HTTPException(status_code=400, detail="Cannot share file!")
    
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    # background_tasks.add_task(sharing_notification, timestamp, share_input.user_id, share_input.owner_user_id, share_input.file_id, status=0)

    return {"message": f"File {share_input.file_id} was shared to {share_input.user_id}."}


@storage_app.delete("/shared_files")
async def unshare_file(unshare_input: AccessFileModel):
    storage_repo = StorageRepository()
    try:
        storage_repo.unshare_file(unshare_input=unshare_input)
    except CannotShareFile:
        raise HTTPException(status_code=400, detail="Cannot unshare file!")
    return {"message": f"File {unshare_input.file_id} was unshared to {unshare_input.user_id}."}



# below requests are for ease of testing only

@storage_app.post("/test_user")
async def add_user(user_id: str, user_name: str) -> UserIdResponse:
    storage_repo = StorageRepository()
    user = UserModel(user_id=user_id, user_name=user_name)
    try:
        user_id = storage_repo.insert_user(user)
    except UserAlreadyExists:
        existing_user_name = user_name
        raise HTTPException(status_code=400, detail=f"User {existing_user_name} already exists!")
    return UserIdResponse(user_id=user_id)


@storage_app.post("/test_files")
async def add_test_file(file_input: UploadFile, user_id: str) -> FileIdModel:
    storage_repo = StorageRepository()
    file_manager = FileManager(user_id=user_id)
    contents = await file_input.read()
    contents_mb_size = sys.getsizeof(contents)/1024 ** 2
    file = FileModel(
                    user_id=user_id,
                    file_name=file_input.filename,
                    file_size=contents_mb_size)
    limit_exceeded = False
    try:
        file_id = storage_repo.insert_file(file)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    except StorageLimitExceeded as e:
        limit_exceeded = True
        requested_total_storage = e.new_total_size
        current_plan_name = e.current_plan_name
        required_space = e.required_space
    except FileSaveError:
        raise HTTPException(status_code=500, detail="An unexpected error ocurred when trying to save the file")

    if not limit_exceeded:
        file_manager.insert_file(file_id, contents)
        return FileIdModel(file_id=file_id)

    try:
        upgrade_plan_name = storage_repo.get_required_plan(requested_total_storage)
    except CannotGetPlan:
        raise HTTPException(status_code=500, detail="Cannot get user's current plan!")

    upgrade_details = UpgradePlan(current_plan_name=current_plan_name, upgrade_plan_name=upgrade_plan_name)
    detail_message = (
        f"Storage limit exceded. Currently your plan is {current_plan_name}. You lack {required_space} Mb."
    )
    detail_data = UrlResponseModel(url='http://localhost:8000/notification/upgrade_plan', data=upgrade_details.model_dump())

    raise HTTPException(status_code=413, detail={"message": detail_message, "data": detail_data.model_dump()})
