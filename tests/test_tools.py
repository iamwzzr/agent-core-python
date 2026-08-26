from collections.abc import Callable
from typing import cast

import pytest
from pydantic import BaseModel, ConfigDict

from agent_core_python.tools import (
    DuplicateToolError,
    ToolArgumentsError,
    ToolNotFoundError,
    ToolRegistry,
)


class AddArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    a: int
    b: int


class WordCountArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str


def add(a: int, b: int) -> int:
    return a + b


def word_count(text: str) -> int:
    return len(text.split())


def test_register_and_list_tool() -> None:
    registry = ToolRegistry()

    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )

    assert registry.list_tools() == [
        {
            "name": "add",
            "description": "Add two integers",
            "input_schema": AddArguments.model_json_schema(),
        }
    ]


def test_call_add_tool() -> None:
    registry = ToolRegistry()
    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )

    result = registry.call("add", {"a": 2, "b": 3})

    assert result == 5


def test_call_validates_and_converts_arguments() -> None:
    registry = ToolRegistry()
    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )

    result = registry.call("add", {"a": "2", "b": 3})

    assert result == 5


def test_call_word_count_tool() -> None:
    registry = ToolRegistry()
    registry.register(
        "word_count",
        "Count words",
        word_count,
        WordCountArguments,
    )

    result = registry.call("word_count", {"text": "hello agent world"})

    assert result == 3


def test_unknown_tool_raises_error() -> None:
    registry = ToolRegistry()

    with pytest.raises(ToolNotFoundError):
        registry.call("missing", {})


def test_duplicate_tool_raises_error() -> None:
    registry = ToolRegistry()
    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )

    with pytest.raises(DuplicateToolError):
        registry.register(
            "add",
            "Another add tool",
            add,
            AddArguments,
        )


def test_invalid_tool_arguments_raise_error() -> None:
    registry = ToolRegistry()
    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )

    with pytest.raises(ToolArgumentsError):
        registry.call(
            "add",
            {"a": "not-an-integer", "b": 3},
        )


def test_missing_tool_argument_raises_error() -> None:
    registry = ToolRegistry()
    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )

    with pytest.raises(ToolArgumentsError):
        registry.call("add", {"a": 2})


def test_extra_tool_argument_raises_error() -> None:
    registry = ToolRegistry()
    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )

    with pytest.raises(ToolArgumentsError):
        registry.call(
            "add",
            {"a": 2, "b": 3, "c": 4},
        )


def test_register_rejects_non_callable_function() -> None:
    registry = ToolRegistry()
    invalid_function = cast(Callable[..., object], "not callable")

    with pytest.raises(TypeError):
        registry.register(
            "invalid",
            "Invalid tool",
            invalid_function,
            AddArguments,
        )
