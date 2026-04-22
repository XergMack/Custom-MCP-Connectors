from app.core.config import settings
from app.families import requests as requests_family
from app.families import notes as notes_family
from app.families import worklogs as worklogs_family
from app.families import tasks as tasks_family

class Service:
    def health(self):
        return {
            "ok": True,
            "system": "servicedesk",
            "environment": settings.mcp_env,
            "base_uri_present": bool(settings.servicedesk_base_uri),
            "api_key_present": bool(settings.servicedesk_api_key),
        }

    async def list_requests(self, params: dict | None = None):
        return await requests_family.list_requests(params=params)

    async def get_request(self, request_id: str):
        return await requests_family.get_request(request_id=request_id)

    async def create_request(self, payload: dict):
        return await requests_family.create_request(payload=payload)

    async def update_request(self, request_id: str, payload: dict):
        return await requests_family.update_request(request_id=request_id, payload=payload)

    async def create_request_from_context(self, subject: str, description: str, requester_name: str):
        return await requests_family.create_request_from_context(
            subject=subject,
            description=description,
            requester_name=requester_name,
        )

    async def create_request_for_requester_id(self, subject: str, description: str, requester_id: str):
        return await requests_family.create_request_for_requester_id(
            subject=subject,
            description=description,
            requester_id=requester_id,
        )

    async def update_request_status(self, request_id: str, status_id: str):
        return await requests_family.update_request_status(
            request_id=request_id,
            status_id=status_id,
        )

    async def update_request_subject_and_description(self, request_id: str, subject: str, description: str):
        return await requests_family.update_request_subject_and_description(
            request_id=request_id,
            subject=subject,
            description=description,
        )

    async def list_request_notes(self, request_id: str):
        return await notes_family.list_request_notes(request_id=request_id)

    async def add_request_note(self, request_id: str, payload: dict):
        return await notes_family.add_request_note(request_id=request_id, payload=payload)

    async def add_request_note_simple(self, request_id: str, description: str, show_to_requester: bool = False):
        return await notes_family.add_request_note_simple(
            request_id=request_id,
            description=description,
            show_to_requester=show_to_requester,
        )

    async def list_request_worklogs(self, request_id: str):
        return await worklogs_family.list_request_worklogs(request_id=request_id)

    async def add_request_worklog(self, request_id: str, payload: dict):
        return await worklogs_family.add_request_worklog(request_id=request_id, payload=payload)

    async def list_request_tasks(self, request_id: str):
        return await tasks_family.list_request_tasks(request_id=request_id)

    async def add_request_task(self, request_id: str, payload: dict):
        return await tasks_family.add_request_task(request_id=request_id, payload=payload)

    async def update_request_task(self, request_id: str, task_id: str, payload: dict):
        return await tasks_family.update_request_task(request_id=request_id, task_id=task_id, payload=payload)
