# CaberLink Amazon Business MCP v1.0.0

Ticket 124261. Parent lifecycle architecture: ServiceDesk 122328.

Read-only MCP backend for CaberLink Amazon Business procurement data.

API scope:
- Reporting API v2025-06-09: orders, order line items, purchase-order lookup, shipments, shipment line items.
- Product Search API v2020-08-26: product search and bulk ASIN detail with OFFERS pricing when authorized.

Explicitly excluded: Ordering API and every purchase, cancellation, return, payment, and account mutation.

Authentication uses Login With Amazon refresh-token exchange. Production credentials must be injected from protected runtime secret references; raw credentials and access tokens must never appear in MCP responses, tickets, source control, or build logs.

Required Amazon roles for the initial connector are Amazon Business Analytics and Business Product Catalog.
