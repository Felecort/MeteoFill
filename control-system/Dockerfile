FROM python:3.10-slim

# Like requirements
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev build-essential

RUN pip install --no-cache-dir -r requirements.txt
# RUN apt-get update && apt-get install -y --no-install-recommends tree

COPY . ./control-system
WORKDIR /control-system

EXPOSE 8092

CMD ["python", "-u", "main.py"]
# CMD ["python", "-u", "-c", "import os; os.system('tree -L 1')"]
