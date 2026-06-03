# Aislapian

A command-line AI agent built in Python using Google's Gemini API. It explores
codebases, reads and writes files, runs scripts, and iterates in a feedback
loop until it completes a task — extended with custom WhatsApp messaging tools
and a sub-agent poem generator.

---

## What it does

You pass a prompt on the command line. The agent sends it to Gemini along with a set of available tools, then enters a loop: the model decides which tool to call, the program executes it and feeds the result back, and this repeats until the model produces a final text answer. Full conversation history is maintained across iterations so the model has complete context at every step.

```bash
uv run main.py "Read calculator/main.py and tell me what it does"
```

---

## Agent loop

```
User prompt
     │
     ▼
┌─────────────┐       tool call        ┌──────────────┐
│  Gemini API │ ─────────────────────► │ call_function │
│  (model)    │ ◄───────────────────── │ (dispatcher) │
└─────────────┘       tool result      └──────────────┘
     │
     │ final text answer (no more tool calls)
     ▼
  Output to user
```

The loop is capped at a configurable max iteration count to prevent runaway agents.

---

## Tools

### Built-in (sandboxed file tools)

All file tools operate inside a working directory — the model cannot escape the sandbox.

| Tool | Description |
|------|-------------|
| `get_files_info` | List directory contents and file sizes |
| `get_file_content` | Read a file's contents (with size limits) |
| `write_file` | Write or overwrite a file |
| `run_python_file` | Execute a Python file |

### Custom extensions

| Tool | Description |
|------|-------------|
| `send_whatsapp_to_person` | Send a WhatsApp message to a contact via `pywhatkit` |
| `send_whatsapp_to_group` | Send a WhatsApp message to a group |
| `generate_poem` | A sub-agent tool — makes its own isolated Gemini call with a dedicated poet persona and returns a short poem |

> **Note:** `pywhatkit` sends via WhatsApp Web — it will open a browser tab to do so. It's not a silent background send.

The `generate_poem` tool is the most architecturally interesting: it spins up a completely separate Gemini conversation with its own system prompt, keeping the poet's context isolated from the main agent. The prompt-building logic is split into a pure function (`build_poem_prompt`) and an impure API call (`generate_poem`) to keep it testable.

---

## Architecture notes

**Central dispatcher (`call_function`)** routes the model's tool requests to the right Python function. It also injects runtime dependencies — the working directory path for file tools, and the Gemini `client` object for the poem tool — that the model itself cannot supply. This keeps individual tool functions decoupled from global state.

**Dependency injection** is used throughout so functions can be tested in isolation without requiring a live API connection or a real filesystem path.

---

## Setup

**Prerequisites**: Python 3.11+, [`uv`](https://docs.astral.sh/uv/)

1. Clone the repo and install dependencies:

```bash
git clone https://github.com/amelfia/Aislapian-Agent
cd Aislapian-Agent
uv sync
```

2. Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
```

Get a free API key from [Google AI Studio](https://aistudio.google.com/).

3. Run it:

```bash
uv run main.py "your prompt here"
```

---

## Example

```bash
uv run main.py "Look at the calculator app and fix any bugs you find"
```

The agent will explore the `calculator/` directory, read the source files, identify issues, and write fixes — all autonomously.

---

## Tech stack

- **Python** — core language
- **Google Gemini API** (`google-genai`) — the underlying model
- **uv** — dependency and environment management
- **pywhatkit** — WhatsApp messaging
- **python-dotenv** — API key loading from `.env`

---

## Project structure

```text
Aislapian-Agent/
├── main.py                          # Entry point; parses CLI args and starts the agent loop
├── config.py                        # Model config and agent settings (e.g. max iterations)
├── prompts.py                       # System prompt definitions
├── functions/
│   ├── call_function.py             # Central dispatcher; routes tool calls and injects deps
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   ├── run_python_file.py
│   ├── generate_poem.py             # Sub-agent tool with isolated Gemini call
│   ├── send_whatsapp_to_person.py
│   └── send_whatsapp_to_group.py
├── calculator/                      # Sample codebase for the agent to operate on
│   ├── main.py
│   ├── tests.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
├── test_get_file_content.py         # Unit tests (dependency-injected, no live API needed)
├── test_get_files_info.py
├── test_run_python_file.py
├── test_send_whatsapp_to_group.py
├── test_send_whatsapp_to_person.py
├── test_write_file.py
├── pyproject.toml
└── .gitignore
```

---

## Gitignored files

- `.env` — contains your API key
- `PyWhatKit_DB.txt` — generated by pywhatkit at runtime
- Any poem output files generated during runs

