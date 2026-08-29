from collections.abc import Callable
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict


@dataclass(frozen=True, slots=True)
class RegisteredTool:
    name: str
    description: str
    function: Callable[..., object]
    arguments_model: type[BaseModel]


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    arguments: dict[str, object]


class ToolResult(BaseModel):
    tool_name: str
    output: object
