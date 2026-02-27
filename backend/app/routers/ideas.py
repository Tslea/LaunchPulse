from fastapi import APIRouter, Depends

from app.clients.claude_client import ClaudeClient
from app.dependencies import get_claude_client, get_supabase
from app.prompts.idea_intake import IDEA_STRUCTURING_SYSTEM, build_idea_structuring_prompt
from app.schemas.idea import IdeaCard, IdeaCreate, IdeaResponse
from app.services.idea_service import IdeaService

router = APIRouter()


@router.post("/ideas", response_model=IdeaResponse)
def create_idea(
    body: IdeaCreate,
    claude: ClaudeClient = Depends(get_claude_client),
    supabase=Depends(get_supabase),
):
    """Create a new idea. Structures the raw input via Claude, then stores it."""
    user_prompt = build_idea_structuring_prompt(body)
    idea_card, _tokens = claude.generate_structured(
        system_prompt=IDEA_STRUCTURING_SYSTEM,
        user_prompt=user_prompt,
        output_model=IdeaCard,
    )

    service = IdeaService(supabase)
    return service.create_idea(idea_card)


@router.get("/ideas", response_model=list[IdeaResponse])
def list_ideas(supabase=Depends(get_supabase)):
    service = IdeaService(supabase)
    return service.list_ideas()


@router.get("/ideas/{idea_id}", response_model=IdeaResponse)
def get_idea(idea_id: str, supabase=Depends(get_supabase)):
    service = IdeaService(supabase)
    return service.get_idea(idea_id)
