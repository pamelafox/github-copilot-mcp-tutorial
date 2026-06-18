# Exercise 3: Build your own MCP server

In this exercise, you'll build an MCP server from scratch using [FastMCP](https://gofastmcp.com/). You'll create your own **store** server — selling whatever products you want — with tools for browsing and buying, then test it with your coding agent and the MCP Inspector.

- [Step 1: Create the server skeleton](#step-1-create-the-server-skeleton)
- [Step 2: Customize the store](#step-2-customize-the-store)
- [Step 3: Add a tool to list products](#step-3-add-a-tool-to-list-products)
- [Step 4: Add a tool to buy a product](#step-4-add-a-tool-to-buy-a-product)
- [Step 5: Run and test the server](#step-5-run-and-test-the-server)
- [Step 6: Test with GitHub Copilot](#step-6-test-with-github-copilot)
- [Take it further](#take-it-further)

---

## Step 1: Create the server skeleton

Create a file called `servers/store_server.py` with the following starter code:

```python
import logging
from typing import Annotated

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("StoreMCP")
logger.setLevel(logging.INFO)

mcp = FastMCP("Bake & Take")

# In-memory product inventory: name -> {price, quantity}
INVENTORY = {
    "Croissant": {"price": 3.50, "quantity": 40},
    "Sourdough Loaf": {"price": 8.00, "quantity": 12},
    "Cinnamon Roll": {"price": 4.25, "quantity": 20},
    "Blueberry Muffin": {"price": 3.00, "quantity": 35},
}

# TODO: Add your tools here (Steps 3 and 4)


if __name__ == "__main__":
    logger.info("Store MCP server starting (HTTP mode on port 8420)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8420)
```

---

## Step 2: Customize the store

The starter code uses a bakery theme, but you can change it to anything you like. Pick a theme and update the `FastMCP` name and `INVENTORY` in your file:

| Theme | Example products |
| --- | --- |
| Bookshop | Python Crash Course, Designing Data-Intensive Applications |
| Plant Shop | Monstera, Snake Plant, Pothos |
| Coffee Roaster | Ethiopian Yirgacheffe, Colombian Supremo |
| Record Store | Kind of Blue (Miles Davis), Rumours (Fleetwood Mac) |

Each product needs a `price` and `quantity`. Feel free to keep the bakery if you like it — just make sure you have at least 3–5 products before moving on.

---

## Step 3: Add a tool to list products

Add a tool that returns the current product listings:

```python
@mcp.tool
async def list_products() -> dict:
    """List all available products with their prices and stock levels."""
    return INVENTORY
```

---

## Step 4: Add a tool to buy a product

Add a tool that "buys" a product by reducing its quantity in the inventory.

```python
@mcp.tool
async def buy_product(
    name: Annotated[str, "Name of the product"],
    quantity: Annotated[int, "Quantity of product to buy"],
) -> str:
    """Buy a product from the store, reducing its inventory."""
    if name not in INVENTORY:
        raise ToolError(f"'{name}' is not available in the store.")
    product = INVENTORY[name]
    if product["quantity"] < quantity:
        raise ToolError(f"Only {product['quantity']} units of '{name}' are in stock.")
    product["quantity"] -= quantity
    total = product["price"] * quantity
    return f"Purchased {quantity}x {name} for ${total:.2f}. Remaining stock: {product['quantity']}."
```

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

With the server running, add it to GitHub Copilot.

### GitHub Copilot in VS Code

1. Add to `.mcp.json`:

    ```json
    {
        "mcpServers": {
            "product-store": {
                "type": "http",
                "url": "http://localhost:8420/mcp"
            }
        }
    }
    ```

2. Select "Start" from the CodeLens menu above the server entry.

3. Close the `store_server.py` file so that Copilot does not keep the file in its direct context and try to answer questions based on the file itself.

3. Open the "Configure tools" button from the Copilot chat, and ensure that "product-store" mcp server is enabled, with the expected tools listed.

4. Ask Copilot to query the store:

    ```text
    What products are available in the store?
    ```

    Make sure that Copilot uses the MCP server to answer the question, **not** the local file.

5. Ask Copilot to buy a product from the store, based on the listed products.

### GitHub Copilot CLI

1. Add the MCP server using this command:

   ```bash
   copilot mcp add --transport http product-store http://localhost:8420/mcp
   ```

2. Ask Copilot to query the store:

   ```bash
   copilot -i "What products are available in the store?"
   ```

### GitHub Copilot app

1. Open the GitHub Copilot app.
2. Select the "Settings" (gear) icon in the bottom left.
3. Select "MCP servers" from settings menu.
4. Select "+ Add server" and "Add custom server".

   * For server name, enter "product-store"
   * Select "HTTP" next to server name.
   * For URL, enter "http://localhost:8420/mcp"
   * Select "Add server"

5. In a new chat, ask Copilot to query the store:

   ```text
   What products are available in the store?
   ```

## Take it further

If you finish early, try adding:

- A `search_products` tool that filters by keyword or price range
- A `@mcp.resource` that exposes the full inventory as read-only data
- A `@mcp.prompt` that generates a shopping recommendation prompt
