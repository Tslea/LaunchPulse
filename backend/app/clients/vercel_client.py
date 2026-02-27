import logging

import httpx

logger = logging.getLogger(__name__)

VERCEL_API_BASE = "https://api.vercel.com"


class VercelClient:
    """Client for Vercel REST API — deploys single-file landing pages."""

    def __init__(self, token: str, team_id: str = ""):
        self.token = token
        self.team_id = team_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _params(self) -> dict:
        if self.team_id:
            return {"teamId": self.team_id}
        return {}

    async def create_deployment(
        self,
        project_name: str,
        html_content: str,
        slug: str,
    ) -> dict:
        """Deploy an inline HTML file to Vercel.

        Uses Vercel's v13/deployments API with inline files.
        Returns deployment data including the live URL.
        """
        payload = {
            "name": project_name,
            "files": [
                {
                    "file": "index.html",
                    "data": html_content,
                }
            ],
            "projectSettings": {
                "framework": None,
            },
            "target": "production",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{VERCEL_API_BASE}/v13/deployments",
                headers=self.headers,
                params=self._params(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        url = data.get("url", "")
        if url and not url.startswith("https://"):
            url = f"https://{url}"

        logger.info("Vercel deployment created: %s (slug=%s)", url, slug)
        return {
            "id": data.get("id", ""),
            "url": url,
            "ready_state": data.get("readyState", ""),
        }

    async def get_deployment(self, deployment_id: str) -> dict:
        """Check deployment status."""
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                f"{VERCEL_API_BASE}/v13/deployments/{deployment_id}",
                headers=self.headers,
                params=self._params(),
            )
            response.raise_for_status()
            return response.json()
