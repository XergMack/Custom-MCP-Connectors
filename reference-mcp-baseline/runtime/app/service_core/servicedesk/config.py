import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceDeskSettings:
    base_uri: str
    default_api_key: str | None = None

    @staticmethod
    def _normalize_base_uri(base_uri: str | None) -> str:
        value = (base_uri or "https://tickets.caberlink.com/api/v3").strip().rstrip("/")
        if not value.endswith("/api/v3"):
            value = f"{value}/api/v3"
        return value

    @classmethod
    def from_env(cls) -> "ServiceDeskSettings":
        return cls(
            base_uri=cls._normalize_base_uri(os.getenv("SERVICEDESK_BASE_URI")),
            default_api_key=os.getenv("SERVICEDESK_API_KEY"),
        )

    def resolve_api_key(self, override_api_key: str | None) -> str:
        api_key = override_api_key or self.default_api_key
        if not api_key or not api_key.strip():
            raise ValueError("ServiceDesk API key is required.")
        return api_key.strip()
