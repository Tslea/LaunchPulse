from __future__ import annotations

import logging
from typing import Any

from app.clients.claude_client import ClaudeClient
from app.clients.vercel_client import VercelClient
from app.config import settings
from app.prompts.idea_intake import IDEA_STRUCTURING_SYSTEM, build_idea_structuring_prompt
from app.schemas.idea import IdeaCard, IdeaCreate, IdeaStatus
from app.schemas.pipeline import (
    PipelineConfig,
    PipelineRunResponse,
    PipelineStep,
    StepStatus,
)
from app.services.deploy_service import DeployService
from app.services.idea_service import IdeaService
from app.services.landing_service import LandingService
from app.services.prd_service import PRDService

logger = logging.getLogger(__name__)


class PipelineService:
    """Orchestrates the full validation pipeline synchronously (Phase 1).

    Steps:
    1. Structure idea (Claude) → IdeaCard
    2. Generate PRD (Claude) → PRDContent
    3. Generate landing content (Claude) → LandingPageContent
    4. Render HTML template
    5. Deploy to Vercel
    """

    def __init__(
        self,
        claude: ClaudeClient,
        supabase: Any,
        vercel: VercelClient,
    ):
        self.claude = claude
        self.db = supabase
        self.vercel = vercel

    async def run(
        self, idea_input: IdeaCreate, config: PipelineConfig
    ) -> PipelineRunResponse:
        steps = [
            PipelineStep(name="structure_idea"),
            PipelineStep(name="generate_prd"),
            PipelineStep(name="generate_landing"),
            PipelineStep(name="render_html"),
            PipelineStep(name="deploy"),
        ]

        response = PipelineRunResponse(idea_id="", steps=steps)

        # Step 1: Structure idea
        steps[0].status = StepStatus.RUNNING
        try:
            user_prompt = build_idea_structuring_prompt(idea_input)
            idea_card, _ = self.claude.generate_structured(
                system_prompt=IDEA_STRUCTURING_SYSTEM,
                user_prompt=user_prompt,
                output_model=IdeaCard,
            )

            idea_service = IdeaService(self.db)
            idea = idea_service.create_idea(idea_card)
            idea_service.update_status(idea.id, IdeaStatus.GENERATING)
            response.idea_id = idea.id
            steps[0].status = StepStatus.COMPLETED
            steps[0].detail = f"Idea: {idea_card.name}"
        except Exception as e:
            steps[0].status = StepStatus.FAILED
            steps[0].detail = str(e)
            logger.exception("Pipeline failed at structure_idea")
            return response

        # Step 2: Generate PRD
        steps[1].status = StepStatus.RUNNING
        try:
            prd_service = PRDService(self.claude, self.db)
            prd = prd_service.generate_prd(idea.id, idea_card)
            response.prd_generated = True
            steps[1].status = StepStatus.COMPLETED
        except Exception as e:
            steps[1].status = StepStatus.FAILED
            steps[1].detail = str(e)
            logger.exception("Pipeline failed at generate_prd")
            return response

        # Step 3: Generate landing content
        steps[2].status = StepStatus.RUNNING
        try:
            landing_service = LandingService(self.claude, self.db)
            content = landing_service.generate_content(idea.id, prd)
            steps[2].status = StepStatus.COMPLETED
        except Exception as e:
            steps[2].status = StepStatus.FAILED
            steps[2].detail = str(e)
            logger.exception("Pipeline failed at generate_landing")
            return response

        # Step 4: Render HTML
        steps[3].status = StepStatus.RUNNING
        try:
            html = landing_service.render_html(
                content,
                idea_id=idea.id,
                api_base_url=settings.api_base_url,
                tiktok_pixel_id=settings.tiktok_pixel_id,
            )
            landing_service.save_landing_page(idea.id, content, html)
            response.landing_generated = True
            steps[3].status = StepStatus.COMPLETED
        except Exception as e:
            steps[3].status = StepStatus.FAILED
            steps[3].detail = str(e)
            logger.exception("Pipeline failed at render_html")
            return response

        # Step 5: Deploy to Vercel
        if config.deploy_to_vercel:
            steps[4].status = StepStatus.RUNNING
            try:
                deploy_service = DeployService(self.vercel, self.db)
                deployment = await deploy_service.deploy_landing(
                    idea_id=idea.id,
                    idea_name=idea_card.name,
                    html_content=html,
                )
                response.landing_page_url = deployment["url"]
                response.deployed = True
                idea_service.update_status(idea.id, IdeaStatus.LIVE)
                steps[4].status = StepStatus.COMPLETED
                steps[4].detail = deployment["url"]
            except Exception as e:
                steps[4].status = StepStatus.FAILED
                steps[4].detail = str(e)
                logger.exception("Pipeline failed at deploy")
        else:
            steps[4].status = StepStatus.COMPLETED
            steps[4].detail = "Skipped (deploy_to_vercel=false)"

        return response
