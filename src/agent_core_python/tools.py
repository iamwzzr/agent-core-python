from collections.abc import Callable


class ToolNotFoundError(Exception):
    """Raised when a requested tool is not registered."""


class DuplicateToolError(Exception):
    """Raised when a tool name is registered twice."""


class ToolRegistry:
    def __init__(self) -> None:
        #创建用于保存工具的空字典
        self._tools : dict[
            str,
            tuple[str,Callable[...,object]]
        ] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable[..., object],
    ) -> None:
        # TODO 1：检查name是否已经存在
        # TODO 2：如果存在，抛出DuplicateToolError
        # TODO 3：否则保存description和function
        if name in self._tools:
            raise DuplicateToolError(
                f"Tool is already registered: {name}"
            )
        self._tools[name] = (description , function)

    def call(
        self,
        name: str,
        arguments: dict[str, object],
    ) -> object:
        # TODO 1：检查name是否存在
        # TODO 2：如果不存在，抛出ToolNotFoundError
        # TODO 3：取出对应函数
        # TODO 4：通过function(**arguments)调用并返回结果
        if name not in self._tools:
            raise ToolNotFoundError(
                f"Tool is not registered: {name}"
            )
        _,function = self._tools[name]
        return function(**arguments)


    def list_tools(self) -> list[dict[str, str]]:
        # TODO：遍历所有工具，只返回name和description
        # 不要返回function对象
         return [
            {
                "name": name,
                "description": description,
            }
            for name, (description, _) in self._tools.items()
        ]