from enum import Enum


class Status(str, Enum):
    NOTPDF = 'not_pdf'
    SUCCESS = 'success'
    NOT200CODE = 'not_200_code'
    HTTPERROR = 'http_error'
    NOTOPENACCESS = 'not_open_access'
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ERROR = 'error'
