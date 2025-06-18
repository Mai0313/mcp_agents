<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

⚠️ **IMPORTANT**: After making any code changes, adding features, or updating functionality, you MUST update .github/copilot-instructions.md to reflect the current project state and capabilities.

# Project Background

This is the **MCP Agents** project - a Model Context Protocol (MCP) agent implementation that enables intelligent automation through LLM-powered agents. The project demonstrates how to create agents using the Model Context Protocol to connect Large Language Models with external tools and services, enabling automated interactions with enterprise systems like Jira ticket management, Confluence documentation, and other MCP-compatible services.

The project focuses on practical MCP agent implementation with support for multiple connection protocols and integration with various external services.

## Project Features

### 🤖 MCP Agent Implementation
- **MCPAgent Class**: Central orchestrator for MCP connections and agent interactions
- **Multi-Protocol Support**: STDIO and SSE (Server-Sent Events) connections
- **AutoGen Integration**: Leverages Microsoft's AutoGen for multi-agent conversations
- **Async/Await Pattern**: Fully asynchronous implementation for efficient operations

### 🔌 MCP Server Integrations
- **Atlassian Integration**: Jira and Confluence operations via `mcp-atlassian`
- **Context7**: Documentation and knowledge base access via `@upstash/context7-mcp`
- **Codex**: Code-related operations via `codex mcp`
- **Gitea**: Git repository management via `gitea-mcp`

### 🛠️ Development Environment
- **uv dependency management**: Fast, reliable Python package management
- **Type hints**: Full type annotation support with Pydantic models
- **Testing framework**: pytest with coverage reporting
- **Code quality**: ruff linting and formatting
- **Documentation**: MkDocs with automatic generation

## Core Architecture

### MCPAgent Class (`main.py`)
- **Purpose**: Central class for managing MCP connections and agent interactions
- **Supported Protocols**: STDIO and SSE (Server-Sent Events) connections
- **LLM Integration**: Configured for Azure OpenAI with specific API endpoints
- **Tool Management**: Automatic discovery and execution of MCP tools

### Key Methods
- `a_list_tools()`: Lists available MCP tools asynchronously
- `a_run(message)`: Executes agent with given message asynchronously
- `_session_context()`: Context manager for MCP session handling
- `_create_toolkit_and_run()`: Creates toolkit from MCP session and runs agent

### Supported Connection Types
- **StdioServerParameters**: For command-line MCP servers
- **SSEServerParameters**: For HTTP-based MCP servers with Server-Sent Events

## Usage Examples

The project includes examples for:
- Atlassian Jira/Confluence operations
- Documentation queries with Context7
- Code operations with Codex
- Git repository management with Gitea

## Environment Variables
- **API_KEY**: Required for LLM API access
- **JIRA_PERSONAL_TOKEN**: For Jira integration
- **CONFLUENCE_PERSONAL_TOKEN**: For Confluence integration
- Various SSL and configuration options for different MCP servers

## File Structure
```
├── .github/
│   ├── workflows/          # CI/CD workflows (test, code-quality, docs)
│   └── copilot-instructions.md
├── docker/                 # Docker configurations with multi-stage builds
├── docs/                   # MkDocs documentation source
├── scripts/                # Automation scripts
│   ├── gen_docs.py        # Documentation generation script
│   └── __init__.py
├── main.py                # Main MCP Agent implementation
├── pyproject.toml         # Project configuration with comprehensive settings
├── Makefile              # Development commands
├── docker-compose.yaml   # Container orchestration
└── README.md             # Comprehensive project documentation
```

## Development Workflow
- **Make commands**: `make clean`, `make format`, `make test`, `make gen-docs`
- **uv commands**: `uv add <package>`, `uv sync`, `uv run`
- **Testing**: pytest with coverage reporting and parallel execution
- **Documentation**: Automatic generation from code and markdown sources

## Configuration Files
- **pyproject.toml**: Comprehensive project configuration including pytest, coverage, and ruff settings
- **mkdocs.yml**: Documentation site configuration
- **docker-compose.yaml**: Container orchestration for development and deployment
