# Exercise 3: Build your own MCP server

In this exercise, you'll build an MCP server from scratch using [FastMCP](https://gofastmcp.com/). You'll create your own **store** server — selling whatever products you want — with tools for browsing and buying, then test it with your coding agent and the MCP Inspector.

- [Step 1: Create the server skeleton](#step-1-create-the-server-skeleton)
- [Step 2: Design your inventory](#step-2-design-your-inventory)
- [Step 3: Add a tool to list products](#step-3-add-a-tool-to-list-products)
- [Step 4: Add a tool to buy a product](#step-4-add-a-tool-to-buy-a-product)
- [Step 5: Run and test the server](#step-5-run-and-test-the-server)
- [Step 6: Test with GitHub Copilot](#step-6-test-with-github-copilot)
- [Step 7: Test with MCP Inspector](#step-7-test-with-mcp-inspector)
- [Step 8: Test with MCPJam](#step-8-test-with-mcpjam)
- [Take it further](#take-it-further)

---

## Step 1: Create the server skeleton

Create a file called `servers/store_server.py` with the following starter code:

```python
import logging
from typing import Annotated

from fastmcp import FastMCP

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("StoreMCP")
logger.setLevel(logging.INFO)

mcp = FastMCP("________")  # TODO: Name your store!

# In-memory product inventory: name -> {price, quantity}
INVENTORY = {
    # TODO: Add your products here (Step 2)
}

# TODO: Add your tools here (Steps 3 and 4)


if __name__ == "__main__":
    logger.info("Store MCP server starting (HTTP mode on port 8420)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8420)
```

---

## Step 2: Design your inventory

Fill in the `INVENTORY` dictionary with **your own products**. Pick a theme — here are some ideas:

| Theme | Example products |
| --- | --- |
| Bakery | Croissant, Sourdough Loaf, Cinnamon Roll |
| Bookshop | Python Crash Course, Designing Data-Intensive Applications |
| Plant Shop | Monstera, Snake Plant, Pothos |
| Coffee Roaster | Ethiopian Yirgacheffe, Colombian Supremo |
| Record Store | Kind of Blue (Miles Davis), Rumours (Fleetwood Mac) |

Each product needs a `price` and `quantity`. For example:

```python
INVENTORY = {
    "Croissant": {"price": 3.50, "quantity": 40},
    # ...
}
```

Add at least 3–5 products.

Give your store a name too, by updating the `FastMCP("________")` line to match your theme (e.g. `FastMCP("Bake & Shake")`).

---

## Step 3: Add a tool to list products

Add a tool that returns the current product listings. Here's the structure — fill in the implementation:

```python
@mcp.tool
async def list_products() -> # TODO: return type:
    """List all available products with their prices and stock levels."""
    # TODO: Return the inventory as the specified return type
```

---

## Step 4: Add a tool to buy a product

Add a tool that "buys" a product by reducing its quantity in the inventory. Fill in the arguments and implementation:

```python
@mcp.tool
async def buy_product(
    # TODO: Add arguments for this tool using Annotated types.
    # What does the LLM need to provide to buy a product?
    # Hint: You'll need at least a product name and a quantity.
) -> # TODO: return type:
    """Buy a product from the store, reducing its inventory."""
    # TODO: Implement the buy logic:
    # 1. Check if the product exists in INVENTORY
    # 2. Check if there's enough stock
    # 3. Reduce the quantity and return a success message
```

For reference, you can see what a tool with typed arguments looks like in FastMCP (from the [expenses demo server](servers/expenses_tracker.py)). Each argument uses `Annotated[type, "description"]` so the LLM knows what to pass.

---

## Step 5: Run and test the server

Start the server:

```bash
uv run servers/store_server.py
```

You should see output like:

```text
Product Store MCP server starting (HTTP mode on port 8420)
```

The server is now listening at `http://localhost:8420/mcp`.

---

## Step 6: Test with GitHub Copilot

With the server running, add it to GitHub Copilot from Exercise 1.

### GitHub Copilot in VS Code

1. Add to `.vscode/mcp.json`:

    ```json
    {
      "servers": {
        "product-store": {
          "type": "http",
          "url": "http://localhost:8420/mcp"
        }
      }
    }
    ```

2. Select "Start" from the CodeLens menu above the server entry.

3. Open the "Configure tools" button from the Copilot chat, and ensure that "product-store" mcp server is enabled, with the expected tools listed.

4. Try a prompt like "What products are available in the store?" Make sure that Copilot uses the MCP server to answer the question, **not** the local file. If you don't see an MCP tool call, you may need to close the file and start a new chat so that Copilot doesn't base its answer off of the file itself.

### GitHub Copilot CLI

1. Add the MCP server using this command:

   ```bash
   copilot mcp add --transport http product-store http://localhost:8420/mcp
   ```

2. Try a prompt like:

   ```bash
   copilot -i "What products are available in the store?"
   ```

---

## Step 7: Test with MCP Inspector

[MCP Inspector](https://github.com/modelcontextprotocol/inspector) lets you test your server directly without going through an LLM.

> 🪧 **Note:** MCP Inspector does not work if you're developing in GitHub Codespaces, due to cross-domain issues between the forwarded Inspector UI and the forwarded MCP server port.

1. In a new terminal (keep the server running), launch the inspector:

   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. In the Inspector UI, connect to `http://localhost:8420/mcp` using the HTTP transport.
3. Click **Tools** to see your `list_products` and `buy_product` tools.
4. Click a tool, fill in any arguments, and run it to see the result.

> **Tip:** MCP Inspector is great for debugging — you can see exactly what your server returns without the LLM interpreting it.

---

## Step 8: Test with MCPJam

[MCPJam](https://www.mcpjam.com/) is a web-based MCP playground that lets you interact with your server through a chat-like UI. It's a nice middle ground between the raw Inspector and a full coding agent.

> 🪧 **Note:** MCPJam does not work if you're developing in GitHub Codespaces, due to cross-domain issues between the forwarded Inspector UI and the forwarded MCP server port.

1. Launch MCPJam locally (needed to access localhost servers):

   ```bash
   npx @mcpjam/inspector@latest
   ```

2. Open the "Servers" tab and select "Add Server". Add the local server at `http://localhost:8420/mcp`.
3. Open the "Tools" tab and try out the server tools.
4. Open the "Chat" tab and enter prompts like listing products and buying products.

---

## Take it further

If you finish early, try adding:

- A `search_products` tool that filters by keyword or price range
- A `@mcp.resource` that exposes the full inventory as read-only data
- A `@mcp.prompt` that generates a shopping recommendation prompt
