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

The system employs a **complete sequential multi-agent workflow** with six specialized roles:

#### **Planner Agent**

- **Role**: Strategic planning and task decomposition specialist
- **Responsibilities**: Analyzes user requests and creates detailed execution plans with step-by-step instructions
- **Workflow Position**: First agent in the chain (receives user input)
- **Output**: Comprehensive execution plan with objectives, steps, resources, expected outcomes, and considerations
- **System Message**: Uses planner-specific system message from `get_planner_system_message()`
- **Termination**: Ends with "Plan is complete and ready for review"

#### **Manager Agent**

- **Role**: Plan review and approval coordinator
- **Responsibilities**: Reviews planner's execution plans and makes approval decisions
- **Workflow Position**: Second agent in the chain (reviews planner output)
- **Decision Logic**: Approves good plans ("The plan is approved"), requests revisions ("The plan needs revision"), or rejects unfeasible requests
- **System Message**: Uses manager-specific system message from `get_manager_system_message()`

#### **Router Agent**

- **Role**: Execution path determination specialist
- **Responsibilities**: Routes approved plans to appropriate execution agents based on task characteristics
- **Workflow Position**: Third agent in the chain (routes approved plans)
- **Routing Logic**: Routes to code_agent ("This task requires coding"), mcp_agent ("This task requires tools"), or execution_agent ("This task requires execution")
- **System Message**: Uses router-specific system message from `get_router_system_message()`

#### **Code Agent**

- **Role**: Software development and technical implementation specialist
- **Expertise**: Code writing, development workflows, technical implementation
- **Tools**: **NO direct MCP access** - focuses on code creation and technical design
- **Collaboration**: Can hand off to execution_agent for code execution or mcp_agent for tool operations
- **System Message**: Uses code-specific system message from `get_code_agent_system_message()`

#### **Execution Agent**

- **Role**: Code execution and testing specialist
- **Expertise**: Running code, executing scripts, testing programs, performance monitoring
- **Tools**: **NO direct MCP access** - focuses on code execution and testing
- **Responsibilities**: Executes code written by code_agent, runs tests, handles runtime debugging
- **System Message**: Uses execution-specific system message from `get_execution_agent_system_message()`

#### **MCP Agent**

- **Role**: **EXCLUSIVE** MCP tool execution specialist
- **Expertise**: Direct MCP tool execution, API operations, external system interactions
- **Tools**: **ONLY agent with MCP toolkit registration** - has exclusive access to all MCP tools
- **Responsibilities**: Executes all MCP tool operations (Jira, Confluence, Git, etc.), data manipulation, external system interactions
- **System Message**: Uses MCP-specific system message from `get_mcp_agent_system_message()`

### Key Methods

- `a_list_tools()`: Lists available MCP tools asynchronously
- `a_run(message)`: Executes multi-agent swarm workflow using `_create_toolkit_and_run()`
- `run(message)`: Synchronous version of `a_run()`
- `_session_context()`: Context manager for MCP session handling
- `_create_toolkit_and_run()`: **MAIN ARCHITECTURE** - Creates six-agent sequential workflow: Planner → Manager → Router → (Code Agent OR MCP Agent OR Execution Agent)
- `_create_toolkit_and_run_simple()`: Simplified single-agent execution for direct tool usage (legacy/testing)
- `_create_toolkit_and_run_v1()`: Legacy method (currently not used)

### Prompt Management System

The system features a **centralized prompt management** architecture in `src/prompt.py`:

- **Centralized Prompts**: All system messages are managed in `src/prompt.py` for consistency and maintainability
- **Specialized Prompt Functions**: Seven main functions for generating role-specific prompts:
    - `get_planner_system_message(tools)`: Creates strategic planning prompts
    - `get_manager_system_message(tools)`: Creates plan review and approval prompts
    - `get_router_system_message(tools)`: Creates task routing prompts
    - `get_code_agent_system_message(tools)`: Creates software development prompts
    - `get_execution_agent_system_message(tools)`: Creates code execution prompts
    - `get_mcp_agent_system_message(tools)`: Creates MCP tool operation prompts
    - `generate_dynamic_system_message(tools)`: Fallback for general tool-aware prompts
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

The system implements intelligent agent hand-offs using AutoGen's swarm capabilities with **sequential workflow**:

- **Sequential Planning Flow**: User → Planner → Manager → Router → (Code Agent OR MCP Agent OR Execution Agent)
- **Plan-Driven Execution**: Tasks are first planned, reviewed, approved, then routed for execution
- **Specialized Tool Access**: Only mcp_agent has direct MCP toolkit registration
- **Cross-Agent Collaboration**: Code agents can hand off to execution agents for code execution or mcp_agent for tool operations
- **Termination-based completion**: All agents use AfterWork(AfterWorkOption.TERMINATE) for clean task completion
- **Intelligent Routing**: Router agent makes informed decisions based on task characteristics

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

## Usage

The system uses a **multi-agent sequential workflow** for all tasks:

### 🌊 Multi-Agent Workflow (`a_run` / `run`)

- **Six-agent sequential flow**: Planner → Manager → Router → (Code Agent OR MCP Agent OR Execution Agent)
- **Plan-driven execution**: Tasks are first planned, reviewed, approved, then routed for execution
- **Specialized tool access**: Only mcp_agent has direct MCP toolkit registration
- **Cross-agent collaboration**: Code agents can hand off to execution agents for code execution or mcp_agent for tool operations
- **Best for**: All types of tasks - from simple operations to complex multi-step workflows
- **Implementation**: Uses `_create_toolkit_and_run()` with planner-based sequential workflow

### 🔧 Legacy Simple Mode (Available but not default)

- **Single agent**: Direct tool access via `_create_toolkit_and_run_simple()`
- **Fast execution**: Minimal overhead for testing or debugging
- **Note**: This mode is available for legacy compatibility but not used by default

## Implementation Details

### Actual Code Structure

The current implementation includes:

- **MCPAgent class**: Main orchestrator with Pydantic model configuration
- **Connection handling**: Both STDIO and SSE server parameter support
- **LLM configuration**: Azure OpenAI with specific API endpoints and headers
- **Session management**: Async context manager for MCP connections
- **Tool discovery**: Real-time tool listing and categorization
- **Agent specialization**: Six distinct agent types with specific roles

### Current Routing Logic

```python
# Sequential workflow: Planner → Manager → Router → (Code Agent OR MCP Agent OR Execution Agent)

# Planner creates plan and hands to manager
register_hand_off(
    agent=planner,
    hand_to=[
        OnCondition(target=manager, condition="Plan is complete and ready for review"),
        AfterWork(agent=AfterWorkOption.TERMINATE),
    ],
)

# Manager reviews plan and routes to router if approved
register_hand_off(
    agent=manager,
    hand_to=[
        OnCondition(target=router_agent, condition="The plan is approved"),
        OnCondition(target=planner, condition="The plan needs revision"),
        AfterWork(agent=AfterWorkOption.TERMINATE),
    ],
)

# Router determines execution path: Code Agent, MCP Agent, or Execution Agent
register_hand_off(
    agent=router_agent,
    hand_to=[
        OnCondition(target=code_agent, condition="This task requires coding"),
        OnCondition(target=mcp_agent, condition="This task requires tools"),
        OnCondition(target=execution_agent, condition="This task requires execution"),
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
