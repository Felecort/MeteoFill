FROM python:3.10 AS builder

# Like requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    rabbitmq-server \
    tree \
 && rm -rf /var/lib/apt/lists/*
# RUN rabbitmq-plugins enable rabbitmq_management
RUN rabbitmq-plugins enable --offline rabbitmq_management
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

COPY . .

WORKDIR /backend

# EXPOSE 5432 5672

# CMD ["python",  "-c", "import os; print(os.system('tree -L 4'))"]
CMD ["python", "-u", "src/receiver.py"]