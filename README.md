# Agent Core Python

A minimal typed Python registry for schema-validated agent tools.

## Why

LLM-generated tool arguments are untrusted input. Agent applications need a boundary that describes tool parameters to a model, validates actual arguments at runtime, and calls Python functions only with normalized data.

Agent Core Python provides that boundary through a small typed tool registry built with Pydantic.

## Features

- Register ordinary Python callables with a name, description, and Pydantic argument model.
- Generate JSON Schema for tool discovery.
- Validate and convert arguments before invoking a tool.
- Reject missing, invalid, and extra arguments with `ToolArgumentsError`.
- Prevent duplicate tool names and non-callable registrations.

## Quickstart

Requirements:

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

Clone the repository and install the project:

```bash
git clone https://github.com/iamwzzr/agent-core-python.git
cd agent-core-python
uv sync
```

## Example

Run the included example:

```bash
uv run python examples/basic_usage.py
```

The example:

- defines two Pydantic argument models;
- registers `add` and `word_count` tools;
- prints their JSON input schemas;
- validates and converts tool arguments;
- executes both Python functions;
- catches a `ToolArgumentsError` and preserves the original Pydantic `ValidationError`.

No API key or network connection is required.

Expected key results:

```text
Tool results:
add: 5
word_count: 4

Validation error:
ToolArgumentsError: Invalid arguments for tool: add
Caused by: ValidationError
```

## Development

Install the project with development dependencies:

```bash
uv sync --dev
```

Run the test suite:

```bash
uv run pytest -q
```

Run tests with coverage:

```bash
uv run pytest --cov=agent_core_python --cov-report=term-missing
```

Check code quality and formatting:

```bash
uv run ruff check .
uv run ruff format --check .
```

Apply automatic formatting:

```bash
uv run ruff format .
```

## Current Limitations

This project currently focuses on the tool registry and validation boundary. It does not yet include:

- an LLM provider integration;
- an Agent Loop or multi-step orchestration;
- asynchronous tool execution;
- retries, timeouts, or execution limits;
- permissions or sandboxing for tools;
- conversation memory or persistent state.

## License

This project is released under the [MIT License](LICENSE).
