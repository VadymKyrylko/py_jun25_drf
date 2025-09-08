from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        exc = DRFValidationError(detail=exc.messages)

    return exception_handler(exc, context)
