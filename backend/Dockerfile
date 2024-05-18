FROM python:3.10

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends tree

COPY . ./backend
WORKDIR /backend

CMD ["python", "-u", "main.py"]
# CMD ["python", "-u", "-c", "import os; os.system('tree -L 1')"]
