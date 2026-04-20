# API Family Master Index

| Family | Status | Read | Write | Docs Checked | Live Tested | Notes |
|---|---|---:|---:|---:|---:|---|
| requests | Working | Yes | Yes | Yes | Yes | Core CRUD + deterministic search + create_request_from_context proven |
| notes | Working | Yes | Yes | Partial | Yes | Add note proven |
| worklogs | Working | Yes | Yes | Partial | Yes | Add worklog proven |
| tasks | Working | Yes | Yes | Partial | Yes | Add task proven |
| technicians | Working | Yes | Unknown | Yes | Yes | list_technicians + get_technician proven |
| users-requesters | Working | Yes | Unknown | Yes | Yes | Uses /users, search_requesters proven |
| departments-groups-sites | Working | Yes | Unknown | Yes | Yes | departments + support_groups + sites proven |
| assets | Blocked | No | No | Yes | Yes | /assets returns SDP internal error in this environment |
| cmdb | Blocked | No | No | Yes | Yes | Tested common CI paths; not exposed at tested paths |
| contracts | Working | Yes | Unknown | Partial | Yes | list_contracts proven |
| purchase | License Blocked | No | No | Partial | Yes | purchase_orders blocked by current license |
| problems | Scaffolded | ? | ? | No | No | Placeholder only |
| changes | Scaffolded | ? | ? | No | No | Placeholder only |
| projects | Scaffolded | ? | ? | No | No | Placeholder only |
| solutions | Working | Yes | Unknown | Partial | Yes | list_solutions + search_solutions proven |
| catalog | Working | Yes | No | Yes | Yes | request_templates proven via list_templates |
| admin | Working | Yes | No | Yes | Yes | priorities + statuses + request_templates proven |
