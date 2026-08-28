from collections.abc import Callable

from pydantic import BaseModel, ValidationError

from .models import RegisteredTool


class ToolNotFoundError(Exception):
    """Raised when a requested tool is not registered."""


class DuplicateToolError(Exception):
    """Raised when a tool name is registered twice."""


class ToolArgumentsError(ValueError):
    pass


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable[..., object],
        arguments_model: type[BaseModel],
    ) -> None:
        if name in self._tools:
            raise DuplicateToolError(f"Tool is already registered: {name}")

        if not callable(function):
            raise TypeError(f"Tool function is not callable: {name}")

        self._tools[name] = RegisteredTool(
            name=name,
            description=description,
            function=function,
            arguments_model=arguments_model,
        )

    def call(
        self,
        name: str,
        arguments: dict[str, object],
    ) -> object:
        if name not in self._tools:
            raise ToolNotFoundError(f"Tool is not registered: {name}")
        registered_tool = self._tools[name]
        try:
            validated_arguments = registered_tool.arguments_model.model_validate(
                arguments
            )
        except ValidationError as error:
            raise ToolArgumentsError(f"Invalid arguments for tool: {name}") from error
        return registered_tool.function(**validated_arguments.model_dump())

    def list_tools(self) -> list[dict[str, object]]:
        return [
            {
                "name": registered_tool.name,
                "description": registered_tool.description,
                "input_schema": registered_tool.arguments_model.model_json_schema(),
            }
            for registered_tool in self._tools.values()
        ]
