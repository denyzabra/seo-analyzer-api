import time
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware to log request processing time"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, get_response):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        logger.info(
            f"{request.method} {request.path} - "
            f"Status: { response.status_code} - "
            f"Duration: {duration:.sf}s" 
        )

        return response