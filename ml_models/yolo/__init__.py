import json
import torch

def get_yolo_model():
  yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True) 
  yolo_model.eval()
 
  return yolo_model;

def get_yolo_predictions(model, img, idx):
  results = model([img])
  df_json = results.pandas().xyxy[0].to_json(orient="records") 
  prediction_data = json.loads(df_json)[idx]
  prediction_name = prediction_data['name']
  confidence = prediction_data['confidence']
  confidence_to_percent =  round(confidence * 100, 2)
  return (prediction_name, confidence_to_percent)