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

The system employs a **simplified three-stage workflow** with clear role separation:

#### **User Interaction Flow**

User → Assistant ↔ Planner → MCP Agent

#### **Assistant Agent (Content Preparation Specialist)**

- **Role**: Content preparation and comprehensive answer specialist
- **Responsibilities**:
    - Thoroughly understand user questions and requests
    - Provide detailed answers or content that fulfills what the user is asking for
    - When users ask for explanations (like "說明一下什麼是..."), provide comprehensive explanations
    - Prepare any content, information, or answers needed for execution
    - Focus on WHAT content/information needs to be provided, not just HOW to do it
    - Work in user's language when appropriate
- **Key Principle**: Provides actual content and answers, not just analysis
- **Collaboration**: Works directly with Planner in multi-turn conversations
- **Workflow Position**: First agent in collaborative pair

#### **Planner Agent (Technical Execution Specialist)**

- **Role**: Technical execution planning specialist working with Assistant
- **Responsibilities**:
    - Take the assistant's comprehensive answers and content
    - Incorporate the assistant's content into technical execution plans
    - Map execution steps to available MCP tools
    - Ensure assistant's prepared content is included in the final plan
    - Create step-by-step technical instructions for MCP agent
- **Key Principle**: Assistant provides WHAT content to use, Planner provides HOW to execute it technically
- **Input Information**: Assistant's detailed content plus available tool descriptions
- **Collaboration**: Engages in multi-turn conversation with Assistant
- **Workflow Position**: Second agent in collaborative pair

#### **MCP Agent (Tool Operation Specialist)**

- **Role**: **EXCLUSIVE** external tool operation specialist
- **Expertise**: Direct external tool execution, API operations, system integrations
- **Tools**: **ONLY agent with MCP toolkit registration** - exclusive access to all external tools
- **Input**: Comprehensive execution plan from Assistant-Planner collaboration
- **Capabilities**: Complete independence for all external operations
- **Terminal Role**: Final execution point - terminates after completing tool operations

### Key Methods

- `a_list_tools()`: Lists available MCP tools asynchronously
- `a_run(message)`: Executes three-agent collaborative workflow using `_create_toolkit_and_run()`
- `run(message)`: Synchronous version of `a_run()`
- `_session_context()`: Context manager for MCP session handling
- `_create_toolkit_and_run()`: **MAIN ARCHITECTURE** - Creates collaborative three-agent workflow: Assistant ↔ Planner → MCP Agent
- `_create_toolkit_and_run_simple()`: Simplified single-agent execution for direct tool usage (legacy/testing)
- `_create_toolkit_and_run_v1()`: Legacy method (currently not used)

### Prompt Management System

The system features a **centralized prompt management** architecture in `src/prompt.py`:

- **Centralized Prompts**: All system messages are managed in `src/prompt.py` for consistency and maintainability
- **Specialized Prompt Functions**: Five main functions for generating role-specific prompts:
    - `get_planner_message(tools)`: Creates strategic planning prompts
    - `get_assistant_message(tools)`: Fallback for general tool-aware prompts
- **Universal & Flexible**: Prompts are completely tool-agnostic and work with any MCP server configuration
- **Architecture-Independent**: No hardcoded agent names or specific tool dependencies
- **Clean Format**: Professional, focused prompts without unnecessary decorations
- **Dynamic Adaptation**: Automatically adapts to available capabilities and tools

### Dynamic Tool Discovery

The system features **dynamic tool discovery and system message generation**:

- **Real-time Tool Analysis**: Uses `session.list_tools()` to discover available tools at runtime
- **Automatic Adaptation**: Automatically adapts to any MCP tool configuration
- **Context-Aware Prompts**: Generates system messages based on actual tool availability
- **Universal Compatibility**: Works with any MCP tool types and server configurations
- **Flexible Workflows**: Agents automatically adapt to different tool ecosystems
- **No Hardcoded Dependencies**: System works regardless of specific tool implementations

This ensures that agents always have up-to-date information about available tools and can provide accurate guidance to users, regardless of the specific MCP server configuration.

### Hand-off Strategy

The system implements intelligent agent hand-offs using AutoGen's swarm capabilities with **simplified three-stage workflow**:

#### **Primary Workflow**

User Request → Planner → Manager → (Code Agent OR MCP Agent)

#### **Handoff Conditions**

**Assistant ↔ Planner Collaboration**:

- Condition: Multi-turn conversation (up to 6 turns)
- Purpose: Collaborative analysis and planning
- Triggers: Automatic conversation flow between Assistant and Planner

**Planner → MCP Agent**:

- Condition: "Plan is complete and ready for execution"
- Triggers: When collaborative planning is finished
- Final execution by MCP Agent with available tools

#### **Secondary Collaboration Flow**

Specialists can collaborate when needed:

**Code Agent Handoffs**:

- "execute this code" → Execution Agent
- "need external tools" → MCP Agent

**Execution Agent Handoffs**:

- "need external tools" → MCP Agent

**MCP Agent**:

- Terminal execution point (no further handoffs)

#### **Simplified Benefits**

- **Enhanced Collaboration**: Assistant and Planner work together to thoroughly understand user requirements
- **Comprehensive Analysis**: Multi-turn conversation ensures detailed requirement analysis
- **Tool-Aware Planning**: Plans are created with full knowledge of available MCP tools
- **Efficient Execution**: MCP Agent receives well-analyzed and planned instructions
- **Clear Separation**: Maintains specialist independence while enabling collaboration

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

- **Three-agent collaborative workflow**: Assistant ↔ Planner → MCP Agent
- **Collaborative Analysis**: Assistant and Planner work together to understand and plan tasks
- **Plan-driven execution**: Tasks are analyzed, planned through collaboration, then executed
- **Specialized tool access**: Only MCP agent has direct toolkit registration
- **Best for**: All types of tasks - from simple operations to complex multi-step workflows
- **Implementation**: Uses `_create_toolkit_and_run()` with collaborative assistant-planner workflow

#### **Enhanced Workflow Process**

1. **Assistant Analysis**: Analyzes user requests and identifies requirements
2. **Collaborative Planning**: Assistant and Planner engage in multi-turn conversation (up to 6 turns) to:
    - Understand user requirements thoroughly
    - Map requirements to available MCP tools
    - Create comprehensive execution plans
3. **MCP Execution**: MCP Agent executes the collaboratively created plan using available tools

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
# Sequential workflow: Planner → Manager → Router → (Development Specialist OR Tool Operation Specialist OR Execution Specialist)

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

# Router determines execution path: Development Specialist, Tool Operation Specialist, or Execution Specialist
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

- **`get_assistant_message(tools)`**: Creates adaptive system messages for general tool access

    - Generates comprehensive tool descriptions and capabilities overview
    - Returns system message with available tool information
    - Used as fallback for general-purpose tool operations

- **`get_planner_message(tools)`**: Creates strategic planning prompts with capability overview

- **`get_router_system_message(tools)`**: Creates task routing prompts with capability-aware routing

### Message Templates

- **`_FALLBACK_MESSAGE`**: Used when no tools are available - generic specialist message
- **`_PLANNER_MESSAGE`**: Template for strategic planning with capability awareness
- **`_MCP_AGENT_MESSAGE`**: Template for tool operation specialists with tool access

### Universal Design Principles

The prompt system is designed to be completely universal and adaptable:

- **Tool-Agnostic**: No hardcoded references to specific tools (Jira, Confluence, etc.)
- **Architecture-Independent**: No fixed agent names or specific workflow dependencies
- **Capability-Driven**: Focuses on capabilities and specializations rather than specific implementations
- **Dynamic Adaptation**: Automatically adapts to any available tool configuration
- **Professional Tone**: Clean, focused prompts without unnecessary decorations or rigid formatting
