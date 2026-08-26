from collections.abc import Callable
from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True, slots=True)
class RegisteredTool:
    name: str
    description: str
    function: Callable[..., object]
    arguments_model: type[BaseModel]
