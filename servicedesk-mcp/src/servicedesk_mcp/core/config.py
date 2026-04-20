import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    servicedesk_base_uri: str = os.getenv("SERVICEDESK_BASE_URI", "")
    servicedesk_api_key: str = os.getenv("SERVICEDESK_API_KEY", "")
    mcp_bind_host: str = os.getenv("MCP_BIND_HOST", "0.0.0.0")
    mcp_port: int = int(os.getenv("MCP_PORT", "8000"))
    mcp_env: str = os.getenv("MCP_ENV", "test")
    mcp_log_level: str = os.getenv("MCP_LOG_LEVEL", "INFO")

settings = Settings()
