# Multi-stage build for optimized image

FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
WORKDIR /app

# Copy dependencies

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy model and code

COPY model.pkl .
COPY app.py .

# Health check

HEALTHCHECK --interval=30s --timeout=3s \
 CMD curl -f http://localhost:8080/health || exit 1

# Run server

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]