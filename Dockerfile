## Necessary for building with linux architecture on M1 Mac
## FROM --platform=linux/amd64 python:3.10-slim

FROM python:3.10-slim

RUN apt-get update

#https://github.com/facebookresearch/detectron2/issues/667
RUN apt-get install ffmpeg libsm6 libxext6 gcc git g++ -y

RUN pip3 install torch

# text to speech library dependency
# https://stackoverflow.com/questions/73873102/running-pyttsx3-espeak-text-to-speech-in-docker-container-creates-awful-sound
RUN apt-get install -y espeak

ENV PYTHONUNBUFFERED True
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 webapp:app