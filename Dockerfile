FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py /app/src/main.py

CMD ["python", "/app/src/main.py"]