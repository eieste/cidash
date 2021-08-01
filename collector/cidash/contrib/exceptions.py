class InvalidVersion(ValueError):
    pass

class ValidationError(ValueError):
    pass

class UnauthorizedAccess(PermissionError):
    pass
