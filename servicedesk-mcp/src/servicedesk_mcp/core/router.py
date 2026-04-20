from typing import Any

from servicedesk_mcp.families import requests as requests_family
from servicedesk_mcp.families import notes as notes_family
from servicedesk_mcp.families import worklogs as worklogs_family
from servicedesk_mcp.families import tasks as tasks_family
from servicedesk_mcp.families import technicians as technicians_family
from servicedesk_mcp.families import users_requesters as users_requesters_family
from servicedesk_mcp.families import departments_groups_sites as departments_groups_sites_family
from servicedesk_mcp.families import assets as assets_family
from servicedesk_mcp.families import cmdb as cmdb_family
from servicedesk_mcp.families import contracts as contracts_family
from servicedesk_mcp.families import purchase as purchase_family
from servicedesk_mcp.families import problems as problems_family
from servicedesk_mcp.families import changes as changes_family
from servicedesk_mcp.families import projects as projects_family
from servicedesk_mcp.families import solutions as solutions_family
from servicedesk_mcp.families import catalog as catalog_family
from servicedesk_mcp.families import admin as admin_family

TOOL_REGISTRY = {
    # Requests
    "list_requests": requests_family.list_requests,
    "get_request": requests_family.get_request,
    "create_request": requests_family.create_request,
    "update_request": requests_family.update_request,
    "search_requests": requests_family.search_requests,
    "get_my_open_requests": requests_family.get_my_open_requests,
    "search_requests_by_subject": requests_family.search_requests_by_subject,
    "search_requests_by_requester": requests_family.search_requests_by_requester,

    # Notes
    "list_request_notes": notes_family.list_request_notes,
    "add_request_note": notes_family.add_request_note,

    # Worklogs
    "list_request_worklogs": worklogs_family.list_request_worklogs,
    "add_request_worklog": worklogs_family.add_request_worklog,

    # Tasks
    "list_request_tasks": tasks_family.list_request_tasks,
    "add_request_task": tasks_family.add_request_task,
    "update_request_task": tasks_family.update_request_task,

    # Technicians
    "list_technicians": technicians_family.list_technicians,
    "get_technician": technicians_family.get_technician,

    # Users / Requesters
    "list_requesters": users_requesters_family.list_requesters,
    "get_requester": users_requesters_family.get_requester,
    "search_requesters": users_requesters_family.search_requesters,

    # Departments / Groups / Sites
    "list_departments": departments_groups_sites_family.list_departments,
    "list_groups": departments_groups_sites_family.list_groups,
    "list_sites": departments_groups_sites_family.list_sites,
    "get_site": departments_groups_sites_family.get_site,

    # Assets
    "list_assets": assets_family.list_assets,
    "get_asset": assets_family.get_asset,
    "search_assets": assets_family.search_assets,

    # CMDB
    "list_cis": cmdb_family.list_cis,
    "get_ci": cmdb_family.get_ci,
    "search_cis": cmdb_family.search_cis,

    # Contracts
    "list_contracts": contracts_family.list_contracts,
    "get_contract": contracts_family.get_contract,

    # Purchase
    "list_purchase_orders": purchase_family.list_purchase_orders,
    "get_purchase_order": purchase_family.get_purchase_order,

    # Problems
    "list_problems": problems_family.list_problems,
    "get_problem": problems_family.get_problem,

    # Changes
    "list_changes": changes_family.list_changes,
    "get_change": changes_family.get_change,

    # Projects
    "list_projects": projects_family.list_projects,
    "get_project": projects_family.get_project,

    # Solutions
    "list_solutions": solutions_family.list_solutions,
    "get_solution": solutions_family.get_solution,
    "search_solutions": solutions_family.search_solutions,

    # Catalog
    "list_service_templates": catalog_family.list_service_templates,
    "get_service_template": catalog_family.get_service_template,

    # Admin
    "list_priorities": admin_family.list_priorities,
    "list_statuses": admin_family.list_statuses,
    "list_templates": admin_family.list_templates,
}

def list_tools() -> dict[str, list[str]]:
    return {
        "requests": requests_family.register_tools(),
        "notes": notes_family.register_tools(),
        "worklogs": worklogs_family.register_tools(),
        "tasks": tasks_family.register_tools(),
        "technicians": technicians_family.register_tools(),
        "users_requesters": users_requesters_family.register_tools(),
        "departments_groups_sites": departments_groups_sites_family.register_tools(),
        "assets": assets_family.register_tools(),
        "cmdb": cmdb_family.register_tools(),
        "contracts": contracts_family.register_tools(),
        "purchase": purchase_family.register_tools(),
        "problems": problems_family.register_tools(),
        "changes": changes_family.register_tools(),
        "projects": projects_family.register_tools(),
        "solutions": solutions_family.register_tools(),
        "catalog": catalog_family.register_tools(),
        "admin": admin_family.register_tools(),
    }

async def call_tool(tool_name: str, arguments: dict[str, Any] | None = None) -> Any:
    args = arguments or {}

    if tool_name not in TOOL_REGISTRY:
        return {
            "ok": False,
            "error": f"Unknown tool: {tool_name}",
            "available_tools": sorted(TOOL_REGISTRY.keys()),
        }

    handler = TOOL_REGISTRY[tool_name]
    return await handler(**args)
