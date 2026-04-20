$env:PYTHONPATH = ".\src"
python -m uvicorn servicedesk_mcp.app:app --host 0.0.0.0 --port 8000 --reload
