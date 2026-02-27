from functools import lru_cache

from app.clients.claude_client import ClaudeClient
from app.clients.supabase_client import get_supabase_client
from app.clients.vercel_client import VercelClient
from app.config import settings


@lru_cache
def get_claude_client() -> ClaudeClient:
    return ClaudeClient(
        api_key=settings.anthropic_api_key,
        model=settings.claude_model,
    )


def get_supabase():
    return get_supabase_client(
        url=settings.supabase_url,
        key=settings.supabase_key,
    )


@lru_cache
def get_vercel_client() -> VercelClient:
    return VercelClient(
        token=settings.vercel_token,
        team_id=settings.vercel_team_id,
    )
