# Exercise 2: Use the GitHub MCP server

In this exercise, you'll connect to the GitHub MCP server, use it to find issues on this repository, implement a fix, and open a pull request — all from Copilot.

- [Step 1: Connect the GitHub MCP server](#step-1-connect-the-github-mcp-server)
- [Step 2: Explore the issues](#step-2-explore-the-issues)
- [Step 3: Implement a fix and open a PR](#step-3-implement-a-fix-and-open-a-pr)

---

## Step 1: Connect the GitHub MCP server

The [GitHub MCP server](https://github.com/github/github-mcp-server) gives your agent access to GitHub repositories, issues, pull requests, and more. Unlike the MS Learn server from Exercise 1, this one requires authentication.

Follow the instructions for your agent: [GitHub Copilot in VS Code](#github-copilot-in-vs-code), [GitHub Copilot CLI](#github-copilot-cli), or [GitHub Copilot app](#github-copilot-app).

### GitHub Copilot in VS Code

1. Add the GitHub MCP server to your `.vscode/mcp.json`:

    ```json
    {
       "servers": {
          "github": {
             "type": "http",
             "url": "https://api.githubcopilot.com/mcp/"
          }
       }
    }
    ```

    > 🪧 **Note:** You can have multiple servers in the same `mcp.json` file. Keep the `mslearn` server from Exercise 1 if you like.

2. Select "Start" on the GitHub server in the config file.

3. A prompt will pop up asking whether the MCP server can authenticate to GitHub. Select **Allow**.

4. Click the tools icon in the Copilot Chat panel and confirm the GitHub tools are listed. You should see tools like `list_issues`, `create_pull_request`, `get_file_contents`, and many more.

5. Move on to [Step 2](#step-2-explore-the-issues).

### GitHub Copilot CLI

The GitHub Copilot CLI already comes bundled with the GitHub MCP server.

1. Start Copilot CLI with all GitHub MCP toolsets enabled:

   ```bash
   copilot --enable-all-github-mcp-tools
   ```

   For more setup and customization options, see the [Copilot CLI installation guide](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-copilot-cli.md).

2. Send "/mcp show github-mcp-server" to confirm the built-in server is available and has all tools enabled (around 100).
3. Move on to [Step 2](#step-2-explore-the-issues).


### GitHub Copilot app

The GitHub Copilot app comes bundled with the GitHub MCP. 

1. Ask Copilot whether it has access to the GitHub MCP server tools.

   ```text
   Do you have access to the GitHub MCP server?
   ```

2. Move on to [Step 2](#step-2-explore-the-issues).

---

## Step 2: Explore the issues

This repository has a small quiz script in `src/quiz.py` with some known bugs and missing features, tracked as GitHub issues.

1. Ask Copilot to list the open issues on this repository:

   ```text
   How many open issues are there on this repository? Summarize the issues for me.
   ```

   > 🪧 **Note:** Watch how Copilot calls the GitHub MCP server's `list_issues` tool. You may need to click **Continue** to approve the tool call.

2. Ask Copilot to recommend which issue to work on:

   ```text
   Which of these issues would be the easiest to fix? Pick one for me.
   ```

3. Before implementing, you can try running the quiz yourself to see the bugs firsthand:

   ```bash
   python src/quiz.py
   ```

4. Ask Copilot to implement the issue:

   ```text
   Fix that issue. Follow these steps:
   1. Checkout a new local branch for the fix.
   2. Make the changes to src/quiz.py.
   3. Commit and push the branch.
   4. Create a pull request that references the issue.
   ```

   > ⚠️ **Warning:** Always verify the actions Copilot is asking to perform, especially with write operations from an MCP server. Review the tool calls before clicking **Continue**.

5. Once the pull request is created, open it in GitHub and review the changes.

### Take it further

If you finish early, try one of these:

- **Fix another issue** — Start a new chat and pick a different issue from the list.
- **Search for repos** — Ask Copilot to search GitHub for other MCP-related repositories.
- **Explore the tools** — Ask Copilot what GitHub MCP tools are available and try one you haven't used yet.
