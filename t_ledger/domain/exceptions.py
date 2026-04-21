class BaseError(Exception):
    """Базовое исключение приложения"""


class ApiClientError(BaseError):
    """Исключения, связанные с запросами во внешние API"""


class ApiClientRequestError(ApiClientError):
    """Возникает, когда код статуса ответа не равен: 200 OK"""
