FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pybit requests python-dotenv

CMD ["python", "-u", "monitor.py"]
