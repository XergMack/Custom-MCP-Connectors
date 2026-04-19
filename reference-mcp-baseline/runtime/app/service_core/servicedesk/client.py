from __future__ import annotations

import json
from typing import Any

import requests

from app.service_core.servicedesk.config import ServiceDeskSettings


class ServiceDeskClient:
    def __init__(self, settings: ServiceDeskSettings, api_key: str | None = None):
        self.settings = settings
        self.api_key = settings.resolve_api_key(api_key)

    def _build_url(self, relative_path: str) -> str:
        base = self.settings.base_uri.rstrip("/")
        rel = relative_path.lstrip("/")
        return f"{base}/{rel}"

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/vnd.manageengine.sdp.v3+json",
            "Content-Type": "application/x-www-form-urlencoded",
            "authtoken": self.api_key,
        }

    def _request(
        self,
        method: str,
        relative_path: str,
        input_data: dict[str, Any] | None = None,
    ) -> Any:
        url = self._build_url(relative_path)

        kwargs: dict[str, Any] = {
            "method": method.upper(),
            "url": url,
            "headers": self._headers(),
            "timeout": 30,
        }

        if method.upper() in {"POST", "PUT"}:
            if input_data is not None:
                kwargs["data"] = {"input_data": json.dumps(input_data, separators=(",", ":"))}
        else:
            if input_data is not None:
                kwargs["params"] = {"input_data": json.dumps(input_data, separators=(",", ":"))}

        response = requests.request(**kwargs)

        if not response.ok:
            raise RuntimeError(
                f"ServiceDesk API request failed. "
                f"Method={method.upper()} Uri={response.request.url} "
                f"StatusCode={response.status_code} Body={response.text}"
            )

        return response.json()

    def get_request(self, request_id: str) -> dict[str, Any]:
        payload = self._request("GET", f"requests/{request_id}")
        if isinstance(payload, dict) and "request" in payload:
            return payload["request"]
        return payload

    def search_requests(self, row_count: int = 25, start_index: int = 1) -> Any:
        payload = self._request(
            "GET",
            "requests",
            input_data={
                "list_info": {
                    "row_count": row_count,
                    "start_index": start_index,
                }
            },
        )
        if isinstance(payload, dict) and "requests" in payload:
            return payload["requests"]
        return payload
