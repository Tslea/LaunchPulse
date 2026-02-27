from __future__ import annotations

import logging
from typing import Any

from app.schemas.lead import LeadCreate, LeadResponse

logger = logging.getLogger(__name__)


class LeadService:
    def __init__(self, supabase: Any):
        self.db = supabase

    def save_lead(self, lead: LeadCreate) -> LeadResponse:
        """Save a lead captured from a landing page."""
        result = (
            self.db.table("leads")
            .insert(lead.model_dump())
            .execute()
        )
        row = result.data[0]
        logger.info("Lead captured: idea=%s email=%s variant=%s", lead.idea_id, lead.email, lead.variant)
        return LeadResponse(**row)

    def get_leads(self, idea_id: str) -> list[LeadResponse]:
        """Get all leads for an idea."""
        result = (
            self.db.table("leads")
            .select("*")
            .eq("idea_id", idea_id)
            .order("created_at", desc=True)
            .execute()
        )
        return [LeadResponse(**row) for row in result.data]

    def count_leads(self, idea_id: str) -> int:
        """Count total leads for an idea."""
        result = (
            self.db.table("leads")
            .select("id", count="exact")
            .eq("idea_id", idea_id)
            .execute()
        )
        return result.count or 0
