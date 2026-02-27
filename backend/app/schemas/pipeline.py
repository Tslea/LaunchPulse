from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.idea import IdeaCreate


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class PipelineStep(BaseModel):
    name: str
    status: StepStatus = StepStatus.PENDING
    detail: str = ""


class PipelineConfig(BaseModel):
    """User-configurable options for a pipeline run."""

    daily_budget_eur: float = Field(default=7.0, ge=1.0, le=100.0)
    test_duration_days: int = Field(default=5, ge=1, le=30)
    target_geo: str = Field(default="IT", description="ISO country code")
    deploy_to_vercel: bool = Field(default=True)


class PipelineRunRequest(BaseModel):
    idea: IdeaCreate
    config: PipelineConfig = Field(default_factory=PipelineConfig)


class PipelineRunResponse(BaseModel):
    idea_id: str
    steps: list[PipelineStep]
    landing_page_url: str = ""
    prd_generated: bool = False
    landing_generated: bool = False
    deployed: bool = False
