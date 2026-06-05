FROM python:3.11-alpine

WORKDIR /app

COPY monitor.py .

RUN pip install --no-cache-dir pybit

CMD ["python", "-u", "monitor.py"]
