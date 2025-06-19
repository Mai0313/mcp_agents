import os
from typing import Any
import asyncio
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from mcp import ClientSession, StdioServerParameters
from autogen import ChatResult, AssistantAgent
from pydantic import BaseModel, ConfigDict, computed_field
from autogen.mcp import create_toolkit
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from autogen.io.run_response import Message

from src.types.config import Config


class SSEServerParameters(BaseModel):
    url: str
    headers: dict[str, Any] = {}
    timeout: int = 30
    sse_read_timeout: int = 60


class MCPAgent(Config):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    params: StdioServerParameters | SSEServerParameters | str

    @computed_field
    @property
    def _compiled_params(self) -> StdioServerParameters | SSEServerParameters:
        if isinstance(self.params, (StdioServerParameters, SSEServerParameters)):
            return self.params
        if isinstance(self.params, str):
            return SSEServerParameters(url=self.params)
        raise ValueError("Invalid parameters provided for MCPAgent.")

    @asynccontextmanager
    async def _session_context(self) -> AsyncGenerator[ClientSession, None]:
        if isinstance(self._compiled_params, StdioServerParameters):
            async with (
                stdio_client(self._compiled_params) as (read, write),
                ClientSession(read, write) as session,
            ):
                await session.initialize()
                yield session
        elif isinstance(self._compiled_params, SSEServerParameters):
            async with (
                sse_client(**self._compiled_params.model_dump()) as streams,
                ClientSession(*streams) as session,
            ):
                await session.initialize()
                yield session
        else:
            raise ValueError("Invalid parameters provided for MCPAgent.")

    async def get_tool_detail(self) -> str:
        try:
            async with self._session_context() as session:
                tools_result = await session.list_tools()
                tool_detail = ""
                for tool in tools_result.tools:
                    tool_detail += f"\n- `{tool.name}`:\n{tool.description}"
        except Exception:
            tool_detail = "No tools available or an error occurred while fetching tool details."
        return tool_detail

    async def _create_simple_toolkit_and_run(
        self, message: str, session: ClientSession
    ) -> Message:
        # Ref: https://docs.ag2.ai/0.9.3/docs/user-guide/advanced-concepts/tools/mcp/client/
        # Create a toolkit with available MCP tools
        toolkit = await create_toolkit(session=session)
        agent = AssistantAgent(name="assistant", llm_config=self.llm_config)
        # Register MCP tools with the agent
        toolkit.register_for_llm(agent)

        # Make a request using the MCP tool
        result = await agent.a_run(
            message=message, tools=toolkit.tools, max_turns=2, user_input=False
        )
        await result.process()
        return await result.messages

    async def _create_toolkit_and_run(self, message: str, session: ClientSession) -> Message:
        assistant = AssistantAgent(
            name="assistant",
            system_message="""You are an Assistant Agent who provides comprehensive answers and content preparation for user requests.

            Your responsibilities:
            1. Understand the user's question or request thoroughly
            2. Provide detailed answers or content that fulfills what the user is asking for
            3. If the user asks for explanations (like "說明一下什麼是..."), provide comprehensive explanations
            4. Prepare any content, information, or answers that will be needed in the execution
            5. Work in the user's language when appropriate
            6. Focus on WHAT content/information needs to be provided, not just HOW to do it

            Example: If user asks to "add explanation of MCP to a page", you should:
            - Provide a detailed explanation of what MCP is
            - Suggest the content format and structure
            - Include any disclaimers or notes requested

            You will work with a planner who will use your content and create technical execution plans.
            REPLY `TERMINATE` if the request cannot be fulfilled or requires human intervention.
            """,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            is_termination_msg=lambda x: "TERMINATE" in x.get("content"),
        )

        planner = AssistantAgent(
            name="planner",
            system_message="""You are a Strategic Planner responsible for creating detailed execution plans.

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
            """,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            is_termination_msg=lambda x: "TERMINATE" in x.get("content"),
        )

        # Get available tools information
        tool_detail = await self.get_tool_detail()

        # Step 1: Assistant analyzes the user's request
        assistant_plan = await assistant.a_run(
            recipient=planner,
            message=f"""
            Please work together to fulfill this user request:

            User Request: {message}

            Available MCP Tools:
            {tool_detail}

            Assistant: Please provide comprehensive content/answers that fulfill the user's request.
            If they ask for explanations, provide detailed explanations.
            If they need specific content, prepare that content.

            Planner: Take the assistant's content and create a detailed technical execution plan
            that includes the assistant's prepared content and uses the available tools.
            """,
            max_turns=4,
        )
        await assistant_plan.process()
        result_messages = await assistant_plan.messages

        # Step 2: Execute the plan with MCP agent
        mcp_agent = AssistantAgent(
            name="mcp_agent",
            system_message="""
            You are an MCP Tool Execution Agent.
            You will receive a detailed execution plan from the planner that includes:
            - The assistant's prepared content and answers
            - A step-by-step technical execution plan using available MCP tools
            Follow the execution plan carefully and use the appropriate tools to complete the task.
            """,
            llm_config=self.llm_config,
        )

        toolkit = await create_toolkit(session=session)
        result = await mcp_agent.a_run(
            message=f"Original Message:\n{message}\n\nExecution Plan:\n{result_messages}",
            tools=toolkit.tools,
            max_turns=3,
            user_input=False,
        )
        await result.process()
        return await result.messages

    async def a_list_tools(self) -> str:
        async with self._session_context() as session:
            available_tools = "Available tools:\n"
            tools_result = await session.list_tools()
            for tool in tools_result.tools:
                available_tools += f"- `{tool.name}`: {tool.description}\n"
            return available_tools

    async def a_run(self, message: str) -> ChatResult:
        async with self._session_context() as session:
            return await self._create_simple_toolkit_and_run(message=message, session=session)


if __name__ == "__main__":
    message = """
    幫我看一下 01. Register and Usage (GAI Service API Repository) 裡面有哪一些端口可以使用
    """

    # message = """
    # 請幫我在 https://wiki.mediatek.inc/pages/viewpage.action?pageId=1516686162 這個頁面新增內容
    # 這個頁面是 confluence 頁面
    # 說明一下什麼是 Model Context Protocol (MCP)
    # 並且註明 此文章為 AI 產生，僅供參考
    # """

    # message = """幫我查看一下我現在有哪一些repository"""

    # message = """幫我寫一個 snake game in python, 並存成 snake.py"""

    jira_params = StdioServerParameters(
        command="uvx",
        args=["mcp-atlassian==0.11.2"],
        env={
            "JIRA_URL": "https://mtkjira",
            "CONFLUENCE_URL": "https://wiki.mediatek.inc",
            "JIRA_PERSONAL_TOKEN": os.getenv("JIRA_PERSONAL_TOKEN"),
            "CONFLUENCE_PERSONAL_TOKEN": os.getenv("CONFLUENCE_PERSONAL_TOKEN"),
            "JIRA_SSL_VERIFY": "false",
            "CONFLUENCE_SSL_VERIFY": "false",
            "READ_ONLY_MODE": "false",
        },
    )
    context7_params = StdioServerParameters(command="npx", args=["-y", "@upstash/context7-mcp"])
    codex_params = StdioServerParameters(command="codex", args=["mcp"])
    gitea_params = StdioServerParameters(
        command="gitea-mcp",
        args=[
            "-t",
            "stdio",
            "--insecure",
            "--host",
            "https://gitea.mediatek.inc",
            "--token",
            f"{os.getenv('GITEA_TOKEN')}",
        ],
    )
    github_params = SSEServerParameters(
        url="https://api.githubcopilot.com/mcp",
        headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
    )
    playwright_params = StdioServerParameters(command="npx", args=["-y", "@playwright/mcp@latest"])

    mcp_agent = MCPAgent(model="aide-gpt-4o", params=gitea_params)
    # tools = asyncio.run(mcp_agent.a_list_tools())
    # print(tools)

    # Use the multi-agent workflow
    asyncio.run(mcp_agent.a_run(message=message))
