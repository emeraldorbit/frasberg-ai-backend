"""Sofia SDK Exceptions"""

class SofiaException(Exception):
    """Base exception for Sofia SDK"""
    pass

class APIError(SofiaException):
    """API request failed"""
    pass

class ValidationError(SofiaException):
    """Validation error"""
    pass
