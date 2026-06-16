# Exercise 2: Code a Python agent with MCP tools

In this exercise, you'll write a Python script that creates an AI agent and connects it to an MCP server. The agent will use the MCP server's tools to answer questions - just like the coding agents from Exercise 1, but now you're building the agent yourself.

- [Step 1: Set up an LLM connection](#step-1-set-up-an-llm-connection)
    - [Option 1: Ollama](#option-1-ollama)
    - [Option 2: OpenRouter](#option-2-openrouter)
    - [Option 3: OpenAI](#option-3-openai)
    - [Option 4: Azure OpenAI](#option-4-azure-openai)
- [Step 2: Build an agent with MCP tools](#step-2-build-an-agent-with-mcp-tools)
  - [Option A: Pydantic AI](#option-a-pydantic-ai)
  - [Option B: LangChain v1](#option-b-langchain-v1)
  - [Option C: Microsoft Agent Framework](#option-c-microsoft-agent-framework)
- [Try it out](#try-it-out)
- [Full reference examples](#full-reference-examples)

---

## Step 1: Set up an LLM connection

Your agent needs access to an LLM that supports **tool calling**. Pick **one** of the providers below and create a `.env` file in the repo root. For all providers, use the same three variables: `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL_NAME`.

### Option 1: Ollama

Use [Ollama](https://ollama.com/) to run a local LLM on your machine - no API key required.
⚠️ If you're on shared WiFi, do _not_ pull any new models. In that case, only use Ollama if you have a powerful enough model downloaded already.

1. [Install Ollama](https://ollama.com/download)
2. Pull a model that supports [tool calling](https://ollama.com/search?c=tools):

   ```bash
   ollama pull gemma4:e4b
   ```

    > **Note:** Ollama runs entirely on the machine. A model like `gemma4:e4b` needs ~32 GB of RAM. If your machine has less RAM, try `llama3.1:8b` instead.


3. Add to your `.env`:

   ```text
   LLM_BASE_URL=http://localhost:11434/v1
   LLM_API_KEY=ollama
   LLM_MODEL_NAME=gemma4:e4b
   ```

   If you're using the repository Dev Container, change `LLM_BASE_URL` to:

   ```text
   LLM_BASE_URL=http://host.docker.internal:11434/v1
   ```

### Option 2: OpenRouter

[OpenRouter](https://openrouter.ai/) gives you access to many models through a single API key, including free-tier models.

1. Sign up at [openrouter.ai](https://openrouter.ai/) and get an API key.
2. Add to your `.env`:

   ```text
   LLM_BASE_URL=https://openrouter.ai/api/v1
   LLM_API_KEY=<your OpenRouter API key>
   LLM_MODEL_NAME=google/gemma-3-27b-it
   ```

### Option 3: OpenAI

Use the [OpenAI API](https://platform.openai.com/) directly.

1. Get an API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. Add to your `.env`:

   ```text
   LLM_BASE_URL=https://api.openai.com/v1
   LLM_API_KEY=<your OpenAI API key>
   LLM_MODEL_NAME=gpt-5.4
   ```

### Option 4: Azure OpenAI

Use [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/).

1. You need an Azure OpenAI endpoint and a deployed chat model.
2. Add to your `.env`:

   ```text
   LLM_BASE_URL=<your endpoint>/openai/v1
   LLM_API_KEY=<your API key>
   LLM_MODEL_NAME=<your deployment name>
   ```

## Step 2: Build an agent with MCP tools

Now pick **one** of the three framework options below. Each gives you a skeleton - your job is to fill in the MCP server connection details.

### Option A: Pydantic AI

Create `agents/exercise2_pydanticai.py` with this skeleton:

```python
import asyncio
import logging
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv(override=True)


async def main():
    # TODO: Ensure .env has alll the required env variables for LLM host
    openai_client = AsyncOpenAI(
        base_url=os.environ["LLM_BASE_URL"],
        api_key=os.environ["LLM_API_KEY"],
    )
    model = OpenAIChatModel(
        os.environ["LLM_MODEL_NAME"],
        provider=OpenAIProvider(openai_client=openai_client),
    )

    server = MCPServerStreamableHTTP(
        url="________",  # TODO: Set the MCP server URL
    )

    agent: Agent[None, str] = Agent(
        model,
        system_prompt=(
            "You help answer questions using documentation. "
            "Cite the DeepWiki sources you used at the end of your answer."
        ),
        output_type=str,
        toolsets=[server],
    )

    result = await agent.run(
        "Consult the PrefectHQ/fastmcp changelog and list the last 5 FastMCP releases "
        "with release names and one highlight each."
    )
    print(result.output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main())
```

Run it:

```bash
uv run agents/exercise2_pydanticai.py
```

---

### Option B: LangChain v1

Create `agents/exercise2_langchain.py` with this skeleton:

```python
import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv(override=True)


async def run_agent():
    # TODO: Configure ChatOpenAI using LLM_* env vars.
    model = ChatOpenAI(
        model=os.environ["LLM_MODEL_NAME"],
        base_url=os.environ["LLM_BASE_URL"],
        api_key=SecretStr(os.environ["LLM_API_KEY"]),
    )

    client = MultiServerMCPClient(
        {
            "________": {  # TODO: Set a server name
                "url": "________",  # TODO: Set the MCP server URL
                "transport": "streamable_http",
            }
        }
    )

    tools = await client.get_tools()
    agent = create_agent(
        model,
        tools,
        system_prompt=(
            "Use DeepWiki tools for repository-grounded answers and "
            "cite the DeepWiki sources you used at the end."
        ),
    )

    response = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "Consult the FastMCP Changelog and list the last 5 FastMCP "
                        "releases with release names and one highlight each from "
                        "PrefectHQ/fastmcp."
                    )
                ),
            ]
        }
    )

    print(response["messages"][-1].text)


if __name__ == "__main__":
    asyncio.run(run_agent())
```

Run it:

```bash
uv run agents/exercise2_langchain.py
```

---

### Option C: Microsoft Agent Framework

Create `agents/exercise2_agentframework.py` with this skeleton:

```python
import asyncio
import os

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv(override=True)


async def main():
    client = OpenAIChatCompletionClient(
        base_url=os.environ["LLM_BASE_URL"],
        api_key=os.environ["LLM_API_KEY"],
        model=os.environ["LLM_MODEL_NAME"],
    )

    async with (
        MCPStreamableHTTPTool(
            name="________",  # TODO: Give the MCP server a name
            url="________",  # TODO: Set the MCP server URL
        ) as mcp_server,
        Agent(
            client=client,
            name="DocsAgent",
            instructions=(
                "You help answer questions using documentation. "
                "Cite the DeepWiki sources you used at the end of your answer."
            ),
            tools=[mcp_server],
        ) as agent,
    ):
        result = await agent.run(
            "Consult the PrefectHQ/fastmcp changelog and list the last 5 FastMCP releases "
            "with release names and one highlight each."
        )
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run agents/exercise2_agentframework.py
```

---

## Take it further

Once your agent works with DeepWiki, try extending it with one or more of these ideas:

- Try different questions: ask architecture questions, changelog summaries, release comparisons, or troubleshooting questions.
- Change the output style with system prompts: ask for bullets, tables, executive summaries, or JSON output.
- Use citation-focused prompts: require source links at the end and compare answer quality.
- Swap to a different MCP server: for example, try the Hugging Face MCP server (`https://huggingface.co/mcp`) and ask about popular text generation models.
- Connect multiple MCP servers at once: register DeepWiki plus another server and ask cross-source questions.
- Add server-selection guidance to the prompt: tell the agent when to use each server and when to combine them.
- Compare frameworks: run the same prompt in Pydantic AI, LangChain, and Agent Framework, then compare tool-call behavior and answer formatting.