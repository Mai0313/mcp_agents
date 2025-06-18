<center>

# MCP Agents

[![python](https://img.shields.io/badge/-Python_3.10_%7C_3.11_%7C_3.12-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![uv](https://img.shields.io/badge/-uv_dependency_management-2C5F2D?logo=python&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![tests](https://github.com/Mai0313/mcp_agents/actions/workflows/test.yml/badge.svg)](https://github.com/Mai0313/mcp_agents/actions/workflows/test.yml)
[![code-quality](https://github.com/Mai0313/mcp_agents/actions/workflows/code-quality-check.yml/badge.svg)](https://github.com/Mai0313/mcp_agents/actions/workflows/code-quality-check.yml)
[![codecov](https://codecov.io/gh/Mai0313/mcp_agents/branch/master/graph/badge.svg)](https://codecov.io/gh/Mai0313/mcp_agents)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/Mai0313/mcp_agents/tree/master?tab=License-1-ov-file)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Mai0313/mcp_agents/pulls)
[![contributors](https://img.shields.io/github/contributors/Mai0313/mcp_agents.svg)](https://github.com/Mai0313/mcp_agents/graphs/contributors)

</center>

🤖 **一個基於模型上下文協議（MCP）的智能代理實現，通過 LLM 驱動的代理實現智能自動化**

本專案展示如何使用模型上下文協議創建代理，將大型語言模型與外部工具和服務連接，實現與 Jira、Confluence、Git 儲存庫等企業系統的自動化交互，以及其他 MCP 兼容服務。

**其他語言版本**: [English](README.md) | [中文](README_cn.md)

## ✨ 功能特色

### 🤖 **多代理 MCP 實現**

- **MCPAgent 類**: MCP 連接和代理交互的中央調度器
- **多協議支援**: STDIO 和 SSE（Server-Sent Events）連接
- **AutoGen 整合**: 使用 Microsoft 的 AutoGen 進行多代理對話
- **異步/等待模式**: 完全異步實現，確保高效操作

### � **MCP 服務器整合**

- **Atlassian 整合**: 通過 `mcp-atlassian` 進行 Jira 和 Confluence 操作
- **Context7**: 通過 `@upstash/context7-mcp` 存取文檔和知識庫
- **Codex**: 通過 `codex mcp` 處理程式碼相關操作
- **Gitea**: 通過 `gitea-mcp` 進行 Git 儲存庫管理
- **GitHub**: 通過 Server-Sent Events 進行整合

### 🎯 **智能代理系統**

- **管理代理**: 任務分析和路由協調器
- **文檔代理**: 專門處理 Jira 票券和 Confluence 頁面
- **程式碼代理**: 軟體開發和技術操作
- **規劃代理**: 策略規劃和任務分解
- **執行代理**: 直接 MCP 工具執行專家

### �️ **開發環境**

- **uv 依賴管理**: 快速、可靠的 Python 套件管理
- **型別提示**: 使用 Pydantic 模型的完整型別註解支援
- **測試框架**: pytest 與覆蓋率報告
- **程式碼品質**: ruff 檢查和格式化
- **文檔**: MkDocs 自動生成

## 🚀 快速開始

### 前置需求

- Python 3.10+
- uv（Python 套件管理器）
- Azure OpenAI 或兼容 LLM 服務的 API 存取權限

### 安裝步驟

1. 複製儲存庫：

    ```bash
    git clone https://github.com/Mai0313/mcp_agents.git
    cd mcp_agents
    ```

2. 安裝依賴：

    ```bash
    make uv-install  # 如果尚未安裝 uv
    uv sync          # 安裝專案依賴
    ```

3. 設定環境變數：

    ```bash
    export API_KEY="your-llm-api-key"
    export BASE_URL="your-llm-base-url"
    export JIRA_PERSONAL_TOKEN="your-jira-token"
    export CONFLUENCE_PERSONAL_TOKEN="your-confluence-token"
    ```

### 基本使用方法

1. **簡單模式** - 直接工具執行：

    ```python
    from main import MCPAgent, StdioServerParameters

    # 配置 MCP 服務器（例如：Atlassian）
    jira_params = StdioServerParameters(
        command="uvx",
        args=["mcp-atlassian==0.11.2"],
        env={
            "JIRA_URL": "https://your-jira-instance",
            "CONFLUENCE_URL": "https://your-confluence-instance",
            "JIRA_PERSONAL_TOKEN": "your-token",
            "CONFLUENCE_PERSONAL_TOKEN": "your-token",
        },
    )

    # 創建並運行代理
    agent = MCPAgent(model="gpt-4", params=jira_params)
    result = agent.run("為錯誤修復創建新的 Jira 票券")
    ```

2. **群體模式** - 多代理協作：

    ```python
    # 使用群體模式處理複雜任務
    result = asyncio.run(agent.a_run("分析專案需求並在 Confluence 中創建文檔"))
    ```

## 📁 專案結構

```
├── .github/
│   ├── workflows/          # CI/CD 工作流程
│   └── copilot-instructions.md  # 詳細技術文檔
├── docker/                 # Docker 配置
├── docs/                   # MkDocs 文檔
├── scripts/                # 自動化腳本
│   ├── gen_docs.py        # 文檔生成
│   └── __init__.py
├── src/                    # 源代碼模組
│   └── prompt.py          # 集中化提示管理
├── main.py                # 主要 MCP Agent 實現
├── pyproject.toml          # 專案配置
├── Makefile               # 開發命令
├── docker-compose.yaml    # 容器編排
└── README.md              # 專案概述
```

## 🎯 使用案例

### 📋 文檔管理

- **Jira 操作**: 自動票券創建、狀態更新、專案管理
- **Confluence 操作**: 頁面創建、內容編輯、文檔結構化
- **跨平台整合**: Jira 和 Confluence 之間的無縫協調
- **動態工具整合**: 實時發現和利用可用工具

### 💻 軟體開發

- **程式碼生成**: 採用最佳實踐的 AI 驅動程式碼撰寫
- **Git 操作**: 自動化儲存庫管理和 PR 創建
- **開發工作流程**: 端到端開發流程自動化
- **適應性工具使用**: 自動適應可用的開發工具

### 🔧 複雜任務編排

- **多步驟規劃**: 將複雜任務分解為可管理的組件
- **資源協調**: 智能分配專業代理
- **錯誤處理**: 強大的容錯機制和錯誤恢復
- **上下文感知執行**: 根據實際工具可用性生成系統消息

## 🛠️ 可用命令

```bash
# 開發
make clean          # 清理自動生成的檔案
make format         # 執行 pre-commit hooks 和格式化
make test           # 執行所有測試
make gen-docs       # 生成文檔

# 依賴管理
make uv-install     # 安裝 uv 依賴管理器
uv add <package>    # 添加生產依賴
uv add <package> --dev  # 添加開發依賴
uv sync            # 安裝所有依賴
```

## 🔧 配置

### 環境變數

- **API_KEY**: LLM API 存取必需
- **BASE_URL**: LLM 服務基本 URL（用於 Azure OpenAI 或兼容服務）
- **JIRA_PERSONAL_TOKEN**: 用於 Jira 整合
- **CONFLUENCE_PERSONAL_TOKEN**: 用於 Confluence 整合
- **GITHUB_TOKEN**: 用於 GitHub 整合（如果使用 GitHub MCP 服務器）

### MCP 服務器配置

系統支援多個 MCP 服務器：

- **Atlassian (mcp-atlassian)**: Jira 和 Confluence 整合
- **Context7 (@upstash/context7-mcp)**: 文檔和知識庫
- **Codex (codex mcp)**: 程式碼相關操作
- **Gitea (gitea-mcp)**: Git 儲存庫管理
- **GitHub (SSE-based)**: 通過 Server-Sent Events 進行 GitHub 整合

## 🚀 執行模式

### 多代理工作流程 (`a_run` / `run`)

- **順序流程**: 規劃器 → 管理器 → 路由器 → (代碼代理 或 MCP代理 或 執行代理)
- **計劃驅動執行**: 任務首先被規劃、審查、批准，然後路由執行
- **專門化工具存取**: 只有 mcp_agent 擁有直接的 MCP 工具包註冊
- **清晰的職責分離**:
    - **代碼代理**: 編寫和設計代碼
    - **執行代理**: 執行和測試代碼
    - **MCP代理**: 處理所有外部工具操作 (Jira, Confluence, Git 等)
- **跨代理協作**: 代理可以根據專業化將任務交接給彼此
- **最適合**: 所有類型的任務 - 從簡單操作到複雜的多步驟工作流程

## 🏗️ 架構

### MCPAgent 類

中央調度器，管理 MCP 連接並協調代理交互，支援 STDIO 和 SSE 協議。

### 多代理系統

- **管理代理**: 分析任務並路由到適當的專家
- **文檔代理**: 處理 Jira 票券和 Confluence 頁面
- **程式碼代理**: 管理軟體開發和 Git 操作
- **規劃代理**: 提供策略規劃和任務分解
- **執行代理**: 直接執行 MCP 工具

### 動態工具發現

系統在運行時自動發現可用的 MCP 工具，並生成上下文感知的系統消息以實現最佳代理性能。

## 🤝 貢獻

我們歡迎貢獻！請隨時：

- 開啟問題回報錯誤或功能請求
- 提交拉取請求進行改進
- 分享您使用此 MCP 代理系統的經驗
- 添加對新 MCP 服務器的支援

## 📖 文檔

詳細的技術文檔和實現細節，請參閱：

- [Copilot 指引](.github/copilot-instructions.md) - 完整技術文檔
- [生成文檔](https://mai0313.github.io/mcp_agents/) - API 文檔和指南

## 👥 貢獻者

[![Contributors](https://contrib.rocks/image?repo=Mai0313/mcp_agents)](https://github.com/Mai0313/mcp_agents/graphs/contributors)

Made with [contrib.rocks](https://contrib.rocks)

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案。
