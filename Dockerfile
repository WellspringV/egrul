FROM python:3.12

RUN apt-get update && apt-get install -y wget curl

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app

COPY ./ /app

ENTRYPOINT ["python", "main.py"]
