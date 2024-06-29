
from sqlalchemy import create_engine, select, insert, update
from sqlalchemy.exc import IntegrityError
from notification.models import UserModel, FileModel, SharingFile
from notification.database_definition import UserTable, FileTable, NotificationTable
from notification.exceptions import UserAlreadyExists, UserDoesNotExist, FileAlreadyExists, FileDoesNotExist


class NotificationRepository():
    ENGINE = create_engine("sqlite:///notification/notification.db")

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
    
    def add_file(self, file: FileModel) -> str:
        stmt = (
            insert(FileTable).values(file.model_dump())
        )
        try:
            self._connection.execute(stmt)
            self._connection.commit()
        except IntegrityError:
            raise FileAlreadyExists()
        finally:
            self._connection.close()
        return file.file_id

    def get_file(self, file_id: str) -> FileModel:
        stmt = (
            select(FileTable).where(FileTable.c.file_id == file_id)
        )
        try:
            file = self._connection.execute(stmt).fetchone()
        except IntegrityError:
            raise FileDoesNotExist()
        finally:
            self._connection.close()
        return FileModel.model_validate(file)

    def add_notification(self, data: SharingFile) -> str:
        stmt = (
            insert(NotificationTable).values(data.model_dump())
        )
        try:
            self._connection.execute(stmt)
            self._connection.commit()
        except IntegrityError:
            raise Exception
        finally:
            self._connection.close()
        return data.file_id
    
    def update_notification_status(self, file_id: str) -> str:
        stmt = (
            update(NotificationTable)
            .where(NotificationTable.c.file_id == file_id)
            .values(status=1)
        )
        try:
            self._connection.execute(stmt)
            self._connection.commit()
        except IntegrityError:
            raise Exception
        finally:
            self._connection.close()
        return file_id
    
    def get_unread_notification(self, user_id: str) -> list[SharingFile]:
        stmt = (
            select(NotificationTable)
            .where(NotificationTable.c.user_id == user_id)
            .where(NotificationTable.c.status == 0)
        )
        try:
            notifications = self._connection.execute(stmt).fetchall()
        except IntegrityError:
            raise FileDoesNotExist()
        finally:
            self._connection.close()
        return [SharingFile.model_validate(notification) for notification in notifications]
