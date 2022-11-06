FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update -y && apt-get install -y gcc

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python3", "webapp.py", "--port=8080"]