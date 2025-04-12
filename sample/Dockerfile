FROM python:3.12-slim

RUN apt-get update && apt-get install -y gnupg

WORKDIR /app

COPY test_public.key /tmp/

RUN gpg --import /tmp/test_public.key

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY server.py .

COPY templates /app/templates

CMD ["python", "server.py"]