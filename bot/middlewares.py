import logging

logger = logging.getLogger(__name__)


async def log_request(app, handler):
    async def middleware_handler(request):
        logger.info(f"Получен запрос: {request.method} {request.path}")
        logger.info(f"Заголовки: {request.headers}")

        try:
            body = await request.text()
            logger.info(f"Тело запроса: {body}")
        except Exception as e:
            logger.error(f"Не удалось получить тело запроса: {e}")

        return await handler(request)
    return middleware_handler
