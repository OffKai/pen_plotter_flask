# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5000
COPY . .

ENTRYPOINT [ "python", "main.py" ]
CMD [ "--config", "/app/config.yaml"]
