import uuid

from sqlalchemy import create_engine, select, insert, update, delete, func, asc
from sqlalchemy.exc import IntegrityError, DatabaseError

from storage.models import UserModel, FileModel, FileRenameModel, AccessFileModel
from storage.database_definition import UserTable, FileTable, PlanTable, FileAccess
from storage.exceptions import UserAlreadyExists, UserDoesNotExist, FileDoesNotExist, StorageLimitExceeded, CannotGetPlan, CannotUpgradePlan, FileAlreadyExists, FileSaveError, CannotShareFile


storage_plans = [["basic", 10, 0], ["silver", 50, 50], ["gold", 100, 100], ["unlimited", float('inf'), 200]]


class StorageRepository():
    ENGINE = create_engine("sqlite:///storage/storage.db")

    def __init__(self) -> None:
        self._connection = self.ENGINE.connect()


    def insert_user(self, user: UserModel) -> str:
        stmt = (
            insert(UserTable).values(user.model_dump())
        )
        try:
            self._connection.execute(stmt)
            self._connection.commit()
        except IntegrityError:
            raise UserAlreadyExists()
        finally:
            self._connection.close()
        return user.user_id


    def get_user(self, user_id: str) -> UserModel:
        stmt = (
            select(UserTable).where(UserTable.c.user_id == user_id)
        )
        try:
            user = self._connection.execute(stmt).fetchone()
        except IntegrityError:
            raise UserDoesNotExist()
        finally:
            self._connection.close()
        return UserModel.model_validate(user)


    def insert_file(self, file: FileModel) -> uuid.UUID:
        user_query = select(
            UserTable.c.user_plan,
            PlanTable.c.limit,
            PlanTable.c.name
        ).where(
            UserTable.c.user_id == file.user_id
        ).join(
            PlanTable,
            UserTable.c.user_plan==PlanTable.c.level
        )
        user_result = self._connection.execute(user_query).first()
        if user_result is None:
            raise UserDoesNotExist("The user does not exist")
        

        total_files_size_query = select(func.sum(FileTable.c.file_size)).where(FileTable.c.user_id == file.user_id)
        total_files_size_result = self._connection.execute(total_files_size_query).scalar() or 0
        new_total_size = total_files_size_result + file.file_size

        user_plan_name = user_result.name
        user_plan_limit = user_result.limit
        required_space = new_total_size - user_plan_limit
        if new_total_size > user_plan_limit:
            raise StorageLimitExceeded(
                "Adding this file would exceed the user's storage limit",
                current_plan_name=user_plan_name,
                required_space=required_space,
                new_total_size=new_total_size
            )
        insert_stmt = (
            insert(FileTable).values(file.model_dump() | {"file_id": str(file.file_id)})
        )
        try:
            self._connection.execute(insert_stmt)
            self._connection.commit()
        except DatabaseError:
            self._connection.rollback()
            raise FileSaveError() from None
        finally:
            self._connection.close()

        return file.file_id


    def get_files(self, user_id: str) -> list[FileModel]:
        user_stmt = select(UserTable).where(UserTable.c.user_id == user_id)
        user_result = self._connection.execute(user_stmt).first()
        if user_result is None:
            raise UserDoesNotExist()

        stmt = (
            select(FileTable).where(FileTable.c.user_id == user_id)
        )
        files = self._connection.execute(stmt).fetchall()
        self._connection.close()
        return [FileModel.model_validate(file) for file in files]

    
    def get_shared_files(self, user_id: str) -> list[FileModel]:
        user_stmt = select(FileAccess).where(FileAccess.c.user_id == user_id)
        user_result = self._connection.execute(user_stmt).first()
        if user_result is None:
            raise UserDoesNotExist()
        
        stmt = (
            select(FileTable)
            .select_from(
                FileTable.join(FileAccess, FileTable.c.file_id == FileAccess.c.file_id)
            )
            .where(FileAccess.c.user_id == user_id)
        )
        files = self._connection.execute(stmt).fetchall()
        self._connection.close()
        return [FileModel.model_validate(file) for file in files]


    def get_file_by_id(self, user_id: str, file_id: str) -> FileModel:
        user_stmt = select(UserTable).where(UserTable.c.user_id == user_id)
        user_result = self._connection.execute(user_stmt).first()

        if user_result is None:
            raise UserDoesNotExist()
        stmt = (
            select(FileTable)
            .where(FileTable.c.file_id == file_id)
        )
        try:
            file = self._connection.execute(stmt).fetchone()
        except IntegrityError:
            raise FileDoesNotExist()
        finally:
            self._connection.close()
        self._connection.close()
        return FileModel.model_validate(file)


    def rename_file(self, file_id: uuid.UUID, new_file: FileRenameModel) -> uuid.UUID:
        update_dict = new_file.model_dump(exclude_none=True)
        if not update_dict:
            return file_id

        stmt = (
            update(
                FileTable
            ).where(
                FileTable.c.file_id == str(file_id)
            ).values(
                update_dict
            )
        )

        result = self._connection.execute(stmt)
        self._connection.commit()
        if result.rowcount == 0:
            raise FileDoesNotExist()
        self._connection.close()
        return file_id
    

    def delete_file(self, file_id: uuid.UUID) -> uuid.UUID:
        stmt = (
            delete(FileTable).where(FileTable.c.file_id == str(file_id))
        )
        result = self._connection.execute(stmt)
        self._connection.commit()
        if result.rowcount == 0:
            raise FileDoesNotExist()
        self._connection.close()
        return file_id
    

    def get_required_plan(self, storage_total) -> str:
        stmt = select(
            PlanTable.c.name
        ).where(
            PlanTable.c.limit >= storage_total
        ).order_by(
            asc(PlanTable.c.limit)
        ).limit(1)
        try:
            result = self._connection.execute(stmt).fetchone()
        except IntegrityError:
            raise CannotGetPlan()
        return result.name
    

    def upgrade_plan(self, user_id: str, upgrade_plan_name: str):
        stmt = select(PlanTable.c.level).where(PlanTable.c.name == upgrade_plan_name)
        try:
            upgrade_plan_level = self._connection.execute(stmt).fetchone().level
        except IntegrityError:
            raise CannotGetPlan()

        stmt = (
            update(
                UserTable
            ).where(
                UserTable.c.user_id == user_id
            ).values(
                user_plan=upgrade_plan_level
            )
        )

        try:
            self._connection.execute(stmt)
            self._connection.commit()
        except IntegrityError:
            self._connection.rollback()
            raise CannotUpgradePlan()
        finally:
            self._connection.close()
        return upgrade_plan_name


    def share_file(self, share_input: AccessFileModel):
        stmt = (
            insert(FileAccess).values(share_input.model_dump() | {"file_access_id": str(share_input.file_access_id)})
        )
        try:
            self._connection.execute(stmt)
            self._connection.commit()
        except IntegrityError:
            raise CannotShareFile()
        finally:
            self._connection.close()
        return share_input.user_id


    def unshare_file(self, unshare_input: AccessFileModel):
        stmt = (
            delete(FileAccess).where(
                (FileAccess.c.user_id == str(unshare_input.user_id)) &
                (FileAccess.c.file_id == str(unshare_input.file_id))
            )
        )
        result = self._connection.execute(stmt)
        self._connection.commit()
        if result.rowcount == 0:
            raise CannotShareFile()
        self._connection.close()
        return unshare_input.user_id
    