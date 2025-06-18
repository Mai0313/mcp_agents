<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

⚠️ **IMPORTANT**: After making any code changes, adding features, or updating functionality, you MUST update .github/copilot-instructions.md to reflect the current project state and capabilities.

# Project Background

This is the **MCP Agents** project - a Python project template and Model Context Protocol (MCP) agent implementation. The project serves as both a comprehensive Python project template with modern tooling and CI/CD pipelines, and a practical implementation of MCP agents that can interact with various services like Atlassian (Jira/Confluence), Git repositories, and other MCP-compatible tools.

The project demonstrates how to create intelligent agents using the Model Context Protocol to connect Large Language Models (LLMs) with external tools and services, enabling automated interactions with enterprise systems like Jira ticket management and Confluence documentation.

# Project Structure / Features

## Core Architecture
- **Main Application**: `main.py` - Contains the `MCPAgent` class that orchestrates MCP connections and AutoGen agents
- **MCP Integration**: Uses the Model Context Protocol to connect with various external services
- **AutoGen Framework**: Leverages Microsoft's AutoGen for multi-agent conversations and tool execution
- **Async/Await Pattern**: Fully asynchronous implementation for efficient I/O operations

## Key Components

### MCPAgent Class (`main.py`)
- **Purpose**: Central class for managing MCP connections and agent interactions
- **Supported Protocols**: STDIO and SSE (Server-Sent Events) connections
- **LLM Integration**: Configured for Azure OpenAI with specific API endpoints
- **Tool Management**: Automatic discovery and execution of MCP tools

### Supported MCP Servers
- **Atlassian Integration**: Jira and Confluence operations via `mcp-atlassian`
- **Context7**: Documentation and knowledge base access via `@upstash/context7-mcp`
- **Codex**: Code-related operations via `codex mcp`
- **Gitea**: Git repository management via `gitea-mcp`

## Project Template Features

### 🏗️ Modern Development Environment
- **uv dependency management**: Fast, reliable Python package management
- **Multi-version support**: Python 3.10, 3.11, and 3.12
- **Type hints**: Full type annotation support with Pydantic models
- **VS Code Dev Container**: Fully configured development environment

### 🧪 Testing & Quality Assurance
- **pytest framework**: Comprehensive testing with 80% coverage requirement
- **Parallel execution**: Faster test runs with pytest-xdist
- **ruff linting**: Fast Python linter and formatter
- **pre-commit hooks**: Automated code quality checks

### 🚀 CI/CD Pipeline
- **Multi-version testing**: Automated testing across Python versions
- **Code quality checks**: Automated linting and formatting validation
- **Documentation deployment**: Automatic GitHub Pages deployment with MkDocs
- **Release automation**: Semantic versioning and changelog generation

### 📚 Documentation System
- **MkDocs Material**: Beautiful, responsive documentation
- **Auto-generation**: `scripts/gen_docs.py` for generating docs from code
- **Blog support**: Built-in blog functionality for project updates
- **API documentation**: Automatic API reference generation

## File Structure
```
├── .devcontainer/          # VS Code Dev Container configuration
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
- **.pre-commit-config.yaml**: Git hooks for code quality
- **docker-compose.yaml**: Container orchestration for development and deployment

## Environment Variables
- **API_KEY**: Required for LLM API access
- **JIRA_PERSONAL_TOKEN**: For Jira integration
- **CONFLUENCE_PERSONAL_TOKEN**: For Confluence integration
- Various SSL and configuration options for different MCP servers
