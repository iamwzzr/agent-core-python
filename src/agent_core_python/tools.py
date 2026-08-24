from collections.abc import Callable


class ToolNotFoundError(Exception):
    """Raised when a requested tool is not registered."""


class DuplicateToolError(Exception):
    """Raised when a tool name is registered twice."""


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[str, Callable[..., object]]] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable[..., object],
    ) -> None:
        if name in self._tools:
            raise DuplicateToolError(f"Tool is already registered: {name}")
        self._tools[name] = (description, function)

    def call(
        self,
        name: str,
        arguments: dict[str, object],
    ) -> object:
        if name not in self._tools:
            raise ToolNotFoundError(f"Tool is not registered: {name}")
        _, function = self._tools[name]
        return function(**arguments)

    def list_tools(self) -> list[dict[str, str]]:
        return [
            {
                "name": name,
                "description": description,
            }
            for name, (description, _) in self._tools.items()
        ]
