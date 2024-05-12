FROM python:3.10 AS builder

# Like requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    rabbitmq-server \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
# COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY . .

# EXPOSE 5432 5672

CMD ["python", "endpoint/main.py"]
