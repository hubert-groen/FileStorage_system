import uuid

from sqlalchemy import create_engine, select, insert, update, delete, func, asc
from sqlalchemy.exc import IntegrityError

from authentication.models import UserModel
from authentication.database_definition import UserTable
from authentication.exceptions import UserAlreadyExists, UserDoesNotExist

class AuthenticationRepository():
    ENGINE = create_engine("sqlite:///authentication/authentication.db")

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


    def get_user(self, user_id: str) -> str:
        stmt = (
            select(UserTable).where(UserTable.c.user_id == user_id)
        )
        try:
            user = self._connection.execute(stmt).fetchone()
            if user is None:
                raise UserDoesNotExist()
        except IntegrityError:
            raise UserDoesNotExist()
        self._connection.close()
        return user
    

    def get_user_id(self, user_email: str) -> str:
        stmt = select(UserTable.c.user_id).where(UserTable.c.user_email == user_email)
        try:
            result = self._connection.execute(stmt).fetchone()
            if result is None:
                raise UserDoesNotExist()
        except IntegrityError:
            raise UserDoesNotExist()
        finally:
            self._connection.close()
        
        return result[0]