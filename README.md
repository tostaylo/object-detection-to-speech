# Object Detection API using Flask and Object Detection Libraries

## Docker (preferred)

### with Docker Compose

```sh
docker-compose up --build
```

### or CLI commands

```sh
# Build
docker build -t object-detection .
# Run
docker run -e PORT=8080 -p 8080:8080 object-detection:latest

```

then visit http://localhost:8080/ in your browser:

## Run & Develop with Local Python Environment (alternative to Docker)

```sh
python3 -m venv venv
source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ python3 webapp.py --port 8080
```

then visit http://localhost:8080/ in your browser:

## Google Cloud Run

```sh
gcloud services enable containerregistry.googleapis.com
docker pull <docker-id>/<image-name>
docker tag <docker-id>/<image-name> gcr.io/<project-id>/<image-name>
docker push gcr.io/<project-id>/<image-name>
```

## Reference

- https://github.com/ultralytics/yolov5
- https://github.com/jzhang533/yolov5-flask
- https://github.com/robmarkcole/yolov5-flask (this repo was forked from here)
- https://github.com/avinassh/pytorch-flask-api-heroku
