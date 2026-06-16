# Exercise 4: Add advanced features to your MCP server

In this exercise, you'll add a visual UI to your store server from Exercise 3 using [Prefab UI](https://gofastmcp.com/apps/prefab) — an interactive component library for FastMCP apps. Instead of returning plain text, your tools will render charts, tables, and cards directly in the host's conversation.

- [Step 1: Add an inventory dashboard tool](#step-1-add-an-inventory-dashboard-tool)
- [Step 2: Purchase confirmation with elicitation](#step-2-purchase-confirmation-with-elicitation)
- [Take it further](#take-it-further)
- [Further reading](#further-reading)

---

## Step 1: Add an inventory dashboard tool

Add a new tool to your `servers/store_server.py` that shows inventory levels as a bar chart. Add these imports at the top of your file:

```python
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading
from prefab_ui.components.charts import BarChart, ChartSeries
```

Then add this tool that has `app=True` and fill in the TODO to build the chart data from your `INVENTORY`:

```python
@mcp.tool(app=True)
def show_inventory_chart() -> PrefabApp:
    """Show current inventory levels as an interactive bar chart."""

    # TODO: Build a list of dicts from INVENTORY for the chart.
    # Each dict needs a "product" key (the name) and a "quantity" key.
    # Example: [{"product": "Croissant", "quantity": 40}, ...]
    data = []

    with Column(gap=4, css_class="p-6") as view:
        Heading("Inventory Levels")
        BarChart(
            data=data,
            series=[ChartSeries(data_key="quantity", label="In Stock")],
            x_axis="product",
        )

    return PrefabApp(view=view)
```

Restart the server:

```bash
uv run servers/store_server.py
```

Ask your coding agent:

```text
Show me the inventory chart
```

If the agent supports MCP apps, you should see an interactive bar chart rendered inline in the conversation:

![Inventory chart showing bar chart of product stock levels](docs/screenshot_inventorychart.png)

Try buying an available product, then viewing the chart again to see the updated quantities.

---

## Step 2: Purchase confirmation with elicitation

Instead of buying immediately, have the server ask the user to confirm the purchase. This uses [elicitation](https://gofastmcp.com/clients/elicitation) — a way for the server to request structured input from the user mid-operation.

Update your `buy_product` tool to use the `Context` object for elicitation. Add these imports:

```python
from fastmcp import Context
from pydantic import BaseModel, Field
```

Define a response model for the confirmation dialog:

```python
class PurchaseConfirmation(BaseModel):
    confirm: bool = Field(title="Confirm purchase", description="Approve this transaction?")
```

Then modify `buy_product` to accept a `ctx: Context` parameter and ask for confirmation before completing the purchase:

```python
@mcp.tool
async def buy_product(
    product_name: Annotated[str, "Name of the product to buy"],
    quantity: Annotated[int, "Number of items to buy"],
    ctx: Context,
) -> str:
    """Buy a product from the store, with user confirmation."""
    if product_name not in INVENTORY:
        return f"Error: '{product_name}' not found."

    product = INVENTORY[product_name]
    total = product["price"] * quantity

    # Ask the user to confirm before purchasing
    response = await ctx.elicit(
        message=f"Buy {quantity}x {product_name} for ${total:.2f}?",
        response_type=PurchaseConfirmation,
    )

    if response.action != "accept" or not response.data.confirm:
        return "Purchase cancelled."

    # TODO: Complete the purchase (check stock, reduce quantity, return success)
```


Restart the server:

```bash
uv run servers/store_server.py
```

Ask your coding agent to purchase an available item. If the agent supports elicitations, it should display a confirmation dialog:

![Dialog to confirm purchasing item](docs/screenshot_vscode_elicitation.png)

You can accept, decline, or cancel, and the tool should respond based on the choice.

---

## Take it further

If you finish early, try one of these ideas. 

**Apps:**

- **Product catalog with cards**: Display products as styled cards with prices and stock badges. Useful components: `Grid`, `Card`, `CardContent`, `Text`, `Badge`, `Separator`.
- **Sales dashboard**: Track purchases in a list and render them as a `Table` or a `LineChart` of revenue over time.
- **Filterable inventory**: Add a search `Input` and a `Select` for category, with reactive state to filter the displayed products.
- **Restock form**: Use `Form`, `Input`, and `Button` components to let the user add stock to a product directly from the UI.

**Elicitations:**

- **Quantity adjustment**: If the requested quantity exceeds stock, elicit the user to pick a smaller quantity instead of failing.
- **Shipping address**: Before completing a purchase, elicit a structured address (multiple fields in one Pydantic model).
- **Multi-step checkout**: Chain elicitations: confirm items → ask for gift wrap → ask for delivery date.
- **Discount code**: Optionally elicit a promo code with a free-text response, then apply a discount if it matches.

---

## Related reading

- [MCP Apps overview](https://gofastmcp.com/apps/overview) — Three other ways to build apps (FastMCPApp, Generative UI, custom HTML)
- [Prefab UI docs](https://gofastmcp.com/apps/prefab) — Full component reference (charts, tables, forms, state, reactivity)
- [Prefab patterns](https://gofastmcp.com/apps/patterns) — Dashboards, data tables, and more examples
- [Elicitation](https://gofastmcp.com/clients/elicitation) — Server-initiated user input requests
- [Background tasks](https://gofastmcp.com/servers/tasks) — Run long operations asynchronously with progress reporting
