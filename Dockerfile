## Necessary for building with linux architecture on M1 Mac
## FROM --platform=linux/amd64 python:3.10-slim

FROM python:3.10-slim

ENV PYTHONPATH /app
ENV PYTHONUNBUFFERED True

RUN apt-get update
#https://github.com/facebookresearch/detectron2/issues/667
RUN apt-get install ffmpeg libsm6 libxext6 gcc git g++ -y

RUN pip3 install torch

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
ADD . /app

EXPOSE 8080

CMD exec gunicorn --reload --bind :$PORT --workers 1 --threads 8 --timeout 0 webapp:app