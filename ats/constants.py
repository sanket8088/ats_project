# enums.py (create a new Python file)
from enum import Enum

class ErrorMessages(Enum):
    CANDIDATE_NOT_FOUND_ERROR = "Candidate not found."
    OPERATION_REQUIRED_ERROR = "Operation parameter is required."
    INVALID_OPERATION_ERROR = "Invalid operation. Allowed values are 'shortlist' and 'reject'."
    QUERY_PARAMS_NOT_FOUND = "Query parameter 'q' is required."
