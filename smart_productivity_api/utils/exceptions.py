"""Uniform JSON error envelope for the entire API."""
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    NotAuthenticated, AuthenticationFailed, PermissionDenied,
    NotFound, ValidationError,
)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        message = "Invalid or missing credentials."
        code = "unauthorized"
    elif isinstance(exc, PermissionDenied):
        message = "You do not have permission to perform this action."
        code = "forbidden"
    elif isinstance(exc, NotFound):
        message = "Requested resource was not found."
        code = "not_found"
    elif isinstance(exc, ValidationError):
        message = "Validation failed."
        code = "validation_error"
    else:
        message = "An error occurred."
        code = "error"

    response.data = {
        "success": False,
        "code": code,
        "message": message,
        "errors": response.data,
        "status_code": response.status_code,
    }
    return response
