FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV MCP_HOST=0.0.0.0

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

EXPOSE 8000

CMD ["python", "-m", "app.mcp.server"]
