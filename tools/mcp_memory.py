from typing import Any
import os
from loguru import logger
from agents.mcp import MCPServerStdio


class MCPLibsqlTools:
    def __init__(self, libsql_url: str) -> None:
        self.libsql_url = libsql_url

    async def list_tools(self) -> dict[str, Any]:
        params = {
            "command": "npx",
            "args": ["-y", "mcp-memory-libsql"],
            "env": {"LIBSQL_URL": self.libsql_url},
        }
        try:
            async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
                tools_desc = await server.list_tools()
                tool_names = []
                if isinstance(tools_desc, dict) and "tools" in tools_desc:
                    tool_names = [t.get("name") for t in tools_desc.get("tools", [])]
                elif isinstance(tools_desc, list):
                    tool_names = [getattr(t, "name", None) for t in tools_desc]
                logger.info("MCP memory tools: {}", tool_names)
                return {"connected": True, "tools": tool_names}
        except Exception as e:
            logger.warning("MCP memory server unavailable: {}", e)
            return {"connected": False, "tools": []} 