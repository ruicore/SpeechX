class Error(RuntimeError):
    status_code: int = 500
    code: str = ''

    def __init__(self, message: str, code: str = 'ERROR'):
        super().__init__(message)
        self.code = self.code or code


class LLMError(Error):
    code: str = 'LLM_ERROR'
    status_code: int = 502


class BadRequestError(Error):
    code: str = 'BAD_REQUEST'
    status_code: int = 400


class ConfigError(Error):
    code: str = 'CONFIG_ERROR'
    status_code: int = 500
