from pprint import pprint

from pydantic import BaseModel, ConfigDict

from agent_core_python.tools import ToolArgumentsError, ToolRegistry


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


def main() -> None:
    registry = ToolRegistry()

    registry.register(
        name="add",
        description="Add two integers",
        function=add,
        arguments_model=AddArguments,
    )
    registry.register(
        name="word_count",
        description="Count words in text",
        function=word_count,
        arguments_model=WordCountArguments,
    )

    print("Registered tools:")
    pprint(registry.list_tools())

    add_result = registry.call(
        "add",
        {"a": "2", "b": 3},
    )
    word_count_result = registry.call(
        "word_count",
        {"text": "Agent tools need schemas"},
    )

    print("\nTool results:")
    print(f"add: {add_result}")
    print(f"word_count: {word_count_result}")

    print("\nValidation error:")
    try:
        registry.call(
            "add",
            {"a": "not-an-integer", "b": 3},
        )
    except ToolArgumentsError as error:
        print(f"{type(error).__name__}: {error}")
        print(f"Caused by: {type(error.__cause__).__name__}")


if __name__ == "__main__":
    main()
