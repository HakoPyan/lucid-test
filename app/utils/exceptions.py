class AlreadyExistsError(Exception):
    def __init__(self, message: str, constraint_name: str):
        super().__init__(message)
        self.constraint_name = constraint_name


class UnauthorizedError(Exception):
    def __init__(self):
        super().__init__('Invalid credentials.')
