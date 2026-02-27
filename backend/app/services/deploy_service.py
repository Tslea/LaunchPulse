from __future__ import annotations

import logging
import re
from typing import Any

from app.clients.vercel_client import VercelClient

logger = logging.getLogger(__name__)


def _slugify(name: str) -> str:
    """Convert an idea name to a URL-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug[:50].strip("-")


class DeployService:
    def __init__(self, vercel: VercelClient | None, supabase: Any):
        self.vercel = vercel
        self.db = supabase

    async def deploy_landing(
        self,
        idea_id: str,
        idea_name: str,
        html_content: str,
        landing_page_id: str | None = None,
        variant: str = "A",
    ) -> dict:
        """Deploy a rendered landing page to Vercel and record the deployment."""
        slug = _slugify(idea_name)
        project_name = f"lp-{slug}"

        deployment = await self.vercel.create_deployment(
            project_name=project_name,
            html_content=html_content,
            slug=slug,
        )

        # Store deployment record
        result = (
            self.db.table("deployments")
            .insert(
                {
                    "idea_id": idea_id,
                    "landing_page_id": landing_page_id,
                    "url": deployment["url"],
                    "vercel_deployment_id": deployment["id"],
                    "variant": variant,
                }
            )
            .execute()
        )

        row = result.data[0]
        logger.info("Deployed: idea=%s url=%s variant=%s", idea_id, deployment["url"], variant)
        return {
            "id": row["id"],
            "url": deployment["url"],
            "vercel_deployment_id": deployment["id"],
            "variant": variant,
        }

    def get_deployments(self, idea_id: str) -> list[dict]:
        """Get all deployments for an idea."""
        result = (
            self.db.table("deployments")
            .select("*")
            .eq("idea_id", idea_id)
            .order("created_at", desc=True)
            .execute()
        )
        return result.data
