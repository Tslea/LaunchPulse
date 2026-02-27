"""Supabase client with lazy import to avoid import-time failures in test environments."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

_client: Any = None


def get_supabase_client(url: str, key: str) -> Any:
    """Get or create a Supabase client singleton.

    Uses lazy import of the supabase SDK to avoid import-time errors
    when the cryptography module is unavailable (e.g. in CI/test environments).
    """
    global _client
    if _client is None:
        if not url or not key:
            logger.warning("Supabase credentials not configured — client will be unavailable")
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        from supabase import create_client

        _client = create_client(url, key)
        logger.info("Supabase client initialized for %s", url)
    return _client
