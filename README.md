# Object Detection API using Flask and Object Detection Libraries

## Run & Develop with Local Python Environment

- `python3 -m venv venv`
- `source venv/bin/activate`
- `(venv) $ pip install -r requirements.txt`
- `(venv) $ python3 webapp.py --port 8080`

then visit http://localhost:8080/ in your browser:

## Tests

An example python script to perform inference using [requests](https://docs.python-requests.org/en/master/) is given in `tests/test_request.py`

## Docker

```sh
# Build
docker build -t object-detection .
# Run
docker run -e PORT=8080 -p 8080:8080 object-detection:latest

```

then visit http://localhost:8080/ in your browser:

## Google Cloud Run

`gcloud services enable containerregistry.googleapis.com`

`docker pull <docker-id>/<image-name>`

`docker tag <docker-id>/<image-name> gcr.io/<project-id>/<image-name>`

`docker push gcr.io/<project-id>/<image-name>`

## Reference

- https://github.com/ultralytics/yolov5
- https://github.com/jzhang533/yolov5-flask
- https://github.com/robmarkcole/yolov5-flask (this repo was forked from here)
- https://github.com/avinassh/pytorch-flask-api-heroku
