# De-scope Forge and Enable Site/Drive Targeting

This change removes forced Forge path coercion and makes site/drive selection explicit per tool call.

Key changes:
- Added list_sites
- Removed automatic Forge/ prefixing
- Generic Shared Documents/ prefix stripping only
- site_id and drive_id are now optional tool parameters
- env values remain only as fallback defaults
