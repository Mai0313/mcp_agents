import os
from typing import Any
import asyncio
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from mcp import ClientSession, StdioServerParameters
from autogen import LLMConfig, AssistantAgent
from pydantic import BaseModel, ConfigDict, computed_field
from mcp.types import ListToolsResult
from autogen.mcp import create_toolkit
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from autogen.io.run_response import Message


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

    async def _create_toolkit_and_run(self, message: str, session: ClientSession) -> Message:
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

    async def a_run(self, message: str) -> Message:
        async with self._session_context() as session:
            return await self._create_toolkit_and_run(message=message, session=session)

    def list_tools(self) -> ListToolsResult:
        return asyncio.run(self.a_list_tools())

    def run(self, message: str) -> Message:
        return asyncio.run(self.a_run(message=message))


if __name__ == "__main__":
    # message = """
    # 幫我看一下 01. Register and Usage (GAI Service API Repository) 裡面有哪一些端口可以使用
    # """

    message = """
    請幫我在 https://wiki.mediatek.inc/pages/viewpage.action?pageId=1516686162 創建一個新頁面
    這個頁面是 confluence 的 Personal Space 頁面
    說明一下什麼是 Model Context Protocol (MCP)
    並且註明 此文章為 AI 產生，僅供參考
    """

    message = """
    請幫我在 https://wiki.mediatek.inc/pages/viewpage.action?pageId=1516686162 這個頁面新增內容
    這個頁面是 confluence 頁面
    寫 此由 AI 產生，僅供參考
    """

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

    mcp_agent = MCPAgent(model="aide-gpt-4o", params=jira_params)
    asyncio.run(mcp_agent.a_run(message=message))
