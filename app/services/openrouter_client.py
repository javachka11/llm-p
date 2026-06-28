import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self):
        self._api_key = settings.openrouter_api_key
        self._base_url = settings.openrouter_base_url
        self._model = settings.openrouter_model
        self._site_url = settings.openrouter_site_url
        self._app_name = settings.openrouter_app_name

    async def chat_completion(self, messages: list[dict],
                              temperature: float = 0.7) -> str:
        headers = {'Authorization': f'Bearer {self._api_key}',
                   'HTTP-Referer': self._site_url,
                   'X-Title': self._app_name,
                   'Content-Type': 'application/json'}
        
        payload = {'model': self._model,
                   'messages': messages,
                   'temperature': temperature}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f'{self._base_url}/chat/completions',
                                             json=payload,
                                             headers=headers,
                                             timeout=30.0)
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']['content']
            except httpx.HTTPStatusError as e:
                raise ExternalServiceError(f'OpenRouter вернул ошибку \
                                           {e.response.status_code}: \
                                           {e.response.text}')
            except (httpx.RequestError, KeyError, IndexError) as e:
                raise ExternalServiceError(f'Ошибка при выполнении запроса \
                                           к OpenRouter: {str(e)}')
