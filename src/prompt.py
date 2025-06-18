from typing import Any

from mcp.types import Tool

_FALLBACK_MESSAGE = """You are an MCP Tool Specialist with access to automation tools.
Analyze the user's request and use the available tools to complete their task.
Always execute actual tool calls rather than just describing what you would do.
"""

_MANAGER_MESSAGE = """You are a Task Manager responsible for analyzing user requests and routing them to appropriate specialist agents.

Your responsibilities:
1. Analyze the user's request to understand the task type and requirements
2. Route tasks to the most appropriate specialist agent based on task category:
   - Documentation/Content tasks: Route to documentation_agent
   - Code/Development tasks: Route to code_agent

Available tool categories in the system: {categories_text}

Key routing guidelines:
- For content creation, editing, or information management: Route to documentation_agent
- For software development, coding, or technical implementation: Route to code_agent
- After routing, let the specialist agent handle the task completely

Important: After identifying the task type and routing to the appropriate agent, your job is done.
Do not continue the conversation unless there are additional tasks.
"""

_ASST_MESSAGE = """You are an MCP Tool Specialist with access to various automation tools.

AVAILABLE TOOLS BY CATEGORY:

{tool_categories}

CORE PRINCIPLES:
1. Analyze the user's request to understand what they want to accomplish
2. Identify which tools are most appropriate for the task
3. Execute tools in logical sequence (e.g., get/read before update/create)
4. Handle errors gracefully and suggest alternatives if needed
5. Provide clear feedback on what was accomplished

EXECUTION APPROACH:
- For data retrieval: Use appropriate 'get', 'search', or 'list' tools first
- For modifications: Get current state, then apply changes
- For creation: Gather required information, then create
- Always use actual tool calls rather than describing what you would do

Analyze the user's request and use the most appropriate tools to complete their task.
"""


async def generate_dynamic_system_message(tools: list[Tool] | None) -> str:
    """Generate dynamic system message based on available MCP tools"""
    if not tools:
        return _FALLBACK_MESSAGE

    # Group tools by common patterns
    tool_categories: dict[str, list[Any]] = {}
    for tool in tools:
        # Extract category from tool name pattern
        category = tool.name.split("_")[0].title() if "_" in tool.name else "General"

        if category not in tool_categories:
            tool_categories[category] = []

        tool_categories[category].append({
            "name": tool.name,
            "description": tool.description[:120] + "..."
            if len(tool.description) > 120
            else tool.description,
        })

    # Build dynamic system message
    system_message = "You are an MCP Tool Specialist with access to various automation tools.\nAVAILABLE TOOLS BY CATEGORY:\n"

    # Add tools by category
    tool_categorie_content = ""
    for category, tools_list in tool_categories.items():
        system_message += f"{category.upper()} TOOLS:\n"
        for tool in tools_list:
            tool_categorie_content += f"\n- {tool['name']}: {tool['description']}"

    return _ASST_MESSAGE.format(tool_categories=tool_categorie_content)


async def get_manager_system_message(tools: list[Tool] | None) -> str:
    """Generate manager agent system message"""
    if tools:
        tool_categories = set()
        for tool in tools:
            if "_" in tool.name:
                tool_categories.add(tool.name.split("_")[0].title())
        categories_text = (
            ", ".join(sorted(tool_categories)) if tool_categories else "various tools"
        )
    else:
        categories_text = "various tools"
    return _MANAGER_MESSAGE.format(categories_text=categories_text)
