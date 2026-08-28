import asyncio
import json
import httpx
from amazon_client import AmazonBusinessClient, AmazonBusinessConfig

TOKEN="TEST_ACCESS_TOKEN_DO_NOT_EXPORT"
SECRET="TEST_CLIENT_SECRET_DO_NOT_EXPORT"
REFRESH="TEST_REFRESH_TOKEN_DO_NOT_EXPORT"

def handler(request: httpx.Request) -> httpx.Response:
    if str(request.url)=="https://api.amazon.com/auth/O2/token":
        body=request.content.decode("utf-8")
        assert SECRET in body and REFRESH in body and "grant_type=refresh_token" in body
        return httpx.Response(200,json={"access_token":TOKEN,"expires_in":3600})
    assert request.headers.get("x-amz-access-token")==TOKEN
    p=request.url.path
    if p.endswith("/orderReports") and "/purchaseOrders/" not in p:
        return httpx.Response(200,json={"ordersReport":[{"orderMetadata":{"orderId":"111-TEST"},"orderStatus":"CLOSED"}],"nextPageToken":"","size":1})
    if p.endswith("/orderLineItemReports"):
        return httpx.Response(200,json={"orderLineItemsReport":[{"orderMetadata":{"orderId":"111-TEST"},"productDetails":{"asin":"B000TEST01","title":"Test Item"},"quantity":2}],"nextPageToken":"","size":1})
    if "/purchaseOrders/" in p:
        return httpx.Response(200,json={"ordersReport":[{"orderMetadata":{"orderId":"111-TEST"},"purchaseOrderNumber":"PO-TEST"}],"nextPageToken":"","size":1})
    if p.endswith("/shipmentReports"):
        return httpx.Response(200,json={"shipmentsReport":[{"orderMetadata":{"orderId":"111-TEST"},"shipmentMetadata":{"shipmentId":"SHIP-TEST"}}],"nextPageToken":"","size":1})
    if p.endswith("/shipmentLineItemReports"):
        return httpx.Response(200,json={"shipmentLineItemsReport":[{"orderMetadata":{"orderId":"111-TEST"},"productDetails":{"asin":"B000TEST01"},"quantity":2}],"nextPageToken":"","size":1})
    assert request.headers.get("x-amz-user-email")=="buyer@example.com"
    if p.endswith("/products/getProductsByAsins"):
        return httpx.Response(200,json={"products":[{"asin":"B000TEST01","title":"Test Item"}],"notFoundAsins":[]})
    if p.endswith("/products"):
        return httpx.Response(200,json={"products":[{"asin":"B000TEST01","title":"Test Item","offers":[{"price":{"currencyCode":"USD","amount":"61.72"}}]}]})
    return httpx.Response(404,json={"errors":[{"code":"NOT_FOUND"}]})

async def main():
    http=httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client=AmazonBusinessClient(AmazonBusinessConfig(client_id="TEST_CLIENT_ID",client_secret=SECRET,refresh_token=REFRESH,user_email="buyer@example.com"),client=http)
    try:
        results=[
            await client.health(),
            await client.order_reports("2026-01-01T00:00:00Z","2026-01-31T23:59:59Z"),
            await client.order_line_items("2026-01-01T00:00:00Z","2026-01-31T23:59:59Z",["111-TEST"]),
            await client.orders_by_purchase_order("PO-TEST"),
            await client.shipment_reports("2026-01-01T00:00:00Z","2026-01-31T23:59:59Z"),
            await client.shipment_line_items("2026-01-01T00:00:00Z","2026-01-31T23:59:59Z"),
            await client.search_products("test"),
            await client.products_by_asins(["B000TEST01"]),
        ]
        assert results[0]["scope"]=="read_only"
        assert results[1]["items"][0]["orderMetadata"]["orderId"]=="111-TEST"
        assert results[2]["items"][0]["productDetails"]["asin"]=="B000TEST01"
        assert results[3]["items"][0]["purchaseOrderNumber"]=="PO-TEST"
        assert results[4]["items"][0]["shipmentMetadata"]["shipmentId"]=="SHIP-TEST"
        assert results[7]["items"][0]["asin"]=="B000TEST01"
        combined=json.dumps(results)
        for forbidden in (TOKEN,SECRET,REFRESH,"TEST_CLIENT_ID"):
            assert forbidden not in combined
        assert all(x.get("raw_secret_values_exported") is False for x in results)
        print("AMAZON_BUSINESS_SELFTEST=PASS")
        print("TOOLS_READ_ONLY=PASS")
        print("SECRET_OUTPUT_SCAN=PASS")
    finally:
        await http.aclose()

if __name__=="__main__": asyncio.run(main())
