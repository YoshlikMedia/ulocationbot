FROM python:3.9

ENV BOT_NAME=$BOT_NAME

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .