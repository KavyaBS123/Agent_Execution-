FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml ./
COPY src ./src
COPY migrations ./migrations
COPY entrypoint.sh ./entrypoint.sh

RUN pip install --no-cache-dir -e . && chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "agent_platform.main:app", "--host", "0.0.0.0", "--port", "8000"]
