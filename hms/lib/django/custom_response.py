from http.client import responses

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

import hms.settings as settings

class CustomResponse:
    """customized data response"""

    def __init__(
        self,
        message = None,
        data=None,
        status=None,
    ):
        self.message = str(message) if settings.DEBUG else None
        self.data = data
        self.status = status

    @property
    def status_text(self):
        """
        Returns reason text corresponding to our HTTP response status code.
        Provided for convenience.
        """
        return responses.get(int(self.status), "")

    def success_message(self):
        self.status = self.status if self.status else HTTP_200_OK
        self.data = {
            "message": self.message if self.message else "success",
            "data": self.data if self.data else "{}",
            "status": self.status_text,
        }
        return Response(self.data)

    def error_message(self):
        self.status = self.status if self.status else HTTP_400_BAD_REQUEST
        self.data = {
            "message": self.message if self.message else "Something went wrong!",
            "data": self.data if self.data else "{}",
            "status": self.status_text,
        }
        return Response(self.data)
