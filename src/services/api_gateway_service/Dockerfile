FROM python:3.10-slim

WORKDIR /app

# Install Python deps first for layer caching
COPY services/api_gateway_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy shared common library and gateway source
COPY common/ /app/common/
COPY services/api_gateway_service/ /app/gateway/

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
