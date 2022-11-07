FROM python:3.8-slim-buster

RUN apt-get update

#https://github.com/facebookresearch/detectron2/issues/667
RUN apt-get install ffmpeg libsm6 libxext6 gcc git g++ -y

RUN pip3 install torch

# text to speech library dependency
# https://stackoverflow.com/questions/73873102/running-pyttsx3-espeak-text-to-speech-in-docker-container-creates-awful-sound
RUN apt-get install -y espeak

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python3", "webapp.py", "--port=8080"]