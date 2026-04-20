FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

ENV PYTHONPATH=/app/src
ENV MCP_BIND_HOST=0.0.0.0
ENV MCP_PORT=8000

CMD ["python", "-m", "uvicorn", "servicedesk_mcp.app:app", "--host", "0.0.0.0", "--port", "8000"]
