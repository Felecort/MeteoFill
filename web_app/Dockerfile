FROM python:3.10

# Like requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /web_app

EXPOSE 8050

CMD ["python", "-u", "web.py"]
