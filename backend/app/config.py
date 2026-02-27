from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Anthropic (Claude API)
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-5-20250514"

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # Vercel
    vercel_token: str = ""
    vercel_team_id: str = ""

    # TikTok (Phase 2)
    tiktok_pixel_id: str = ""
    tiktok_access_token: str = ""
    tiktok_advertiser_id: str = ""

    # App
    environment: str = "development"
    api_base_url: str = "http://localhost:8000"
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
