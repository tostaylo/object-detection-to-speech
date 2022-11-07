import argparse
import io
from PIL import Image
import torch
from flask import Flask, render_template, request, redirect
import json
import pyttsx3

# Detectron
import detectron2
# !nvcc --version
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch: ", TORCH_VERSION, "; cuda: ", CUDA_VERSION)
print("detectron2:", detectron2.__version__)

from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, cv2, json


# Custom imports
from coco_classes import categories
from implement_detectron import get_detectron_predictor

app = Flask(__name__)

def handle_file(request):
  if "file" not in request.files:
    return redirect(request.url)
  file = request.files["file"]
  if not file:
      return
  
  return file

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")

@app.route('/detectron' , methods = ['POST'])
def predict_detectron():
  file = handle_file(request)

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

  print(predicted_categories[0])
  speech_engine.save_to_file(predicted_categories[0], 'detectron-prediction.mp3')
  speech_engine.runAndWait()

  return f'Detectron predicted the image contained a {predicted_categories[0]}. There was a .mp3 file created from the result.'


@app.route("/yolo", methods=["POST"])
def predict_yolo():
    file = handle_file(request)

    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    image_directory = 'temp_images'
    image_path = f'{image_directory}/image.jpg'
    isDirectory = os.path.exists(image_directory)
    if (not isDirectory):
      os.mkdir(image_directory)
  
    img.save(image_path)
  
    results = yolo_model([img])

    results.render()  # updates results.imgs with boxes and labels
    # results.save(save_dir="static/")
    
    df_json = results.pandas().xyxy[0].to_json(orient="records") 
    prediction_to_text = json.loads(df_json)[0]['name']
  
    speech_engine.save_to_file(prediction_to_text, 'yolo5-prediction.mp3')
    speech_engine.runAndWait()
  
    return f'Yolo5 predicted the image contained a {prediction_to_text}. There was a .mp3 file created from the result.'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8080, type=int, help="port number")
    args = parser.parse_args()

    #initialize yolo
    yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # force_reload = recache latest code
    yolo_model.eval()

    #initialize detectron
    detectron_predictor = get_detectron_predictor()

    #initalize speech to text
    speech_engine = pyttsx3.init()
  
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
