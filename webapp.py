import argparse
import io
import base64
from PIL import Image
import torch
from flask import Flask, render_template, request, redirect, jsonify
import json
import numpy as np
import os, cv2, json

# Text to Speech
import pyttsx3

# Detectron
import detectron2
from detectron2.utils.logger import setup_logger

# Custom imports
from coco_classes import categories
from detectron_init import get_detectron_predictor
from helpers import handle_file, print_versions


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")

@app.route('/detectron' , methods = ['POST'])
def predict_detectron():
  file = handle_file(request, redirect)

  img_bytes = file.read()
  img = Image.open(io.BytesIO(img_bytes))

  image_directory = 'temp_images'
  image_path = f'{image_directory}/image.jpg'
  isDirectory = os.path.exists(image_directory)
  
  if (not isDirectory):
    os.mkdir(image_directory)

  img.save(image_path)
  im = cv2.imread(image_path)

  outputs = detectron_predictor(im)
  
  prediction_classes = outputs['instances'].pred_classes.cpu().tolist()
  predicted_categories = list(map(lambda category_id: categories[category_id + 1], prediction_classes  ))
  first_prediction = predicted_categories[0]

  speech_engine = pyttsx3.init()
  speech_engine.save_to_file(first_prediction, 'detectron-prediction.mp3')
  speech_engine.runAndWait()

  return f'Detectron predicted the image contained a {first_prediction}. There was a .mp3 file created from the result.'


@app.route("/yolo", methods=["POST"])
def predict_yolo():
    file = handle_file(request, redirect)

    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    results = yolo_model([img])
    
    df_json = results.pandas().xyxy[0].to_json(orient="records") 
    prediction_to_text = json.loads(df_json)[0]['name']
  
    speech_engine = pyttsx3.init()
    speech_engine.save_to_file(prediction_to_text, 'yolo5-prediction.mp3')
    speech_engine.runAndWait()
  
    return f'Yolo5 predicted the image contained a {prediction_to_text}. There was a .mp3 file created from the result.'


@app.route("/webcam", methods=["POST"])
def predict_from_webcam():
  base_64_img_json = request.get_json()
  base64_image_str = base_64_img_json[base_64_img_json.find(",")+1:]
  decoded = base64.decodebytes(bytes(base64_image_str, "utf-8"))

  img = Image.open(io.BytesIO(decoded))

  results = yolo_model([img])
    
  df_json = results.pandas().xyxy[0].to_json(orient="records") 
  prediction_to_text = json.loads(df_json)[0]['name']

  print(prediction_to_text)
  return jsonify(f'{prediction_to_text}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8080, type=int, help="port number")
    args = parser.parse_args()

    print_versions(torch, detectron2)

    setup_logger()

    #initialize yolo
    yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # force_reload = recache latest code
    yolo_model.eval()

    #initialize detectron
    detectron_predictor = get_detectron_predictor()
  
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
