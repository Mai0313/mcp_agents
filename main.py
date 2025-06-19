import os
import asyncio

from mcp import StdioServerParameters

from src.mcp_agent import MCPAgent, SSEServerParameters

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

    mcp_agent = MCPAgent(model="aide-gpt-4o", params=jira_params)
    # print(mcp_agent.list_tools())

    # Use the multi-agent workflow
    asyncio.run(mcp_agent.a_run(message=message))
