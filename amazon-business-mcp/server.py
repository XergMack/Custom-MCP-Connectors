from __future__ import annotations

from typing import Any
from mcp.server.fastmcp import FastMCP
from amazon_client import AmazonBusinessClient, AmazonBusinessConfig, AmazonBusinessError

mcp = FastMCP(
    name="CaberLink Amazon Business",
    instructions=("Read-only Amazon Business procurement access. Use bounded order, line-item, shipment, and product reads. No ordering, cancellation, return, payment, or account mutation capability exists."),
    host="0.0.0.0",
    port=8000,
    streamable_http_path="/mcp",
    stateless_http=True,
    json_response=True,
)

async def _client() -> AmazonBusinessClient:
    return AmazonBusinessClient(AmazonBusinessConfig.from_env())

async def _safe(call) -> Any:
    client = await _client()
    try:
        return await call(client)
    except AmazonBusinessError as exc:
        return {"ok": False, "status": "error", "error": str(exc), "raw_secret_values_exported": False}
    finally:
        await client.close()

@mcp.tool()
async def amazon_business_health() -> dict[str, Any]:
    """Verify Login With Amazon authentication readiness without exposing token or credential values."""
    return await _safe(lambda c: c.health())

@mcp.tool()
async def amazon_orders_search(order_start_date: str, order_end_date: str, order_ids: list[str] | None = None, next_page_token: str | None = None) -> dict[str, Any]:
    """Return Amazon Business order reports for an ISO-8601 range no wider than 366 days."""
    return await _safe(lambda c: c.order_reports(order_start_date, order_end_date, order_ids, next_page_token))

@mcp.tool()
async def amazon_order_line_items(order_start_date: str, order_end_date: str, order_ids: list[str] | None = None, next_page_token: str | None = None) -> dict[str, Any]:
    """Return detailed order line-item reports, optionally narrowed to Amazon order IDs."""
    return await _safe(lambda c: c.order_line_items(order_start_date, order_end_date, order_ids, next_page_token))

@mcp.tool()
async def amazon_orders_by_purchase_order(purchase_order_number: str, next_page_token: str | None = None) -> dict[str, Any]:
    """Find Amazon Business orders associated with one buyer purchase-order number."""
    return await _safe(lambda c: c.orders_by_purchase_order(purchase_order_number, next_page_token))

@mcp.tool()
async def amazon_shipments_search(order_start_date: str, order_end_date: str, order_ids: list[str] | None = None, next_page_token: str | None = None) -> dict[str, Any]:
    """Return shipment reports for orders in an ISO-8601 date range."""
    return await _safe(lambda c: c.shipment_reports(order_start_date, order_end_date, order_ids, next_page_token))

@mcp.tool()
async def amazon_shipment_line_items(order_start_date: str, order_end_date: str, order_ids: list[str] | None = None, next_page_token: str | None = None) -> dict[str, Any]:
    """Return detailed shipment line items, including carrier/package/receiving fields when Amazon provides them."""
    return await _safe(lambda c: c.shipment_line_items(order_start_date, order_end_date, order_ids, next_page_token))

@mcp.tool()
async def amazon_products_search(keywords: str, facets: str = "OFFERS", product_region: str = "US", locale: str = "en_US", page_size: int = 10) -> dict[str, Any]:
    """Search Amazon Business products; OFFERS requests current offer/pricing data when authorized."""
    return await _safe(lambda c: c.search_products(keywords, facets=facets, product_region=product_region, locale=locale, page_size=page_size))

@mcp.tool()
async def amazon_products_get(asins: list[str], facets: str = "OFFERS", product_region: str = "US", locale: str = "en_US") -> dict[str, Any]:
    """Retrieve details for up to 30 ASINs, optionally including offer/pricing facets."""
    return await _safe(lambda c: c.products_by_asins(asins, facets=facets, product_region=product_region, locale=locale))

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
