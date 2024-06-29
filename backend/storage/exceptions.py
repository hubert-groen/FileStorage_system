class UserAlreadyExists(Exception):
    ...


class UserDoesNotExist(Exception):
    ...


class FileAlreadyExists(Exception):
    ...


class FileDoesNotExist(Exception):
    ...


class FileSaveError(Exception):
    ...


class StorageLimitExceeded(Exception):
    """Exception raised when the storage limit is exceeded."""
    def __init__(self, message, current_plan_name, required_space, new_total_size):
        self.message = message
        self.current_plan_name = current_plan_name
        self.required_space = required_space
        self.new_total_size = new_total_size
        super().__init__(message)


class CannotGetPlan(Exception):
    ...


class CannotUpgradePlan(Exception):
    ...


class CannotShareFile(Exception):
    ...