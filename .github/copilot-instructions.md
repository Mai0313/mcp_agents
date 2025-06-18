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
- **Multi-Agent System**: Advanced swarm-based agent orchestration for specialized task handling

### Specialized Agent Architecture

The system now employs a sophisticated multi-agent architecture with specialized roles:

#### **Manager Agent**

- **Role**: Task analysis and routing coordinator
- **Responsibilities**: Analyzes user requests and routes to appropriate specialist agents
- **Routing Logic**: Documentation tasks → documentation_agent, Code tasks → code_agent, Complex tasks → planning_agent

#### **Planning Agent**

- **Role**: Strategic planning and task decomposition
- **Responsibilities**: Breaks down complex tasks into actionable steps, identifies dependencies
- **Handoff Strategy**: Routes to execution specialists based on plan requirements

#### **Documentation Agent**

- **Role**: Jira and Confluence operations specialist
- **Expertise**: Ticket management, page creation/editing, content structuring
- **Tools**: Dynamically configured with available Atlassian MCP tools
- **System Message**: Auto-generated based on real-time tool discovery

#### **Code Agent**

- **Role**: Software development and Git operations specialist
- **Expertise**: Code writing, repository management, PR creation, development workflows
- **Tools**: Specialized in Git MCP tools and code development

#### **Execution Agent**

- **Role**: Direct MCP tool execution specialist
- **Expertise**: Tool authentication, error handling, cross-system operations
- **Tools**: Access to all available MCP tools for specialized execution

### Key Methods

- `a_list_tools()`: Lists available MCP tools asynchronously
- `a_run(message)`: Executes simplified single-agent workflow
- `a_run_swarm(message)`: Executes multi-agent swarm workflow
- `_session_context()`: Context manager for MCP session handling
- `_create_toolkit_and_run()`: Creates specialized agent swarm and orchestrates task execution
- `_create_toolkit_and_run_simple()`: Simplified single-agent execution for direct tool usage
- `_generate_dynamic_system_message()`: Dynamically generates system messages based on available tools

### Prompt Management System

The system features a **centralized prompt management** architecture:

- **Centralized Prompts**: All system messages are managed in `src/prompt.py` for consistency and maintainability
- **Dynamic Generation**: Prompts are generated based on actual available MCP tools at runtime
- **Generic & Adaptable**: Prompts are tool-agnostic and work with any MCP server configuration
- **Clean Format**: Professional, focused prompts without unnecessary decorations
- **Reusable Functions**: Modular prompt generation for different agent types

### Dynamic Tool Discovery

The system features **dynamic tool discovery and system message generation**:

- **Real-time Tool Analysis**: Uses `session.list_tools()` to discover available MCP tools at runtime
- **Automatic Categorization**: Automatically categorizes tools by prefix patterns (jira\_, confluence\_, etc.)
- **Context-Aware Prompts**: Generates system messages based on actual tool availability
- **Universal Compatibility**: Works with any MCP tool types, not just Jira/Confluence
- **Adaptive Workflows**: Agents automatically adapt to different MCP server configurations

This ensures that agents always have up-to-date information about available tools and can provide accurate guidance to users.

- `a_list_tools()`: Lists available MCP tools asynchronously
- `a_run(message)`: Executes agent with given message asynchronously
- `_session_context()`: Context manager for MCP session handling
- `_create_toolkit_and_run()`: Creates specialized agent swarm and orchestrates task execution

### Hand-off Strategy

The system implements intelligent agent hand-offs using AutoGen's swarm capabilities:

- **Condition-based routing**: Agents transition based on task analysis and completion status
- **Fallback mechanisms**: AfterWork handlers ensure proper task completion and coordination
- **Circular coordination**: Agents can collaborate across specialties when tasks require multiple domains

### Supported Connection Types

- **StdioServerParameters**: For command-line MCP servers
- **SSEServerParameters**: For HTTP-based MCP servers with Server-Sent Events

## Usage Examples

The project supports sophisticated multi-agent workflows for:

### 📋 Documentation Management

- **Jira Operations**: Automated ticket creation, status updates, and project management
- **Confluence Operations**: Page creation, content editing, and documentation structuring
- **Cross-platform Integration**: Seamless coordination between Jira and Confluence
- **Dynamic Tool Integration**: Real-time discovery and utilization of available Atlassian tools

### 💻 Software Development

- **Code Generation**: AI-powered code writing with best practices
- **Git Operations**: Automated repository management and PR creation via Gitea
- **Development Workflows**: End-to-end development process automation
- **Adaptive Tool Usage**: Automatically adapts to available development tools

### 🔧 Complex Task Orchestration

- **Multi-step Planning**: Breaking down complex tasks into manageable components
- **Resource Coordination**: Intelligent allocation of specialized agents
- **Error Handling**: Robust fallback mechanisms and error recovery
- **Context-Aware Execution**: System messages generated based on actual tool availability

### 🚀 Enhanced Features (New)

- **Dynamic System Messages**: Auto-generated based on real-time MCP tool discovery
- **Tool Categorization**: Automatic classification of tools (Confluence, Jira, Git, etc.)
- **Adaptive Agent Configuration**: Agents automatically configure based on available tools
- **Dual Execution Modes**: Simple single-agent mode and complex multi-agent swarm mode

### 🎯 Specialized Task Routing

- **Intelligent Routing**: Automatic task classification and agent assignment
- **Context Awareness**: Maintaining context across agent handoffs
- **Collaborative Execution**: Multiple agents working together on complex tasks

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
├── src/                    # Source code modules
│   └── prompt.py          # Centralized prompt management
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

## Usage Modes

The system supports two execution modes:

### 🔧 Simple Mode (`a_run`)

- **Single agent**: Direct tool access without complex routing
- **Fast execution**: Minimal overhead for straightforward tasks
- **Dynamic adaptation**: Automatically discovers and uses available tools
- **Best for**: Simple Confluence/Jira operations, direct tool execution

### 🌊 Swarm Mode (`a_run_swarm`)

- **Multi-agent**: Specialized agents with intelligent routing
- **Advanced coordination**: Complex task decomposition and collaboration
- **Fallback handling**: Robust error recovery and alternative approaches
- **Best for**: Complex workflows, multi-system integration, planning tasks

## Tool Discovery Process

1. **Session Initialization**: Connect to MCP server (Atlassian, Git, etc.)
2. **Dynamic Discovery**: Call `session.list_tools()` to get available tools
3. **Tool Categorization**: Automatically sort tools by type (Confluence, Jira, etc.)
4. **System Message Generation**: Create context-aware instructions for agents
5. **Agent Configuration**: Set up agents with appropriate tool access and expertise
6. **Task Execution**: Route and execute tasks using the most suitable approach
