<center>

# MCP Agents

[![python](https://img.shields.io/badge/-Python_3.10_%7C_3.11_%7C_3.12-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![uv](https://img.shields.io/badge/-uv_dependency_management-2C5F2D?logo=python&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![tests](https://github.com/Mai0313/mcp_agents/actions/workflows/test.yml/badge.svg)](https://github.com/Mai0313/mcp_agents/actions/workflows/test.yml)
[![code-quality](https://github.com/Mai0313/mcp_agents/actions/workflows/code-quality-check.yml/badge.svg)](https://github.com/Mai0313/mcp_agents/actions/workflows/code-quality-check.yml)
[![codecov](https://codecov.io/gh/Mai0313/mcp_agents/branch/master/graph/badge.svg)](https://codecov.io/gh/Mai0313/mcp_agents)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/Mai0313/mcp_agents/tree/master?tab=License-1-ov-file)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Mai0313/mcp_agents/pulls)
[![contributors](https://img.shields.io/github/contributors/Mai0313/mcp_agents.svg)](https://github.com/Mai0313/mcp_agents/graphs/contributors)

</center>

🤖 **A Model Context Protocol (MCP) agent implementation that enables intelligent automation through LLM-powered agents**

This project demonstrates how to create agents using the Model Context Protocol to connect Large Language Models with external tools and services, enabling automated interactions with enterprise systems like Jira, Confluence, Git repositories, and other MCP-compatible services.

**Other Languages**: [English](README.md) | [中文](README_cn.md)

## ✨ Features

### 🤖 **Multi-Agent MCP Implementation**

- **MCPAgent Class**: Central orchestrator for MCP connections and agent interactions
- **Multi-Protocol Support**: STDIO and SSE (Server-Sent Events) connections
- **AutoGen Integration**: Leverages Microsoft's AutoGen for multi-agent conversations
- **Async/Await Pattern**: Fully asynchronous implementation for efficient operations

### 🔌 **MCP Server Integrations**

- **Atlassian Integration**: Jira and Confluence operations via `mcp-atlassian`
- **Context7**: Documentation and knowledge base access via `@upstash/context7-mcp`
- **Codex**: Code-related operations via `codex mcp`
- **Gitea**: Git repository management via `gitea-mcp`
- **GitHub**: Integration via Server-Sent Events

### 🎯 **Intelligent Agent System**

- **Manager Agent**: Task analysis and routing coordinator
- **Documentation Agent**: Specialized for Jira tickets and Confluence pages
- **Code Agent**: Software development and technical operations
- **Planning Agent**: Strategic planning and task decomposition
- **Execution Agent**: Direct MCP tool execution specialist

### �️ **Development Environment**

- **uv dependency management**: Fast, reliable Python package management
- **Type hints**: Full type annotation support with Pydantic models
- **Testing framework**: pytest with coverage reporting
- **Code quality**: ruff linting and formatting
- **Documentation**: MkDocs with automatic generation

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- uv (Python package manager)
- API access to Azure OpenAI or compatible LLM service

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Mai0313/mcp_agents.git
    cd mcp_agents
    ```

2. Install dependencies:

    ```bash
    make uv-install  # Install uv if not already installed
    uv sync          # Install project dependencies
    ```

3. Set up environment variables:

    ```bash
    export API_KEY="your-llm-api-key"
    export BASE_URL="your-llm-base-url"
    export JIRA_PERSONAL_TOKEN="your-jira-token"
    export CONFLUENCE_PERSONAL_TOKEN="your-confluence-token"
    ```

### Basic Usage

1. **Simple Mode** - Direct tool execution:

    ```python
    from main import MCPAgent, StdioServerParameters

    # Configure MCP server (e.g., Atlassian)
    jira_params = StdioServerParameters(
        command="uvx",
        args=["mcp-atlassian==0.11.2"],
        env={
            "JIRA_URL": "https://your-jira-instance",
            "CONFLUENCE_URL": "https://your-confluence-instance",
            "JIRA_PERSONAL_TOKEN": "your-token",
            "CONFLUENCE_PERSONAL_TOKEN": "your-token",
        },
    )

    # Create and run agent
    agent = MCPAgent(model="gpt-4", params=jira_params)
    result = agent.run("Create a new Jira ticket for bug fixes")
    ```

2. **Swarm Mode** - Multi-agent collaboration:

    ```python
    # Use swarm mode for complex tasks
    result = asyncio.run(
        agent.a_run_swarm("Analyze the project requirements and create documentation in Confluence")
    )
    ```

## 📁 Project Structure

```
├── .github/
│   ├── workflows/          # CI/CD workflows
│   └── copilot-instructions.md  # Detailed technical documentation
├── docker/                 # Docker configurations
├── docs/                   # MkDocs documentation
├── scripts/                # Automation scripts
│   ├── gen_docs.py        # Documentation generation
│   └── __init__.py
├── src/                    # Source code modules
│   └── prompt.py          # Centralized prompt management
├── main.py                # Main MCP Agent implementation
├── pyproject.toml          # Project configuration
├── Makefile               # Development commands
├── docker-compose.yaml    # Container orchestration
└── README.md              # Project overview
```

## 🎯 Use Cases

### 📋 Documentation Management

- **Jira Operations**: Automated ticket creation, status updates, project management
- **Confluence Operations**: Page creation, content editing, documentation structuring
- **Cross-platform Integration**: Seamless coordination between Jira and Confluence
- **Dynamic Tool Integration**: Real-time discovery and utilization of available tools

### 💻 Software Development

- **Code Generation**: AI-powered code writing with best practices
- **Git Operations**: Automated repository management and PR creation
- **Development Workflows**: End-to-end development process automation
- **Adaptive Tool Usage**: Automatically adapts to available development tools

### 🔧 Complex Task Orchestration

- **Multi-step Planning**: Breaking down complex tasks into manageable components
- **Resource Coordination**: Intelligent allocation of specialized agents
- **Error Handling**: Robust fallback mechanisms and error recovery
- **Context-Aware Execution**: System messages generated based on actual tool availability

## 🛠️ Available Commands

```bash
# Development
make clean          # Clean autogenerated files
make format         # Run pre-commit hooks and formatting
make test           # Run all tests
make gen-docs       # Generate documentation

# Dependencies
make uv-install     # Install uv dependency manager
uv add <package>    # Add production dependency
uv add <package> --dev  # Add development dependency
uv sync            # Install all dependencies
```

## 🔧 Configuration

### Environment Variables

- **API_KEY**: Required for LLM API access
- **BASE_URL**: LLM service base URL (for Azure OpenAI or compatible services)
- **JIRA_PERSONAL_TOKEN**: For Jira integration
- **CONFLUENCE_PERSONAL_TOKEN**: For Confluence integration
- **GITHUB_TOKEN**: For GitHub integration (if using GitHub MCP server)

### MCP Server Configuration

The system supports multiple MCP servers:

- **Atlassian (mcp-atlassian)**: Jira and Confluence integration
- **Context7 (@upstash/context7-mcp)**: Documentation and knowledge base
- **Codex (codex mcp)**: Code-related operations
- **Gitea (gitea-mcp)**: Git repository management
- **GitHub (SSE-based)**: GitHub integration via Server-Sent Events

## 🚀 Execution Modes

### Simple Mode (`a_run`)

- **Single Agent**: Direct tool access without complex routing
- **Fast Execution**: Minimal overhead for straightforward tasks
- **Best For**: Simple Confluence/Jira operations, direct tool execution

### Swarm Mode (`a_run_swarm`)

- **Multi-Agent**: Specialized agents with intelligent routing
- **Advanced Coordination**: Complex task decomposition and collaboration
- **Best For**: Complex workflows, multi-system integration, planning tasks

## 🏗️ Architecture

### MCPAgent Class

The central orchestrator that manages MCP connections and coordinates agent interactions with support for both STDIO and SSE protocols.

### Multi-Agent System

- **Manager Agent**: Analyzes tasks and routes to appropriate specialists
- **Documentation Agent**: Handles Jira tickets and Confluence pages
- **Code Agent**: Manages software development and Git operations
- **Planning Agent**: Provides strategic planning and task decomposition
- **Execution Agent**: Executes MCP tools directly

### Dynamic Tool Discovery

The system automatically discovers available MCP tools at runtime and generates context-aware system messages for optimal agent performance.

## 🤝 Contributing

We welcome contributions! Please feel free to:

- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Share your experience using this MCP agent system
- Add support for new MCP servers

## 📖 Documentation

For detailed technical documentation and implementation details, see:

- [Copilot Instructions](.github/copilot-instructions.md) - Comprehensive technical documentation
- [Generated Docs](https://mai0313.github.io/mcp_agents/) - API documentation and guides

## 👥 Contributors

[![Contributors](https://contrib.rocks/image?repo=Mai0313/mcp_agents)](https://github.com/Mai0313/mcp_agents/graphs/contributors)

Made with [contrib.rocks](https://contrib.rocks)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
