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

The system employs a multi-agent architecture with specialized roles:

#### **Manager Agent**

- **Role**: Task analysis and routing coordinator
- **Responsibilities**: Analyzes user requests and routes to appropriate specialist agents
- **Routing Logic**: Simplified routing between documentation_agent and code_agent only
- **System Message**: Uses manager-specific system message from `get_manager_system_message()`

#### **Planning Agent**

- **Role**: Strategic planning and task decomposition (currently implemented but not actively used in routing)
- **Responsibilities**: Available for complex task decomposition but not integrated in current routing logic
- **System Message**: Uses the same dynamic system message as other agents

#### **Documentation Agent**

- **Role**: Documentation and content management specialist
- **Expertise**: Jira tickets, Confluence pages, content creation/editing
- **Tools**: Has access to all available MCP tools through toolkit registration
- **System Message**: Auto-generated based on real-time tool discovery

#### **Code Agent**

- **Role**: Software development and technical operations specialist
- **Expertise**: Code writing, development workflows, technical implementation
- **Tools**: Has access to all available MCP tools through toolkit registration
- **System Message**: Auto-generated based on real-time tool discovery

#### **Execution Agent**

- **Role**: Direct MCP tool execution specialist (currently implemented but simplified)
- **Expertise**: Tool execution and operation handling
- **Tools**: Has access to all available MCP tools through toolkit registration
- **System Message**: Auto-generated based on real-time tool discovery

### Key Methods

- `a_list_tools()`: Lists available MCP tools asynchronously
- `a_run(message)`: Executes simplified single-agent workflow using `_create_toolkit_and_run_simple()`
- `a_run_swarm(message)`: Executes multi-agent swarm workflow using `_create_toolkit_and_run()`
- `_session_context()`: Context manager for MCP session handling
- `_create_toolkit_and_run()`: Creates specialized agent swarm with manager-based routing
- `_create_toolkit_and_run_simple()`: Simplified single-agent execution for direct tool usage
- `_create_toolkit_and_run_v1()`: Legacy method (currently not used)

### Prompt Management System

The system features a **centralized prompt management** architecture in `src/prompt.py`:

- **Centralized Prompts**: All system messages are managed in `src/prompt.py` for consistency and maintainability
- **Dynamic Generation**: Two main functions for generating prompts:
    - `generate_dynamic_system_message(tools)`: Creates tool-aware system messages for specialist agents
    - `get_manager_system_message(tools)`: Creates manager-specific routing messages
- **Generic & Adaptable**: Prompts are tool-agnostic and work with any MCP server configuration
- **Clean Format**: Professional, focused prompts without unnecessary decorations
- **Tool Categorization**: Automatically categorizes tools by prefix patterns for better organization

### Dynamic Tool Discovery

The system features **dynamic tool discovery and system message generation**:

- **Real-time Tool Analysis**: Uses `session.list_tools()` to discover available MCP tools at runtime
- **Automatic Categorization**: Automatically categorizes tools by prefix patterns (jira\_, confluence\_, etc.)
- **Context-Aware Prompts**: Generates system messages based on actual tool availability
- **Universal Compatibility**: Works with any MCP tool types, not just Jira/Confluence
- **Adaptive Workflows**: Agents automatically adapt to different MCP server configurations

This ensures that agents always have up-to-date information about available tools and can provide accurate guidance to users.

### Hand-off Strategy

The system implements intelligent agent hand-offs using AutoGen's swarm capabilities with simplified routing:

- **Manager-based routing**: Manager agent analyzes tasks and routes to documentation_agent or code_agent
- **Direct execution**: Specialist agents (documentation and code) execute tasks directly with MCP toolkit access
- **Termination-based completion**: All agents use AfterWork(AfterWorkOption.TERMINATE) for clean task completion
- **Simple coordination**: Current implementation focuses on clear task segregation rather than complex agent collaboration

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
- **Implementation**: Uses `_create_toolkit_and_run_simple()` with a single MCP agent

### 🌊 Swarm Mode (`a_run_swarm`)

- **Multi-agent**: Specialized agents with intelligent routing
- **Advanced coordination**: Complex task decomposition and collaboration
- **Fallback handling**: Robust error recovery and alternative approaches
- **Best for**: Complex workflows, multi-system integration, planning tasks
- **Implementation**: Uses `_create_toolkit_and_run()` with manager-based routing system

## Implementation Details

### Actual Code Structure

The current implementation includes:

- **MCPAgent class**: Main orchestrator with Pydantic model configuration
- **Connection handling**: Both STDIO and SSE server parameter support
- **LLM configuration**: Azure OpenAI with specific API endpoints and headers
- **Session management**: Async context manager for MCP connections
- **Tool discovery**: Real-time tool listing and categorization
- **Agent specialization**: Five distinct agent types with specific roles

### Current Routing Logic

```python
# Manager routes only to documentation_agent or code_agent
register_hand_off(
    agent=manager,
    hand_to=[
        OnCondition(
            target=documentation_agent,
            condition="The task involves Jira tickets, Confluence pages, or documentation management",
        ),
        OnCondition(
            target=code_agent,
            condition="The task involves coding, software development, or Git repository operations",
        ),
        AfterWork(agent=AfterWorkOption.TERMINATE),
    ],
)
```

### MCP Server Configurations

The system supports multiple MCP servers with example configurations:

- **Atlassian (mcp-atlassian)**: Jira and Confluence integration
- **Context7 (@upstash/context7-mcp)**: Documentation and knowledge base
- **Codex (codex mcp)**: Code-related operations
- **Gitea (gitea-mcp)**: Git repository management
- **GitHub (SSE-based)**: GitHub integration via Server-Sent Events

## Tool Discovery Process

1. **Session Initialization**: Connect to MCP server (Atlassian, Git, etc.)
2. **Dynamic Discovery**: Call `session.list_tools()` to get available tools
3. **Tool Categorization**: Automatically sort tools by type (Confluence, Jira, etc.)
4. **System Message Generation**: Create context-aware instructions for agents
5. **Agent Configuration**: Set up agents with appropriate tool access and expertise
6. **Task Execution**: Route and execute tasks using the most suitable approach

## Prompt System Architecture

### Core Prompt Functions (`src/prompt.py`)

- **`generate_dynamic_system_message(tools)`**: Creates adaptive system messages for specialist agents

    - Groups tools by category using prefix patterns
    - Generates detailed tool descriptions (truncated to 120 characters)
    - Returns comprehensive system message with tool categorization

- **`get_manager_system_message(tools)`**: Creates manager-specific routing instructions

    - Extracts tool categories for routing decisions
    - Focuses on task analysis and agent assignment
    - Provides clear routing guidelines for documentation vs code tasks

### Message Templates

- **`_FALLBACK_MESSAGE`**: Used when no tools are available
- **`_MANAGER_MESSAGE`**: Template for manager agent with routing logic
- **`_ASST_MESSAGE`**: Template for specialist agents with tool access

### Tool Categorization Logic

The system automatically categorizes tools by extracting prefixes from tool names:

- Tools like `jira_create_ticket` → "Jira" category
- Tools like `confluence_create_page` → "Confluence" category
- Generic tools without prefixes → "General" category
