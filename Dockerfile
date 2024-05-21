FROM python:3.12

RUN apt-get update && apt-get install -y wget curl

WORKDIR /app

COPY ./ /app

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]