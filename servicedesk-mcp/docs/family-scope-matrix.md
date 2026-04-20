# ServiceDesk MCP Family Scope Matrix

## Purpose
This document defines the read/write family scope for the rebuilt ServiceDesk MCP connector.

The goal is to support broad test-environment coverage first, then tighten scope later for production if needed.

## Matrix

| Family | Read | Write | MVP Now | Later | Notes |
|---|---:|---:|---:|---:|---|
| Requests | Yes | Yes | Yes |  | Core ticketing surface |
| Notes / Comments | Yes | Yes | Yes |  | Needed for work logs / commentary |
| Worklogs | Yes | Yes | Yes |  | Core operational history |
| Tasks | Yes | Yes | Yes |  | Needed for checklist/SOP flow |
| Problems | Yes | Yes | Yes |  | Useful for root-cause workflows |
| Changes | Yes | Yes | Yes |  | Important for controlled change work |
| Releases | Yes | Yes |  | Yes | Valuable but not first-pass essential |
| Projects | Yes | Yes | Yes |  | Useful for structured internal work |
| Assets | Yes | Yes | Yes |  | Core MSP visibility |
| CMDB / CIs | Yes | Yes | Yes |  | Important if you want asset relationships |
| CI Relationships | Yes | Yes |  | Yes | Good later if CMDB is mature |
| Contracts | Yes | Yes | Yes |  | Important for renewals/lifecycle |
| Purchase / PO | Yes | Yes | Yes |  | Important for procurement flow |
| Billing | Yes | Yes |  | Yes | Likely later unless you actively use it there |
| Timesheets | Yes | Yes |  | Yes | Later unless strongly needed now |
| Solutions / Knowledge Base | Yes | Yes | Yes |  | Good for internal knowledge/testing |
| Topics / Categories | Yes | Yes |  | Yes | Reference/admin-heavy |
| Service Catalog / Service Requests | Yes | Yes | Yes |  | Important if templates/catalog are central |
| Customers | Yes | Yes | Yes |  | MSP-relevant |
| Users / Requesters | Yes | Yes | Yes |  | Core directory inside SDP |
| Technicians | Yes | Yes | Yes |  | Important for routing/assignment |
| Departments / Groups / Sites | Yes | Yes | Yes |  | Useful for reference/admin control |
| Admin Reference Data | Yes | Limited | Yes |  | Read broadly; write carefully |
| Announcements | Yes | Yes |  | Yes | Nice to have |
| Space / Campus / Building / Floor / Room | Yes | Yes |  | Yes | Only if you use facilities data |
| Custom Modules | Yes | Yes |  | Yes | Depends on your implementation |

## Recommended rebuilt ServiceDesk MCP scope

### MVP Now
- Requests
- Notes
- Worklogs
- Tasks
- Problems
- Changes
- Projects
- Assets
- CMDB
- Contracts
- Purchase
- Solutions
- Service Catalog / Service Requests
- Customers
- Users / Requesters
- Technicians
- Departments / Groups / Sites
- Admin reference reads

### Later
- Releases
- CI Relationships
- Billing
- Timesheets
- Announcements
- Space / facilities modules
- Custom Modules

## Doctrine
- Build against the V3 API surface
- Full read and full write are desired in test
- Production scope can be narrowed later if needed
- Any excluded family should be an explicit decision, not an accident
