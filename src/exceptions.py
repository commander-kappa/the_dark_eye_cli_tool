class ApplicationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class AttributeError(ApplicationError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

