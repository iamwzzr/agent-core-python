from collections.abc import Callable
from typing import cast

import pytest
from pydantic import BaseModel, ConfigDict, ValidationError

from agent_core_python.models import ToolCall, ToolResult
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


def test_empty_registry_lists_no_tools() -> None:
    registry = ToolRegistry()

    assert registry.list_tools() == []


def test_list_tools_preserves_registration_order() -> None:
    registry = ToolRegistry()

    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )
    registry.register(
        "word_count",
        "Count words in text",
        word_count,
        WordCountArguments,
    )

    listed_tools = registry.list_tools()

    assert [(tool["name"], tool["description"]) for tool in listed_tools] == [
        ("add", "Add two integers"),
        ("word_count", "Count words in text"),
    ]


def test_tool_arguments_error_preserves_validation_error() -> None:
    registry = ToolRegistry()
    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )

    with pytest.raises(ToolArgumentsError) as exception_info:
        registry.call(
            "add",
            {"a": "not-an-integer", "b": 3},
        )

    assert isinstance(
        exception_info.value.__cause__,
        ValidationError,
    )


def test_execute_returns_tool_result() -> None:
    registry = ToolRegistry()
    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )
    tool_call = ToolCall(
        name="add",
        arguments={"a": "2", "b": 3},
    )

    result = registry.execute(tool_call)

    assert isinstance(result, ToolResult)
    assert result.tool_name == "add"
    assert result.output == 5


def test_execute_unknown_tool_raises_error() -> None:
    registry = ToolRegistry()
    tool_call = ToolCall(
        name="missing",
        arguments={},
    )

    with pytest.raises(ToolNotFoundError):
        registry.execute(tool_call)


def test_execute_invalid_arguments_raises_error() -> None:
    registry = ToolRegistry()
    registry.register(
        "add",
        "Add two integers",
        add,
        AddArguments,
    )
    tool_call = ToolCall(
        name="add",
        arguments={"a": "not-an-integer", "b": 3},
    )

    with pytest.raises(ToolArgumentsError):
        registry.execute(tool_call)


def test_tool_call_rejects_extra_fields() -> None:
    raw_tool_call = {
        "name": "add",
        "arguments": {"a": 2, "b": 3},
        "unexpected": True,
    }

    with pytest.raises(ValidationError):
        ToolCall.model_validate(raw_tool_call)
