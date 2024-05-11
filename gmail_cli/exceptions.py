class CredentialsFileNotFound(Exception):
    '''
    Raised when the credentials file is not found.
    '''
    pass


class ValidationError(Exception):
    '''
    Raised when validation fails.
    '''
    pass
