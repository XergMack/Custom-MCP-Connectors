FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY amazon_client.py server.py selftest.py ./
RUN python -c "import importlib.metadata as m; import mcp.server.fastmcp as f; assert m.version('mcp') == '1.28.1'; assert f.FastMCP is not None; print('MCP_VERSION=' + m.version('mcp'))" \
    && python -m py_compile amazon_client.py server.py selftest.py \
    && python selftest.py
EXPOSE 8000
CMD ["python", "server.py"]
