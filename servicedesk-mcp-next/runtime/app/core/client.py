import json
import httpx
from app.core.config import settings

class ServiceDeskClient:
    def __init__(self) -> None:
        self.base_uri = settings.servicedesk_base_uri.rstrip("/")
        self.headers = {
            "TECHNICIAN_KEY": settings.servicedesk_api_key,
            "Accept": "application/json",
        }

    def build_url(self, path: str) -> str:
        return f"{self.base_uri}/{path.lstrip('/')}"

    async def get(self, path: str, params: dict | None = None):
        query_params = dict(params or {})
        if "input_data" in query_params and isinstance(query_params["input_data"], dict):
            query_params["input_data"] = json.dumps(query_params["input_data"])

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(
                self.build_url(path),
                headers=self.headers,
                params=query_params,
            )
            response.raise_for_status()
            return response.json()

    async def post(self, path: str, json_body: dict):
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self.build_url(path),
                headers=self.headers,
                data={"input_data": json.dumps(json_body)},
            )
            response.raise_for_status()
            return response.json()

    async def put(self, path: str, json_body: dict):
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.put(
                self.build_url(path),
                headers=self.headers,
                data={"input_data": json.dumps(json_body)},
            )
            response.raise_for_status()
            return response.json()
