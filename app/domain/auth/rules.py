class AuthError(Exception):
    pass

class InvalidTokenError(AuthError):
    pass
