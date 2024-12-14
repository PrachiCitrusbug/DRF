
from rest_framework.exceptions import APIException



class ObjExistException(Exception):
    """
    Exception that should be raised if model object already exists
    """

    pass


class SerializerException(APIException):
    """
    Exception class to raise serializer
    """
    status_code = 500
    default_detail = 'A server error occurred. We are looking into it!'
    default_code = 'error'

class OTPExpireException(Exception):
    """
    Exception that should be raised if OTP has expired
    """
    pass


# @dataclass(frozen=True)
# class AppointmentException(Exception):
#     item: str
#     message: str

#     def __str__(self):
#         return "{}: {}".format(self.item, self.message)

# @dataclass(frozen=True)
# class FutureDateException(Exception):
#     """
#     Exception that should be raised if future dates are not accepted
#     """
#     def __str__(self):
#         return "This field doesn't accept future dates"

# @dataclass(frozen=True)
# class PastDateException(Exception):
#     """
#     Exception that should be raised if past dates are not accepted
#     """
#     def __str__(self):
#         return "This field doesn't accept past dates"
