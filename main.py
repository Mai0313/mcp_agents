import os
from typing import Any
import asyncio
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from mcp import ClientSession, StdioServerParameters
from autogen import LLMConfig, ChatResult, AssistantAgent, UserProxyAgent
from pydantic import BaseModel, ConfigDict, computed_field
from mcp.types import ListToolsResult
from autogen.mcp import create_toolkit
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from autogen.io.run_response import Message
from autogen.agentchat.contrib.swarm_agent import (
    AfterWork,
    OnCondition,
    AfterWorkOption,
    register_hand_off,
    initiate_swarm_chat,
)

from src.prompt import (
    get_router_system_message,
    get_manager_system_message,
    get_planner_system_message,
    get_mcp_agent_system_message,
    get_code_agent_system_message,
    get_execution_agent_system_message,
)


class SSEServerParameters(BaseModel):
    url: str
    headers: dict[str, Any] = {}
    timeout: int = 30
    sse_read_timeout: int = 60


class MCPAgent(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    model: str
    params: StdioServerParameters | SSEServerParameters | str

    @computed_field
    @property
    def _compiled_params(self) -> StdioServerParameters | SSEServerParameters:
        if isinstance(self.params, (StdioServerParameters, SSEServerParameters)):
            return self.params
        if isinstance(self.params, str):
            return SSEServerParameters(url=self.params)
        raise ValueError("Invalid parameters provided for MCPAgent.")

    @computed_field
    @property
    def llm_config(self) -> LLMConfig:
        llm_config = LLMConfig(
            model=self.model,
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL"),
            api_version="2025-04-01-preview",
            api_type="azure",
            default_headers={"X-User-Id": "srv_dvc_tma001"},
        )
        return llm_config

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

    async def a_list_tools(self) -> ListToolsResult:
        """List available MCP tools."""
        async with self._session_context() as session:
            return await session.list_tools()

    async def _create_toolkit_and_run_v1(self, message: str, session: ClientSession) -> Message:
        # plan_agent = AssistantAgent(name="plan_agent", llm_config=self.llm_config)
        mcp_agent = AssistantAgent(name="mcp_agent", llm_config=self.llm_config)

        toolkit = await create_toolkit(session=session)
        result = await mcp_agent.a_run(
            # recipient=assistant,
            message=message,
            tools=toolkit.tools,
            max_turns=None,
            user_input=False,
        )
        await result.process()
        return await result.messages

    async def _create_toolkit_and_run_simple(
        self, message: str, session: ClientSession
    ) -> ChatResult:
        # plan_agent = AssistantAgent(name="plan_agent", llm_config=self.llm_config)
        mcp_agent = AssistantAgent(name="mcp_agent", llm_config=self.llm_config)

        toolkit = await create_toolkit(session=session)
        result = await mcp_agent.a_run(
            # recipient=assistant,
            message=message,
            tools=toolkit.tools,
            max_turns=10,
            user_input=False,
        )
        await result.process()
        return await result.messages

    async def _create_toolkit_and_run(self, message: str, session: ClientSession) -> ChatResult:
        user = UserProxyAgent(name="User", code_execution_config=False)

        tools_result = await session.list_tools()
        tools = tools_result.tools

        # 1. Planner Agent - Creates execution plans
        planner_message = await get_planner_system_message(tools=tools)
        planner = AssistantAgent(
            name="planner",
            system_message=planner_message,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
        )

        # 2. Manager Agent - Reviews and approves plans
        manager_message = await get_manager_system_message(tools=tools)
        manager = AssistantAgent(
            name="manager",
            system_message=manager_message,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
        )

        # 3. Router Agent - Routes approved plans to appropriate agents
        router_message = await get_router_system_message(tools=tools)
        router_agent = AssistantAgent(
            name="router_agent",
            system_message=router_message,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
        )

        # 4. Code Agent - Handles software development tasks
        code_agent_message = await get_code_agent_system_message()
        code_agent = AssistantAgent(
            name="code_agent",
            system_message=code_agent_message,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
        )

        # 5. Execution Agent - Handles code execution
        execution_agent_message = await get_execution_agent_system_message()
        execution_agent = AssistantAgent(
            name="execution_agent",
            system_message=execution_agent_message,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
        )

        # 6. MCP Agent - Handles MCP tool operations
        mcp_agent_message = await get_mcp_agent_system_message(tools=tools)
        mcp_agent = AssistantAgent(
            name="mcp_agent",
            system_message=mcp_agent_message,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
        )

        # Complete Multi-Agent Workflow: Planner → Manager → Router → (Code/MCP/Execution Agent)

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

        # Code Agent can collaborate with other agents when needed
        register_hand_off(
            agent=code_agent,
            hand_to=[
                OnCondition(target=execution_agent, condition="execute code"),
                OnCondition(target=mcp_agent, condition="use tools"),
                AfterWork(agent=AfterWorkOption.TERMINATE),
            ],
        )

        # Execution Agent can request tool operations from MCP agent
        register_hand_off(
            agent=execution_agent,
            hand_to=[
                OnCondition(target=mcp_agent, condition="need tools"),
                AfterWork(agent=AfterWorkOption.TERMINATE),
            ],
        )

        # MCP Agent handles all tool operations (final execution)
        register_hand_off(agent=mcp_agent, hand_to=[AfterWork(agent=AfterWorkOption.TERMINATE)])

        # Register MCP toolkit ONLY with mcp_agent
        toolkit = await create_toolkit(session=session)
        toolkit.register_for_execution(mcp_agent)

        # Create complete agent list for swarm chat
        all_agents = [planner, manager, router_agent, code_agent, execution_agent, mcp_agent]

        # Start the workflow with planner
        history = initiate_swarm_chat(
            initial_agent=planner,
            agents=all_agents,
            user_agent=user,
            messages=[{"role": "user", "content": message}],
        )
        return history

    async def a_run(self, message: str) -> ChatResult:
        """Execute multi-agent swarm workflow with planner -> manager -> router -> (code/execution) agents"""
        async with self._session_context() as session:
            return await self._create_toolkit_and_run(message=message, session=session)

    def list_tools(self) -> ListToolsResult:
        return asyncio.run(self.a_list_tools())

    def run(self, message: str) -> ChatResult:
        return asyncio.run(self.a_run(message=message))


if __name__ == "__main__":
    # message = """
    # 幫我看一下 01. Register and Usage (GAI Service API Repository) 裡面有哪一些端口可以使用
    # """

    message = """
    請幫我在 https://wiki.mediatek.inc/pages/viewpage.action?pageId=1516686162 這個頁面新增內容
    這個頁面是 confluence 頁面
    說明一下什麼是 Model Context Protocol (MCP)
    並且註明 此文章為 AI 產生，僅供參考
    """

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
            "...",
        ],
    )
    github_params = SSEServerParameters(
        url="https://api.githubcopilot.com/mcp",
        headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
    )
    playwright_params = StdioServerParameters(command="npx", args=["-y", "@playwright/mcp@latest"])

    mcp_agent = MCPAgent(model="aide-gpt-4o", params=jira_params)
    # print(mcp_agent.list_tools())

    # Use the multi-agent workflow
    asyncio.run(mcp_agent.a_run(message=message))
