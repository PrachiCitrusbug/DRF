from rest_framework.response import Response

class CustomResponse(Response):
    """customized data response"""
    def __init__(self, message=None, data=None, status=None, headers=None,
                 exception=False, content_type=None):
        self.message = message
        custom_data = {"message": self.message, "data": data, "status": status}
        super().__init__(data=custom_data, status=status, headers=headers,
                 exception=exception, content_type=content_type)
