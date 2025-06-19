<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

⚠️ **IMPORTANT**: After making any code changes, adding features, or updating functionality, you MUST update .github/copilot-instructions.md to reflect the current project state and capabilities.

# Project Background

This is the **MCP Agents** project - a Model Context Protocol (MCP) agent implementation that enables intelligent automation through LLM-powered agents. The project demonstrates how to create agents using the Model Context Protocol to connect Large Language Models with external tools and services, enabling automated interactions with enterprise systems like Jira ticket management, Confluence documentation, and other MCP-compatible services.

The project focuses on practical MCP agent implementation with support for multiple connection protocols and integration with various external services.

## Project Features

### 🤖 MCP Agent Implementation

- **MCPAgent Class**: Central orchestrator for MCP connections and agent interactions (inherits from Config)
- **Multi-Protocol Support**: STDIO and SSE (Server-Sent Events) connections with automatic parameter compilation
- **AutoGen Integration**: Leverages Microsoft's AutoGen for multi-agent conversations
- **Async/Await Pattern**: Fully asynchronous implementation with context managers for session handling
- **Pydantic Integration**: Fully typed with Pydantic models and computed fields for configuration

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
- **Architecture**: Inherits from Config class for LLM configuration management
- **Supported Protocols**: STDIO and SSE (Server-Sent Events) connections with automatic parameter compilation
- **LLM Integration**: Flexible configuration supporting OpenAI and Azure OpenAI with custom headers
- **Tool Management**: Dynamic tool discovery and execution through MCP sessions
- **Multi-Agent System**: **Simplified two-stage collaborative workflow** with Assistant ↔ Planner → MCP Agent architecture

### Specialized Agent Architecture

The system employs a **simplified two-stage collaborative workflow** with clear role separation:

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
- **Collaboration**: Works directly with Planner in multi-turn conversations (max 4 turns)
- **Workflow Position**: First agent in collaborative pair

#### **Planner Agent (Strategic Planning Specialist)**

- **Role**: Strategic planning specialist working collaboratively with Assistant
- **Responsibilities**:
    - Take the assistant's comprehensive answers and content
    - Incorporate the assistant's content into technical execution plans
    - Map execution steps to available MCP tools
    - Ensure assistant's prepared content is included in the final plan
    - Create step-by-step technical instructions for MCP agent
- **Key Principle**: Assistant provides WHAT content to use, Planner provides HOW to execute it technically
- **Input Information**: Assistant's detailed content plus available tool descriptions
- **Collaboration**: Engages in multi-turn conversation with Assistant (max 4 turns total)
- **Workflow Position**: Second agent in collaborative pair

#### **MCP Agent (Tool Operation Specialist)**

- **Role**: **EXCLUSIVE** external tool operation specialist
- **Expertise**: Direct external tool execution, API operations, system integrations
- **Tools**: **ONLY agent with MCP toolkit registration** - exclusive access to all external tools
- **Input**: Comprehensive execution plan from Assistant-Planner collaboration
- **Capabilities**: Complete independence for all external operations
- **Execution**: Receives detailed plans and executes using available MCP tools (max 2 turns)
- **Terminal Role**: Final execution point - terminates after completing tool operations

### Key Methods

- `get_tool_detail()`: Asynchronously lists available MCP tools with descriptions
- `a_run(message)`: Executes two-stage collaborative workflow using `_create_run()`
- `_session_context()`: Context manager for MCP session handling with automatic initialization
- `_create_run()`: **MAIN ARCHITECTURE** - Creates collaborative two-agent workflow: Assistant ↔ Planner → MCP Agent
- `_compiled_params`: Computed property that automatically compiles server parameters for both STDIO and SSE connections

### Prompt Management System

The system features **direct system message integration** within the main agent definitions:

- **Embedded Prompts**: System messages are directly embedded in agent creation within `main.py`
- **Role-Specific Messages**: Three distinct system messages for Assistant, Planner, and MCP Agent
- **Collaborative Focus**: Prompts emphasize collaboration between Assistant and Planner
- **Language Flexibility**: Agents can work in user's preferred language (e.g., Traditional Chinese)
- **Task-Oriented**: Clear separation of content preparation vs. technical execution responsibilities

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

The system implements intelligent agent hand-offs using AutoGen's conversation capabilities with **simplified two-stage workflow**:

#### **Primary Workflow**

User Request → Assistant ↔ Planner → MCP Agent

#### **Handoff Conditions**

**Assistant ↔ Planner Collaboration**:

- Condition: Multi-turn conversation (up to 4 turns)
- Purpose: Collaborative content preparation and technical planning
- Triggers: Automatic conversation flow between Assistant and Planner until plan is complete

**Planner → MCP Agent**:

- Condition: "Plan is complete and ready for execution"
- Triggers: When collaborative planning between Assistant and Planner is finished
- Final execution by MCP Agent with available tools (max 2 turns)

#### **Simplified Benefits**

- **Enhanced Collaboration**: Assistant and Planner work together to thoroughly understand user requirements
- **Comprehensive Analysis**: Multi-turn conversation ensures detailed requirement analysis and content preparation
- **Tool-Aware Planning**: Plans are created with full knowledge of available MCP tools
- **Efficient Execution**: MCP Agent receives well-analyzed, content-rich, and planned instructions
- **Clear Separation**: Maintains specialist independence while enabling effective collaboration

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
│   ├── __init__.py
│   └── config.py          # LLM configuration management
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

The system uses a **two-stage collaborative workflow** for all tasks:

### 🌊 Two-Stage Collaborative Workflow (`a_run`)

- **Two-agent collaborative workflow**: Assistant ↔ Planner → MCP Agent
- **Collaborative Analysis**: Assistant and Planner work together to understand user requests and prepare comprehensive content
- **Content Preparation**: Assistant provides detailed answers and content that fulfill user requests
- **Technical Planning**: Planner creates execution plans that incorporate assistant's content and map to available MCP tools
- **Plan-driven execution**: Tasks are analyzed, content prepared, planned through collaboration, then executed
- **Specialized tool access**: Only MCP agent has direct toolkit registration
- **Best for**: All types of tasks - from simple operations to complex multi-step workflows
- **Implementation**: Uses `_create_run()` with collaborative assistant-planner workflow

#### **Enhanced Workflow Process**

1. **Assistant-Planner Collaboration**: Assistant and Planner engage in multi-turn conversation (up to 4 turns) to:
    - Understand user requirements thoroughly (Assistant focus)
    - Prepare comprehensive content and answers (Assistant specialization)
    - Map requirements to available MCP tools (Planner focus)
    - Create comprehensive execution plans that include assistant's content (Planner specialization)
2. **MCP Execution**: MCP Agent executes the collaboratively created plan using available tools (max 2 turns)

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
# Two-stage collaborative workflow: Assistant ↔ Planner → MCP Agent

# Step 1: Assistant and Planner collaborate (up to 4 turns)
assistant_plan = await assistant.a_run(
    recipient=planner,
    message=f"""
    Please work together to fulfill this user request:
    User Request: {message}
    Available MCP Tools: {tool_detail}

    Assistant: Please provide comprehensive content/answers that fulfill the user's request.
    Planner: Take the assistant's content and create a detailed technical execution plan.
    """,
    max_turns=4,
)

# Step 2: MCP Agent executes the collaborative plan
result = await mcp_agent.a_run(
    message=f"Original Message:\n{message}\n\nExecution Plan:\n{result_messages}",
    tools=toolkit.tools,
    max_turns=2,
    user_input=False,
)
```

### MCP Server Configurations

The system supports multiple MCP servers with example configurations:

- **Atlassian (mcp-atlassian)**: Jira and Confluence integration
- **Context7 (@upstash/context7-mcp)**: Documentation and knowledge base
- **Codex (codex mcp)**: Code-related operations
- **Gitea (gitea-mcp)**: Git repository management
- **GitHub (SSE-based)**: GitHub integration via Server-Sent Events
- **Playwright (@playwright/mcp)**: Web automation and testing

## Tool Discovery Process

1. **Session Initialization**: Connect to MCP server (Atlassian, Git, etc.)
2. **Dynamic Discovery**: Call `session.list_tools()` to get available tools
3. **Tool Categorization**: Automatically sort tools by type (Confluence, Jira, etc.)
4. **System Message Generation**: Create context-aware instructions for agents
5. **Agent Configuration**: Set up agents with appropriate tool access and expertise
6. **Task Execution**: Route and execute tasks using the most suitable approach

## Prompt System Architecture

### Direct System Message Integration (`main.py`)

The system now uses **direct system message integration** within the main agent definitions, removing the need for a separate prompt management module:

#### **Assistant Agent System Message**

```python
system_message = """You are an Assistant Agent who provides comprehensive answers and content preparation for user requests.

Your responsibilities:
1. Understand the user's question or request thoroughly
2. Provide detailed answers or content that fulfills what the user is asking for
3. If the user asks for explanations (like "說明一下什麼是..."), provide comprehensive explanations
4. Prepare any content, information, or answers that will be needed in the execution
5. Work in the user's language when appropriate
6. Focus on WHAT content/information needs to be provided, not just HOW to do it

You will work with a planner who will use your content and create technical execution plans.
REPLY `TERMINATE` if the request cannot be fulfilled or requires human intervention.
"""
```

#### **Planner Agent System Message**

```python
system_message = """You are a Strategic Planner responsible for creating detailed execution plans.

Your responsibilities:
1. Take the assistant's comprehensive answers and content
2. Incorporate the assistant's content into a technical execution plan
3. Map the execution steps to available MCP tools
4. Ensure the assistant's prepared content is included in the final plan
5. Create step-by-step instructions for the MCP agent

Key principle: The assistant provides WHAT content/information to use,
you provide HOW to execute it technically using the available tools.

You will receive:
- Detailed content and answers from the assistant
- A list of available MCP tools

Create a comprehensive plan that includes both the assistant's content AND
the technical steps for the MCP agent to execute.
REPLY `TERMINATE` if the request cannot be fulfilled or requires human intervention.
"""
```

#### **MCP Agent System Message**

```python
system_message = """
You are an MCP Tool Execution Agent.
You will receive a detailed execution plan from the planner that includes:
- The assistant's prepared content and answers
- A step-by-step technical execution plan using available MCP tools
Follow the execution plan carefully and use the appropriate tools to complete the task.
"""
```

### Design Principles

- **Embedded Integration**: System messages are directly defined within agent creation in `main.py`
- **Role Clarity**: Clear separation of responsibilities between Assistant, Planner, and MCP Agent
- **Collaborative Focus**: Emphasizes collaboration between Assistant and Planner phases
- **Language Flexibility**: Supports multi-language interactions (e.g., Traditional Chinese)
- **Task-Oriented**: Focuses on content preparation vs. technical execution separation
- **Termination Handling**: Built-in TERMINATE conditions for error handling
