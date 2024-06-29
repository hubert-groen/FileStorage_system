import uuid
from pathlib import Path, PurePath
import os
from storage.exceptions import FileDoesNotExist

STORAGE_FOLDER = 'storage_fs'


class FileManager():
    """ Basic file system tree responsible for storing user data:

            |storage_fs
                .
                .
                .
                |user's folder, name: <some_user_id>
                    |user's file, name: <some_file_id>
                    .
                    .
                    .
    """
    def __init__(self, user_id: uuid.UUID) -> None:
        self.user_data_path = PurePath(
                                        os.path.dirname(__file__),
                                        STORAGE_FOLDER,
                                        str(user_id))

    def insert_file(self, file_id: uuid.UUID, data) -> bool:
        file_path = Path(self.user_data_path, str(file_id))
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, 'wb+') as user_file:
                user_file.write(data)
        except IOError:
            return False
        return True

    def retrive_file(self, file_id: uuid.UUID):
        file_path = Path(self.user_data_path, str(file_id))
        if file_path.exists():
            return file_path.read_bytes()
        else:
            raise FileDoesNotExist

    def get_path_to_file(self, file_id: uuid.UUID):
        file_path = Path(self.user_data_path, str(file_id))
        if file_path.exists():
            return file_path
        else:
            raise FileDoesNotExist

    def delete_file(self, file_id: uuid.UUID) -> None:
        path = self.get_path_to_file(file_id)
        os.remove(path)
