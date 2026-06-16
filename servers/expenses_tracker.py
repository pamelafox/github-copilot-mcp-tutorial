import csv
import logging
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastmcp import Context, FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text
from prefab_ui.components.table import Table, TableBody, TableCell, TableHead, TableHeader, TableRow
from pydantic import BaseModel, Field

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("ExpensesMCP")
logger.setLevel(logging.INFO)

SCRIPT_DIR = Path(__file__).parent
EXPENSES_FILE = SCRIPT_DIR / "expenses.csv"


mcp = FastMCP("Expenses Tracker")


class PaymentMethod(Enum):
    AMEX = "amex"
    VISA = "visa"
    CASH = "cash"


class Category(Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    GADGET = "gadget"
    OTHER = "other"


@mcp.tool
async def add_expense(
    date: Annotated[date, "Date of the expense in YYYY-MM-DD format"],
    amount: Annotated[float, "Positive numeric amount of the expense"],
    category: Annotated[Category, "Category label"],
    description: Annotated[str, "Human-readable description of the expense"],
    payment_method: Annotated[PaymentMethod, "Payment method used"],
) -> str:
    """Add a new expense to the expenses.csv file."""
    if amount <= 0:
        return "Error: Amount must be positive"

    date_iso = date.isoformat()
    logger.info(f"Adding expense: ${amount} for {description} on {date_iso}")

    try:
        file_exists = EXPENSES_FILE.exists()

        with open(EXPENSES_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["date", "amount", "category", "description", "payment_method"])

            writer.writerow([date_iso, amount, category.value, description, payment_method.value])

        return f"Successfully added expense: ${amount} for {description} on {date_iso}"

    except Exception as e:
        logger.error(f"Error adding expense: {str(e)}")
        return "Error: Unable to add expense"


@mcp.resource("resource://expenses")
async def get_expenses_data():
    """Get raw expense data from CSV file"""
    logger.info("Expenses data accessed")

    try:
        with open(EXPENSES_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expenses_data = list(reader)

        csv_content = f"Expense data ({len(expenses_data)} entries):\n\n"
        for expense in expenses_data:
            csv_content += (
                f"Date: {expense['date']}, "
                f"Amount: ${expense['amount']}, "
                f"Category: {expense['category']}, "
                f"Description: {expense['description']}, "
                f"Payment: {expense['payment_method']}\n"
            )

        return csv_content

    except FileNotFoundError:
        logger.error("Expenses file not found")
        return "Error: Expense data unavailable"
    except Exception as e:
        logger.error(f"Error reading expenses: {str(e)}")
        return "Error: Unable to retrieve expense data"


@mcp.prompt
def analyze_spending_prompt(
    category: str | None = None, start_date: str | None = None, end_date: str | None = None
) -> str:
    """Generate a prompt to analyze spending patterns with optional filters."""

    filters = []
    if category:
        filters.append(f"Category: {category}")
    if start_date:
        filters.append(f"From: {start_date}")
    if end_date:
        filters.append(f"To: {end_date}")

    filter_text = f" ({', '.join(filters)})" if filters else ""

    return f"""
    Please analyze my spending patterns{filter_text} and provide:

    1. Total spending breakdown by category
    2. Average daily/weekly spending
    3. Most expensive single transaction
    4. Payment method distribution
    5. Spending trends or unusual patterns
    6. Recommendations for budget optimization

    Use the expense data to generate actionable insights.
    """


@mcp.tool
async def remove_expenses_for_date(
    expense_date: Annotated[date, "Date of expenses to remove in YYYY-MM-DD format"],
    ctx: Context,
) -> str:
    """Remove all expenses for a date after user confirmation."""
    class DeleteExpensesConfirmation(BaseModel):
        confirm: bool = Field(title="Delete expenses", description="Delete all expenses for this date?")

    date_iso = expense_date.isoformat()

    try:
        with open(EXPENSES_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames or ["date", "amount", "category", "description", "payment_method"]
            expenses = list(reader)

        matching_expenses = [expense for expense in expenses if expense.get("date") == date_iso]

        if not matching_expenses:
            return f"No expenses found for {date_iso}."

        total = 0.0
        for expense in matching_expenses:
            try:
                total += float(expense.get("amount", 0))
            except ValueError:
                pass

        response = await ctx.elicit(
            message=f"Delete {len(matching_expenses)} expense(s) from {date_iso} totaling ${total:.2f}?",
            response_type=DeleteExpensesConfirmation,
        )

        if response.action != "accept" or not response.data.confirm:
            return "Deletion cancelled."

        remaining_expenses = [expense for expense in expenses if expense.get("date") != date_iso]

        with open(EXPENSES_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(remaining_expenses)

        return f"Removed {len(matching_expenses)} expense(s) for {date_iso}."

    except FileNotFoundError:
        return "No expenses file found."
    except Exception as e:
        logger.error(f"Error removing expenses: {str(e)}")
        return "Error: Unable to remove expenses"


@mcp.tool(app=True)
def render_expenses() -> PrefabApp:
    """Render the expenses as an interactive table."""
    try:
        with open(EXPENSES_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
    except FileNotFoundError:
        expenses = []

    with Column(gap=4, css_class="p-6") as view:
        Heading("Expenses")

        if not expenses:
            Text("No expenses found.")
        else:
            with Table():
                with TableHeader():
                    with TableRow():
                        TableHead("Date")
                        TableHead("Amount")
                        TableHead("Category")
                        TableHead("Description")
                        TableHead("Payment")

                with TableBody():
                    for expense in expenses:
                        amount = expense.get("amount", "")
                        try:
                            amount = f"${float(amount):.2f}"
                        except ValueError:
                            pass

                        with TableRow():
                            TableCell(expense.get("date", ""))
                            TableCell(amount)
                            TableCell(expense.get("category", ""))
                            TableCell(expense.get("description", ""))
                            TableCell(expense.get("payment_method", ""))

    return PrefabApp(view=view)


if __name__ == "__main__":
    logger.info("MCP Expenses server starting (HTTP mode on port 8000)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)