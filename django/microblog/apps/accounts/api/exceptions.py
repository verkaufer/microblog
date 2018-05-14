from rest_framework import status
from rest_framework.exceptions import APIException


class LoginFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Login attempt failed."
    default_code = 'authentication_failed'