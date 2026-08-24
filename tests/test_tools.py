import pytest

from agent_core_python.tools import (
    DuplicateToolError,
    ToolNotFoundError,
    ToolRegistry,
)


def add(a: int, b: int) -> int:
    return a + b


def word_count(text: str) -> int:
    return len(text.split())


def test_register_and_list_tool() -> None:
    registry = ToolRegistry()

    registry.register("add", "Add two integers", add)

    assert registry.list_tools() == [
        {"name": "add", "description": "Add two integers"}
    ]


def test_call_add_tool() -> None:
    registry = ToolRegistry()
    registry.register("add", "Add two integers", add)

    result = registry.call("add", {"a": 2, "b": 3})

    assert result == 5


def test_call_word_count_tool() -> None:
    registry = ToolRegistry()
    registry.register("word_count", "Count words", word_count)

    result = registry.call("word_count", {"text": "hello agent world"})

    assert result == 3


def test_unknown_tool_raises_error() -> None:
    registry = ToolRegistry()

    with pytest.raises(ToolNotFoundError):
        registry.call("missing", {})


def test_duplicate_tool_raises_error() -> None:
    registry = ToolRegistry()
    registry.register("add", "Add two integers", add)

    with pytest.raises(DuplicateToolError):
        registry.register("add", "Another add tool", add)