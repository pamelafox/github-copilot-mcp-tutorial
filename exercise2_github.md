# Exercise 2: Use the GitHub MCP server

In this exercise, you'll connect to the [GitHub MCP server](https://github.com/github/github-mcp-server), which gives your agent access to GitHub repositories, issues, pull requests, and more. Unlike the MS Learn server from Exercise 1, this one requires authentication.

Follow the section for your agent:

- [GitHub Copilot in VS Code](#github-copilot-in-vs-code)
- [GitHub Copilot CLI](#github-copilot-cli)
- [GitHub Copilot app](#github-copilot-app)

---

## GitHub Copilot in VS Code

### Step 1: Connect the GitHub MCP server

1. Add the GitHub MCP server to your `.mcp.json`:

    ```json
    {
       "mcpServers": {
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

### Step 2: Find and fix an issue

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

---

## GitHub Copilot CLI

### Step 1: Connect the GitHub MCP server

The GitHub Copilot CLI already comes bundled with the GitHub MCP server, but it only has a small subset of tools enabled by default.

1. Start Copilot CLI with all GitHub MCP toolsets enabled:

   ```bash
   copilot --enable-all-github-mcp-tools
   ```

   For more setup and customization options, see the [Copilot CLI installation guide](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-copilot-cli.md).

2. Send "/mcp show github-mcp-server" to confirm the built-in server is available and has all tools enabled (around 100).

### Step 2: Find and fix an issue

This repository has a small quiz script in `src/quiz.py` with some known bugs and missing features, tracked as GitHub issues.

1. Ask Copilot to list the open issues on this repository:

   ```text
   How many open issues are there on this repository? Summarize the issues for me.
   ```

   > 🪧 **Note:** Watch how Copilot calls the GitHub MCP server's `list_issues` tool.

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

   > ⚠️ **Warning:** Always verify the actions Copilot is asking to perform, especially with write operations from an MCP server.

5. Once the pull request is created, open it in GitHub and review the changes.

### Take it further

If you finish early, try one of these:

- **Fix another issue** — Start a new chat and pick a different issue from the list.
- **Search for repos** — Ask Copilot to search GitHub for other MCP-related repositories.
- **Explore the tools** — Ask Copilot what GitHub MCP tools are available and try one you haven't used yet.

---

## GitHub Copilot app

### Step 1: Confirm the GitHub MCP server

The GitHub Copilot app comes bundled with the GitHub MCP server. It has a smaller set of tools than VS Code or the CLI — focused on reading and searching GitHub, rather than creating issues or pull requests.

1. Ask Copilot whether it has access to the GitHub MCP server tools:

   ```text
   Do you have access to the GitHub MCP server? What tools do you have?
   ```

2. Confirm you see tools like `get_file_contents` and `search_code`.

### Step 2: Explore code across GitHub

The GitHub MCP server's `search_code` tool lets you search across **all of GitHub** — not just your local files. Combined with `get_file_contents`, you can browse any public repository without cloning it. In this step, you'll use those tools to research how other projects implement a Python quiz, then use what you learn to improve this repository's quiz script.

1. First, take a look at the quiz script in this repository:

   ```text
   Read src/quiz.py. What patterns does it use? Are there any bugs?
   ```

2. Now search GitHub for other Python quiz implementations:

   ```text
   Search for Python files in other GitHub repos that implement a quiz in a Python script using OOP. Summarize 5 most similar scripts.
   ```

3. Pick an interesting result and explore it:

   ```text
   Read the full source of one of those quiz files. How does their approach compare to this repository's quiz.py?
   ```

4. Based on what you found, ask Copilot to improve the quiz:

   ```text
   Improve quiz.py based off learnings from that quiz and fix any bugs you notice.
   ```

5. Review the changes Copilot made and try running the updated quiz:

   ```bash
   python src/quiz.py
   ```

6. Once you're happy with the changes, ask Copilot to commit and open a pull request:

   ```text
   Commit these changes to a new branch, push it, and open a pull request.
   ```

   > 🪧 **Note:** The Copilot app doesn't have the GitHub MCP server's `create_pull_request` tool, but it can still create PRs using the `gh` CLI or its built-in tools.

### Take it further

If you finish early, try one of these:

- **Search for more patterns** — Ask Copilot to search GitHub for quiz apps that use features like randomized question order, difficulty levels, or timed questions, and apply one of those ideas.
- **Explore another repo** — Use `get_file_contents` to browse the structure of a well-known open source project without cloning it.
- **Find MCP examples** — Use `search_code` to find other MCP server implementations on GitHub and compare their approaches.
