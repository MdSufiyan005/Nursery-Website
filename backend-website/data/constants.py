from enum import Enum

class PaymentStatus(str, Enum):
    SUCCESS = 'Success'
    FAILURE = 'Failure'
    PENDING = 'Pending'