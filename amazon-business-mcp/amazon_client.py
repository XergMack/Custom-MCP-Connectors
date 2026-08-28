from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass
from typing import Any, Iterable
from urllib.parse import quote

import httpx


class AmazonBusinessError(RuntimeError):
    pass


@dataclass(frozen=True)
class AmazonBusinessConfig:
    client_id: str
    client_secret: str
    refresh_token: str
    api_base: str = "https://na.business-api.amazon.com"
    token_url: str = "https://api.amazon.com/auth/O2/token"
    user_email: str | None = None
    product_region: str = "US"
    locale: str = "en_US"
    timeout_seconds: float = 30.0
    max_items: int = 100

    @classmethod
    def from_env(cls) -> "AmazonBusinessConfig":
        def required(name: str) -> str:
            value = os.getenv(name, "").strip()
            if not value:
                raise AmazonBusinessError(f"Missing required environment variable: {name}")
            return value
        return cls(
            client_id=required("AMAZON_BUSINESS_CLIENT_ID"),
            client_secret=required("AMAZON_BUSINESS_CLIENT_SECRET"),
            refresh_token=required("AMAZON_BUSINESS_REFRESH_TOKEN"),
            api_base=os.getenv("AMAZON_BUSINESS_API_BASE", "https://na.business-api.amazon.com").rstrip("/"),
            token_url=os.getenv("AMAZON_BUSINESS_TOKEN_URL", "https://api.amazon.com/auth/O2/token"),
            user_email=os.getenv("AMAZON_BUSINESS_USER_EMAIL") or None,
            product_region=os.getenv("AMAZON_BUSINESS_PRODUCT_REGION", "US"),
            locale=os.getenv("AMAZON_BUSINESS_LOCALE", "en_US"),
            timeout_seconds=float(os.getenv("AMAZON_BUSINESS_TIMEOUT_SECONDS", "30")),
            max_items=max(1, min(int(os.getenv("AMAZON_BUSINESS_MAX_ITEMS", "100")), 500)),
        )


class AmazonBusinessClient:
    def __init__(self, config: AmazonBusinessConfig, client: httpx.AsyncClient | None = None):
        self.config = config
        self._client = client or httpx.AsyncClient(timeout=config.timeout_seconds)
        self._owns_client = client is None
        self._access_token: str | None = None
        self._expires_at = 0.0
        self._token_lock = asyncio.Lock()

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def _token(self) -> str:
        now = time.monotonic()
        if self._access_token and now < self._expires_at - 60:
            return self._access_token
        async with self._token_lock:
            now = time.monotonic()
            if self._access_token and now < self._expires_at - 60:
                return self._access_token
            response = await self._client.post(self.config.token_url, data={
                "grant_type": "refresh_token",
                "refresh_token": self.config.refresh_token,
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
            }, headers={"content-type": "application/x-www-form-urlencoded"})
            if response.status_code >= 400:
                raise AmazonBusinessError(f"Amazon LWA token request failed: HTTP {response.status_code}")
            try:
                payload = response.json()
            except ValueError as exc:
                raise AmazonBusinessError("Amazon LWA token response was not JSON") from exc
            token = str(payload.get("access_token") or "")
            if not token:
                raise AmazonBusinessError("Amazon LWA token response did not contain access_token")
            self._access_token = token
            self._expires_at = time.monotonic() + max(int(payload.get("expires_in") or 3600), 120)
            return token

    async def _request(self, method: str, path: str, *, params: dict[str, Any] | None = None, json_body: Any = None, product_user_context: bool = False) -> Any:
        token = await self._token()
        headers = {"accept": "application/json", "x-amz-access-token": token, "user-agent": "CaberLink-Amazon-Business-MCP/1.0.0"}
        if product_user_context:
            if not self.config.user_email:
                raise AmazonBusinessError("AMAZON_BUSINESS_USER_EMAIL is required for Product Search API calls")
            headers["x-amz-user-email"] = self.config.user_email
        response = await self._client.request(method, f"{self.config.api_base}{path}", params=params, json=json_body, headers=headers)
        if response.status_code >= 400:
            request_id = response.headers.get("x-amzn-requestid") or response.headers.get("x-amzn-request-id")
            suffix = f" request_id={request_id}" if request_id else ""
            raise AmazonBusinessError(f"Amazon Business API request failed: HTTP {response.status_code}{suffix}")
        try:
            return response.json()
        except ValueError as exc:
            raise AmazonBusinessError("Amazon Business API response was not JSON") from exc

    @staticmethod
    def _first_list(payload: Any, keys: Iterable[str]) -> list[Any]:
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            for key in keys:
                if isinstance(payload.get(key), list):
                    return payload[key]
        return []

    def _result(self, payload: Any, keys: Iterable[str], limit: int | None = None) -> dict[str, Any]:
        rows = self._first_list(payload, keys)[: limit or self.config.max_items]
        return {
            "items": rows,
            "next_page_token": payload.get("nextPageToken") if isinstance(payload, dict) else None,
            "size": payload.get("size") if isinstance(payload, dict) else len(rows),
            "raw_secret_values_exported": False,
        }

    async def health(self) -> dict[str, Any]:
        await self._token()
        return {"ok": True, "status": "ready", "api_base": self.config.api_base, "reporting_version": "2025-06-09", "product_search_version": "2020-08-26", "scope": "read_only", "product_user_context_configured": bool(self.config.user_email), "raw_secret_values_exported": False}

    async def order_reports(self, order_start_date: str, order_end_date: str, order_ids: list[str] | None = None, next_page_token: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"orderStartDate": order_start_date, "orderEndDate": order_end_date}
        if order_ids: params["orderIds"] = ",".join(order_ids[:30])
        if next_page_token: params["nextPageToken"] = next_page_token
        return self._result(await self._request("GET", "/reports/2025-06-09/orderReports", params=params), ("ordersReport", "orders"))

    async def order_line_items(self, order_start_date: str, order_end_date: str, order_ids: list[str] | None = None, next_page_token: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"orderStartDate": order_start_date, "orderEndDate": order_end_date}
        if order_ids: params["orderIds"] = ",".join(order_ids[:30])
        if next_page_token: params["nextPageToken"] = next_page_token
        return self._result(await self._request("GET", "/reports/2025-06-09/orderLineItemReports", params=params), ("orderLineItemsReport", "orderLineItems"))

    async def orders_by_purchase_order(self, purchase_order_number: str, next_page_token: str | None = None) -> dict[str, Any]:
        params = {"nextPageToken": next_page_token} if next_page_token else None
        path = f"/reports/2025-06-09/purchaseOrders/{quote(purchase_order_number, safe='')}/orderReports"
        return self._result(await self._request("GET", path, params=params), ("ordersReport", "orders"))

    async def shipment_reports(self, order_start_date: str, order_end_date: str, order_ids: list[str] | None = None, next_page_token: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"orderStartDate": order_start_date, "orderEndDate": order_end_date}
        if order_ids: params["orderIds"] = ",".join(order_ids[:30])
        if next_page_token: params["nextPageToken"] = next_page_token
        return self._result(await self._request("GET", "/reports/2025-06-09/shipmentReports", params=params), ("shipmentsReport", "shipments"))

    async def shipment_line_items(self, order_start_date: str, order_end_date: str, order_ids: list[str] | None = None, next_page_token: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"orderStartDate": order_start_date, "orderEndDate": order_end_date}
        if order_ids: params["orderIds"] = ",".join(order_ids[:30])
        if next_page_token: params["nextPageToken"] = next_page_token
        return self._result(await self._request("GET", "/reports/2025-06-09/shipmentLineItemReports", params=params), ("shipmentLineItemsReport", "shipmentLineItems"))

    async def search_products(self, keywords: str, *, facets: str = "OFFERS", product_region: str | None = None, locale: str | None = None, page_size: int = 10) -> dict[str, Any]:
        params = {"keywords": keywords, "productRegion": product_region or self.config.product_region, "locale": locale or self.config.locale, "facets": facets}
        payload = await self._request("GET", "/products/2020-08-26/products", params=params, product_user_context=True)
        return self._result(payload, ("products",), min(max(page_size, 1), 30))

    async def products_by_asins(self, asins: list[str], *, facets: str = "OFFERS", product_region: str | None = None, locale: str | None = None) -> dict[str, Any]:
        clean = [str(x).strip() for x in asins if str(x).strip()][:30]
        if not clean: raise AmazonBusinessError("At least one ASIN is required")
        body = {"productIds": clean, "productRegion": product_region or self.config.product_region, "locale": locale or self.config.locale, "facets": [x.strip() for x in facets.split(",") if x.strip()]}
        payload = await self._request("POST", "/products/2020-08-26/products/getProductsByAsins", json_body=body, product_user_context=True)
        result = self._result(payload, ("products",), 30)
        result["not_found_asins"] = payload.get("notFoundAsins", []) if isinstance(payload, dict) else []
        return result
