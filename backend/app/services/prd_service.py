from __future__ import annotations

import json
import logging
from typing import Any

from app.clients.claude_client import ClaudeClient
from app.prompts.prd_generation import PRD_GENERATION_SYSTEM, build_prd_prompt
from app.schemas.idea import IdeaCard
from app.schemas.prd import PRDContent

logger = logging.getLogger(__name__)


class PRDService:
    def __init__(self, claude: ClaudeClient, supabase: Any):
        self.claude = claude
        self.db = supabase

    def generate_prd(self, idea_id: str, idea_card: IdeaCard) -> PRDContent:
        """Generate a PRD from an IdeaCard using Claude structured output."""
        user_prompt = build_prd_prompt(idea_card.model_dump_json(indent=2))

        prd, tokens = self.claude.generate_structured(
            system_prompt=PRD_GENERATION_SYSTEM,
            user_prompt=user_prompt,
            output_model=PRDContent,
            max_tokens=4096,
        )

        # Store PRD in Supabase
        self.db.table("prds").upsert(
            {
                "idea_id": idea_id,
                "content": json.loads(prd.model_dump_json()),
                "tokens_used": tokens,
            },
            on_conflict="idea_id",
        ).execute()

        logger.info("PRD generated for idea %s (%d tokens)", idea_id, tokens)
        return prd

    def get_prd(self, idea_id: str) -> PRDContent | None:
        """Retrieve a stored PRD for an idea."""
        result = (
            self.db.table("prds")
            .select("content")
            .eq("idea_id", idea_id)
            .single()
            .execute()
        )
        if result.data:
            return PRDContent.model_validate(result.data["content"])
        return None
