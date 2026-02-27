import json
import logging
from typing import TypeVar

import anthropic
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class ClaudeClient:
    """Wrapper around the Anthropic SDK for structured and text generation."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        output_model: type[T],
        max_tokens: int = 4096,
    ) -> tuple[T, int]:
        """Generate structured output matching a Pydantic model.

        Uses Claude's tool_use to guarantee valid JSON output.
        Returns (parsed_model, total_tokens).
        """
        tool_name = "output"
        tool_schema = output_model.model_json_schema()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            tools=[
                {
                    "name": tool_name,
                    "description": f"Output structured data as {output_model.__name__}",
                    "input_schema": tool_schema,
                }
            ],
            tool_choice={"type": "tool", "name": tool_name},
        )

        total_tokens = response.usage.input_tokens + response.usage.output_tokens

        for block in response.content:
            if block.type == "tool_use" and block.name == tool_name:
                parsed = output_model.model_validate(block.input)
                logger.info(
                    "Claude structured output: model=%s tokens=%d",
                    output_model.__name__,
                    total_tokens,
                )
                return parsed, total_tokens

        raise ValueError(
            f"Claude did not return a tool_use block for {tool_name}. "
            f"Response: {json.dumps([b.model_dump() for b in response.content], indent=2)}"
        )

    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> tuple[str, int]:
        """Generate free-form text (e.g. markdown PRD).

        Returns (text, total_tokens).
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        total_tokens = response.usage.input_tokens + response.usage.output_tokens
        text = response.content[0].text

        logger.info("Claude text output: %d chars, %d tokens", len(text), total_tokens)
        return text, total_tokens
