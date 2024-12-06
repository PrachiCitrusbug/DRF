from dataclasses import dataclass

@dataclass(frozen=True)
class ObjExistException(Exception):
    """
    Exception that should be raised if model object already exists
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