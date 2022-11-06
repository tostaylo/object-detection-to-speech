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

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
# from detectron2.utils.visualizer import Visualizer
# from detectron2.data import MetadataCatalog, DatasetCatalog

from coco_classes import categories

app = Flask(__name__)

enable_detectron = True

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return
       
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        img.save('images/image.jpg')
      
        # Detectron
        if(enable_detectron):
          cfg = get_cfg()
          
          # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
          cfg.MODEL.DEVICE = 'cpu'
          cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
          cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
          # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
          cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

          predictor = DefaultPredictor(cfg)
          im = cv2.imread('images/image.jpg')
          outputs = predictor(im)

          prediction_classes = outputs['instances'].pred_classes.cpu().tolist()
          predicted_categories = list(map(lambda category_id: categories[category_id + 1], prediction_classes  ))
    
          print(predicted_categories[0])
          # speech_engine.save_to_file(predicted_categories[0], 'detectron-prediction.mp3')
          # speech_engine.runAndWait()

          return 'Detectron complete'

        results = model([img])

        results.render()  # updates results.imgs with boxes and labels
        # results.save(save_dir="static/")
        
        df_json = results.pandas().xyxy[0].to_json(orient="records") 
        prediction_to_text = json.loads(df_json)[0]['name']
      
        speech_engine.save_to_file(prediction_to_text, 'yolo5-prediction.mp3')
        speech_engine.runAndWait()
      
        return "Yolo complete"

    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8080, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # force_reload = recache latest code
    model.eval()

    speech_engine = pyttsx3.init()
  
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
