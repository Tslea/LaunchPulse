from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse

from app.clients.claude_client import ClaudeClient
from app.config import settings
from app.dependencies import get_claude_client, get_supabase
from app.schemas.landing import LandingPageContent
from app.services.idea_service import IdeaService
from app.services.landing_service import LandingService
from app.services.prd_service import PRDService

router = APIRouter()


@router.post("/ideas/{idea_id}/landing-page")
def generate_landing_page(
    idea_id: str,
    claude: ClaudeClient = Depends(get_claude_client),
    supabase=Depends(get_supabase),
):
    """Generate a landing page for an idea. Requires PRD to exist."""
    prd_service = PRDService(claude, supabase)
    prd = prd_service.get_prd(idea_id)
    if not prd:
        raise HTTPException(status_code=400, detail="PRD not found. Generate PRD first.")

    landing_service = LandingService(claude, supabase)
    content = landing_service.generate_content(idea_id, prd)
    html = landing_service.render_html(
        content,
        idea_id=idea_id,
        api_base_url=settings.api_base_url,
        tiktok_pixel_id=settings.tiktok_pixel_id,
    )
    row = landing_service.save_landing_page(idea_id, content, html)

    return {
        "id": row["id"],
        "idea_id": idea_id,
        "variant": row["variant"],
        "content": content.model_dump(),
    }


@router.get("/ideas/{idea_id}/landing-page/preview", response_class=HTMLResponse)
def preview_landing_page(
    idea_id: str,
    variant: str = "A",
    supabase=Depends(get_supabase),
):
    """Preview the rendered landing page HTML."""
    landing_service = LandingService(claude=None, supabase=supabase)
    page = landing_service.get_landing_page(idea_id, variant)
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found.")
    return HTMLResponse(content=page["html"])
