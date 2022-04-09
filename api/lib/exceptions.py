from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper


class FieldValidationError(RequestValidationError):
    def __init__(self, field, message):
        super().__init__(
            errors=[ErrorWrapper(exc=Exception(message), loc=('body', field))]
        )
