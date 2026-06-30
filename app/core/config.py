from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Загрузка параметров из файла .env в окружение приложения.

    Атрибуты класса:\\
    app_name - название приложения;\\
    env - окружение приложения;\\
    jwt_secret - секретный ключ для подписи JWT-токена;\\
    jwt_alg - алгоритм шифрования JWT;\\
    access_token_expire_minutes - время жизни JWT-токена (в минутах);\\
    sqlite_path - путь к файлу базы данных SQLite;\\
    openrouter_api_key - API-ключ для доступа к OpenRouter;\\
    openrouter_base_url - базовый URL для OpenRouter;\\
    openrouter_model - используемая LLM-модель в OpenRouter;\\
    openrouter_site_url - HTTP Referer для запросов к OpenRouter;\\
    openrouter_app_name - название приложения для OpenRouter.
    """

    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      case_sensitive=False,
                                      extra='ignore')
    
    app_name: str = 'llm-p'
    env: str = 'local'
    
    jwt_secret: str = 'change_me_super_secret'
    jwt_alg: str = 'HS256'
    access_token_expire_minutes: int = 60
    
    sqlite_path: str = 'app.db'
    
    openrouter_api_key: str
    openrouter_base_url: str = 'https://openrouter.ai/api/v1'
    openrouter_model: str = 'openrouter/free'
    openrouter_site_url: str = 'https://example.com'
    openrouter_app_name: str = 'llm-fastapi-openrouter'


settings = Settings() # type: ignore
