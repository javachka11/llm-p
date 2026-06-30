class BaseAppError(Exception):
    """
    Базовая ошибка приложения.
    """

    def __init__(self, message: str = 'Неизвестная ошибка в приложении.'):
        self.message = message
        super().__init__(self.message)


class ConflictError(BaseAppError):
    """
    Ошибка конфликта (например, email уже существует).
    """

    def __init__(self, message: str = 'Ошибка конфликта.'):
        super().__init__(message)


class UnauthorizedError(BaseAppError):
    """
    Ошибка авторизации (например, неверный пароль).
    """

    def __init__(self, message: str = 'Ошибка авторизации.'):
        super().__init__(message)


class ForbiddenError(BaseAppError):
    """
    Ошибка запрета (например, нет прав).
    """

    def __init__(self, message: str = 'Ошибка запрета.'):
        super().__init__(message)


class NotFoundError(BaseAppError):
    """
    Ошибка отсутствия объекта (например, объект в базе отсутствует).
    """
    
    def __init__(self, message: str = 'Ошибка отсутствия объекта.'):
        super().__init__(message)


class ExternalServiceError(BaseAppError):
    """
    Ошибка внешнего сервиса (например, OpenRouter вернул ошибку). 
    """

    def __init__(self, message: str = 'Ошибка внешнего сервиса.'):
        super().__init__(message)
