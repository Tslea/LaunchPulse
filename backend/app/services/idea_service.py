from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from app.schemas.idea import IdeaCard, IdeaResponse, IdeaStatus

logger = logging.getLogger(__name__)


class IdeaService:
    def __init__(self, supabase: Any):
        self.db = supabase

    def create_idea(self, idea_card: IdeaCard) -> IdeaResponse:
        """Store a structured IdeaCard in Supabase and return the full record."""
        result = (
            self.db.table("ideas")
            .insert({"idea_card": idea_card.model_dump(), "status": IdeaStatus.DRAFT})
            .execute()
        )
        row = result.data[0]
        return IdeaResponse(
            id=row["id"],
            idea_card=IdeaCard.model_validate(row["idea_card"]),
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def get_idea(self, idea_id: str) -> IdeaResponse:
        result = self.db.table("ideas").select("*").eq("id", idea_id).single().execute()
        row = result.data
        return IdeaResponse(
            id=row["id"],
            idea_card=IdeaCard.model_validate(row["idea_card"]),
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def list_ideas(self) -> list[IdeaResponse]:
        result = (
            self.db.table("ideas").select("*").order("created_at", desc=True).execute()
        )
        return [
            IdeaResponse(
                id=row["id"],
                idea_card=IdeaCard.model_validate(row["idea_card"]),
                status=row["status"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in result.data
        ]

    def update_status(self, idea_id: str, status: IdeaStatus) -> None:
        self.db.table("ideas").update({"status": status}).eq("id", idea_id).execute()
        logger.info("Idea %s status updated to %s", idea_id, status)
