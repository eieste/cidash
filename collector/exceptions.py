class InvalidVersion(ValueError):
    pass


class ValidationError(ValueError):
    pass


class UnautorizedAccess(PermissionError):
    pass
