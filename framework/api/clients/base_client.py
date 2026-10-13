"""Base HTTP client: one place for the base URL, the timeout and request logging."""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class BaseApiClient:
    """Wraps httpx.Client; subclasses add one method per API endpoint."""

    def __init__(self, base_url: str, timeout: float) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)
        # __init__ constructor, when object is created from class and it initializes the attributes
        # self link to the object for method to work on it

    def _request(
        self, method: str, path: str, log_body: bool = True, **kwargs: Any
    ) -> httpx.Response:
        # **kwargs pass all the rest as is. (json=.., headers=.., params=.., etc)
        """Send a request, log it, and return the response unchanged (tests do the asserts)."""
        response = self._client.request(method, path, **kwargs)
        logger.info(
            "%s %s -> %s (%.2fs)",  # log's pattern
            method,
            response.request.url,
            response.status_code,
            response.elapsed.total_seconds(),
        )
        if log_body:  # Log the body only if it doesn't contain secrets (like a password or token)
            logger.debug("Response body: %s", response.text)
        else:
            logger.debug("Response body not logged: it may contain secrets")
        return response

    def close(self) -> None:  # close connection
        """Release the network connection; call it when the client is no longer needed."""
        self._client.close()
