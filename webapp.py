import argparse
import io
import base64
from PIL import Image
import torch
from flask import Flask, render_template, request, redirect, jsonify
import json
import os, json

# Custom imports
from datasets import categories
from ml_models.detectron import get_detectron_predictor, get_detectron_prediction
from requests import handle_file


app = Flask(__name__)

#initialize yolo
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True) 
yolo_model.eval()

#initialize detectron
detectron_predictor = get_detectron_predictor()

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")

@app.route('/detectron' , methods = ['POST'])
def predict_detectron():
  file = handle_file(request, redirect)

  img_bytes = file.read()
  img = Image.open(io.BytesIO(img_bytes))

  first_prediction = get_detectron_prediction(detectron_predictor, img, categories)

  return f'Detectron predicted the image contained a {first_prediction}.'


@app.route("/yolo", methods=["POST"])
def predict_yolo():
    file = handle_file(request, redirect)

    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    results = yolo_model([img])
    
    df_json = results.pandas().xyxy[0].to_json(orient="records") 
    prediction_to_text = json.loads(df_json)[0]['name']
  
    return f'Yolo5 predicted the image contained a {prediction_to_text}.'


@app.route("/webcam", methods=["POST"])
def predict_from_webcam():
  base_64_img_json = request.get_json()
  base64_image_str = base_64_img_json[base_64_img_json.find(",")+1:]
  decoded = base64.decodebytes(bytes(base64_image_str, "utf-8"))

  img = Image.open(io.BytesIO(decoded))

  results = yolo_model([img])
    
  df_json = results.pandas().xyxy[0].to_json(orient="records") 
  prediction_to_text = json.loads(df_json)[0]['name']

  return jsonify(f'{prediction_to_text}')


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Flask app exposing ml models")
  parser.add_argument("--port", default=8080, type=int, help="port number")
  args = parser.parse_args()

  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
