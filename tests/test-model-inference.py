import os
import io
import torch
from PIL import Image


model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True)

working_directory = os.getcwd()
file_path = working_directory + "/tests/images/person.jpg"

with open(file_path, "rb") as file:
    img_bytes = file.read()
img = Image.open(io.BytesIO(img_bytes))

results = model(img, size=640)

print(results.pandas().xyxy[0])