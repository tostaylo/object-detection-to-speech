import os
import io
from PIL import Image

from datasets import categories
from ml_models.yolo import get_yolo_predictions, get_yolo_model
from ml_models.detectron import get_detectron_predictor, get_detectron_prediction


yolo_model = get_yolo_model()
detectron_predictor = get_detectron_predictor()

working_directory = os.getcwd()
file_path = working_directory + "/tests/images/person.jpg"

with open(file_path, "rb") as file:
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    yolo_prediction = get_yolo_predictions(yolo_model, img, 0)
    detectron_prediction = get_detectron_prediction(detectron_predictor, img, categories)
    print('hi')
    print(detectron_prediction)
    assert(yolo_prediction == 'persons')
    assert(detectron_prediction == 'person')