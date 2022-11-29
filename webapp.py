import argparse
from flask import Flask, render_template, request, redirect, jsonify
import os

# Custom imports
from datasets import categories
from ml_models.yolo import get_yolo_predictions, get_yolo_model
from ml_models.detectron import get_detectron_predictor, get_detectron_prediction
from helpers.files import handle_file, decode_base64_img
from helpers.images import get_img_from_decoded, get_img_from_file


app = Flask(__name__)


yolo_model = get_yolo_model()
detectron_predictor = get_detectron_predictor()


@app.route('/', methods=['GET'])
def index():
  return render_template("index.html", model={})

@app.route('/detectron' , methods = ['POST'])
def predict_detectron():
  img = get_img_from_file(handle_file(request, redirect))

  prediction_name, confidence = get_detectron_prediction(detectron_predictor, img, categories)

  model = {'img_upload_prediction':{'message': prediction_name, 'predictor': "Detectron2", "confidence": confidence}}

  return render_template("index.html", model=model)

@app.route("/yolo", methods=["POST"])
def predict_yolo():
  img = get_img_from_file(handle_file(request, redirect))

  prediction_name, confidence = get_yolo_predictions(yolo_model, img, 0)

  model = {'img_upload_prediction': {'message': prediction_name, 'predictor': "Yolov5", "confidence": confidence}}
    
  return render_template("index.html", model=model)
  
@app.route("/webcam", methods=["POST"])
def predict_from_webcam():
  decoded = decode_base64_img(request.get_json())
  img = get_img_from_decoded(decoded)

  if request.args.get('inference') == "yolo":
    prediction_name, confidence = get_yolo_predictions(yolo_model, img, 0)
  else:
    prediction_name, confidence = get_detectron_prediction(detectron_predictor, img, categories)


  return jsonify(f'{prediction_name} with confidence of {confidence} percent')



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Flask app exposing ml models")
  parser.add_argument("--port", default=8080, type=int, help="port number")
  args = parser.parse_args()

  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
