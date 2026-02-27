from fastapi import APIRouter, Depends, HTTPException

from app.clients.claude_client import ClaudeClient
from app.clients.vercel_client import VercelClient
from app.dependencies import get_claude_client, get_supabase, get_vercel_client
from app.schemas.pipeline import PipelineRunRequest, PipelineRunResponse
from app.services.idea_service import IdeaService
from app.services.prd_service import PRDService

router = APIRouter()


@router.post("/pipeline/run", response_model=PipelineRunResponse)
async def run_pipeline(
    body: PipelineRunRequest,
    claude: ClaudeClient = Depends(get_claude_client),
    vercel: VercelClient = Depends(get_vercel_client),
    supabase=Depends(get_supabase),
):
    """Run the full validation pipeline: idea → PRD → landing → deploy.

    This is synchronous in Phase 1 (~30-60 seconds).
    Phase 2 will move this to an async Celery task.
    """
    from app.services.pipeline_service import PipelineService

    pipeline = PipelineService(claude, supabase, vercel)
    return await pipeline.run(body.idea, body.config)


@router.post("/ideas/{idea_id}/generate-prd")
def generate_prd(
    idea_id: str,
    claude: ClaudeClient = Depends(get_claude_client),
    supabase=Depends(get_supabase),
):
    """Generate a PRD for an existing idea."""
    idea_service = IdeaService(supabase)
    idea = idea_service.get_idea(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    prd_service = PRDService(claude, supabase)
    prd = prd_service.generate_prd(idea_id, idea.idea_card)
    return prd.model_dump()
