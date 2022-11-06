import argparse
import io
import os
from PIL import Image
import torch
from flask import Flask, render_template, request, redirect
import json
import pyttsx3


app = Flask(__name__)


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
        results = model([img])

        results.render()  # updates results.imgs with boxes and labels
        # results.save(save_dir="static/")
        
        df_json = results.pandas().xyxy[0].to_json(orient="records") 
        prediction_to_text = json.loads(df_json)[0]['name']
      
        speech_engine.save_to_file(prediction_to_text, 'prediction.mp3')
        speech_engine.runAndWait()
      
        return "hihi"

    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8080, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # force_reload = recache latest code
    model.eval()

    speech_engine = pyttsx3.init()
  
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
