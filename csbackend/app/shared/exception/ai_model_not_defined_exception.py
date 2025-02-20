from .cs_exception import CSException

class AIModelNotDefinedException(CSException):
    error_message = "Code Sphere not defined this AI model. Please use another model."
    def __init__(self, message = error_message):
        super().__init__(message)