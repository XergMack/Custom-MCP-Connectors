import httpx
from servicedesk_mcp.core.config import settings

class ServiceDeskClient:
    def __init__(self) -> None:
        self.base_uri = settings.servicedesk_base_uri.rstrip("/")
        self.headers = {
            "TECHNICIAN_KEY": settings.servicedesk_api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def build_url(self, path: str) -> str:
        return f"{self.base_uri}/{path.lstrip('/')}"

    async def get(self, path: str, params: dict | None = None):
        async with httpx.AsyncClient(timeout=60) as client:
            return await client.get(self.build_url(path), headers=self.headers, params=params)

    async def post(self, path: str, json_body: dict):
        async with httpx.AsyncClient(timeout=60) as client:
            return await client.post(self.build_url(path), headers=self.headers, json=json_body)

    async def put(self, path: str, json_body: dict):
        async with httpx.AsyncClient(timeout=60) as client:
            return await client.put(self.build_url(path), headers=self.headers, json=json_body)
