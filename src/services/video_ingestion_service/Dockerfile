FROM python:3.10-slim

WORKDIR /app

COPY services/video_ingestion_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY common/ /app/common/
COPY services/video_ingestion_service/ /app/ingestion/

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "ingestion.main"]
