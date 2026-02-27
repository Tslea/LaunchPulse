from __future__ import annotations

import json
import logging
from typing import Any

from app.clients.claude_client import ClaudeClient
from app.prompts.landing_content import (
    LANDING_CONTENT_SYSTEM,
    build_landing_content_prompt,
)
from app.schemas.landing import LandingPageContent
from app.schemas.prd import PRDContent
from app.templates.engine import render_template

logger = logging.getLogger(__name__)


class LandingService:
    def __init__(self, claude: ClaudeClient | None, supabase: Any):
        self.claude = claude
        self.db = supabase

    def generate_content(self, idea_id: str, prd: PRDContent) -> LandingPageContent:
        """Generate landing page content from a PRD using Claude structured output."""
        user_prompt = build_landing_content_prompt(prd.model_dump_json(indent=2))

        content, tokens = self.claude.generate_structured(
            system_prompt=LANDING_CONTENT_SYSTEM,
            user_prompt=user_prompt,
            output_model=LandingPageContent,
            max_tokens=4096,
        )

        logger.info(
            "Landing content generated for idea %s (%d tokens)", idea_id, tokens
        )
        return content

    def render_html(
        self,
        content: LandingPageContent,
        idea_id: str,
        api_base_url: str,
        tiktok_pixel_id: str = "",
    ) -> str:
        """Render the landing page template with generated content."""
        values = content.model_dump()
        config = {
            "idea_id": idea_id,
            "api_base_url": api_base_url,
            "tiktok_pixel_id": tiktok_pixel_id,
        }
        return render_template("landing_v1.html", values, config)

    def save_landing_page(
        self,
        idea_id: str,
        content: LandingPageContent,
        html: str,
        variant: str = "A",
    ) -> dict:
        """Store landing page content and rendered HTML in Supabase."""
        result = (
            self.db.table("landing_pages")
            .upsert(
                {
                    "idea_id": idea_id,
                    "content": json.loads(content.model_dump_json()),
                    "html": html,
                    "variant": variant,
                },
                on_conflict="idea_id,variant",
            )
            .execute()
        )
        row = result.data[0]
        logger.info("Landing page saved: idea=%s variant=%s", idea_id, variant)
        return row

    def get_landing_page(self, idea_id: str, variant: str = "A") -> dict | None:
        """Retrieve a stored landing page."""
        result = (
            self.db.table("landing_pages")
            .select("*")
            .eq("idea_id", idea_id)
            .eq("variant", variant)
            .single()
            .execute()
        )
        return result.data
