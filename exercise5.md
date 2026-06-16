# Exercise 5: Add Keycloak authentication to your MCP server

In this exercise, you'll add OAuth 2.1 authentication to your store server using [Keycloak](https://www.keycloak.org/), an open-source identity server. After this, only authenticated users can access your server's tools — and the server can identify who is making each request.

- [Step 1: Add Keycloak auth to your server](#step-1-add-keycloak-auth-to-your-server)
- [Step 2: Test the OAuth flow](#step-2-test-the-oauth-flow)
- [Step 3: Make tools user-aware](#step-3-make-tools-user-aware)
- [Recommended reading](#recommended-reading)

---

## Step 1: Add Keycloak auth to your server

Your instructor has a Keycloak instance running with a pre-configured realm and test user accounts. You'll connect your store server to it.
Open your `servers/store_server.py` and make the following changes:

1. **Add the import** at the top of the file:

    ```python
    from fastmcp.server.auth.providers.keycloak import KeycloakAuthProvider
    ```

2. **Configure the auth provider** (before you construct the app):

    ```python
    auth = KeycloakAuthProvider(
        realm_url="https://pf-keycloakmcp-jscl-kc.nicesand-8c230ae8.westus.azurecontainerapps.io/auth/realms/mcp",
        base_url="http://localhost:8420",
        required_scopes=["openid", "mcp:access"],
        audience="mcp-server",
    )
    ```

3. **Pass `auth` to your FastMCP constructor:**

    ```python
    mcp = FastMCP("Your Store Name", auth=auth)
    ```

---

## Step 2: Test the OAuth flow

Restart your server:

```bash
uv run servers/store_server.py
```

Now connect your coding agent to the MCP server. The configuration should point at the same URL, but you may need to restart the server in your coding agent so that it realizes that it now requires authentication.

When you ask the coding agent to use the server:

1. The MCP client detects the server requires authentication (since it receives a 401 response).
2. A browser window opens to the Keycloak login page. Log in with the credentials for the test user: `testuser`, `testpass`.
4. Keycloak shows a consent page. Click **Allow**.
5. The browser redirects back, and the tool call succeeds.

Try asking:

```text
Buy a product from the store
```

You should see the normal response, but now it went through the full OAuth flow first. Check your server's terminal output — you'll see the 401, the token exchange, and then the authenticated 200.

---

## Step 3: Make tools user-aware

Now that users are authenticated, you can identify who is making each request. This requires adding middleware that extracts the user ID from the OAuth token and makes it available to your tools.

**1. Add these imports:**

```python
from fastmcp import Context
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import Middleware, MiddlewareContext
```

**2. Add the middleware class** (before you construct the app):

```python
class UserAuthMiddleware(Middleware):
    def _get_user_id(self):
        token = get_access_token()
        if not (token and hasattr(token, "claims")):
            return None
        return token.claims.get("sub")

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        user_id = self._get_user_id()
        if context.fastmcp_context is not None:
            await context.fastmcp_context.set_state("user_id", user_id)
        return await call_next(context)
```

**3. Wire the middleware into your server:**

```python
mcp = FastMCP("Your Store Name", auth=auth, middleware=[UserAuthMiddleware()])
```

**4. Update `buy_product` to use the user ID:**

If you didn't add `ctx: Context` in Exercise 4, add it now. Then extract and use the user ID:

```python
@mcp.tool
async def buy_product(
    product_name: Annotated[str, "Name of the product to buy"],
    quantity: Annotated[int, "Number of items to buy"],
    ctx: Context,
) -> str:
    """Buy a product from the store, reducing its inventory."""
    user_id = await ctx.get_state("user_id")

    # ... your existing buy logic ...

    return f"User {user_id} bought {quantity}x {product_name} for ${total:.2f}"
```

Restart the server and buy a product — you should see your Keycloak user ID in the response.

---

## Recommended reading

- [MCP Auth specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) — The full OAuth 2.1 protocol for MCP
- [FastMCP auth providers](https://gofastmcp.com/servers/auth) — Built-in providers for Keycloak, Entra, Auth0, ScaleKit, and more
- [Python + MCP: Authentication session](https://aka.ms/pythonmcp/slides/auth) — Slides covering key-based, OAuth, Keycloak, and Entra auth
- [python-mcp-demos](https://github.com/Azure-Samples/python-mcp-demos) — Full examples with Keycloak and Entra deployment
