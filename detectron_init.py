import os, cv2

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
# from detectron2.utils.visualizer import Visualizer
# from detectron2.data import MetadataCatalog, DatasetCatalog

def get_detectron_predictor():
    cfg = get_cfg()
          
    # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
    # https://github.com/facebookresearch/detectron2/issues/300
    cfg.MODEL.DEVICE = 'cpu'
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

    predictor = DefaultPredictor(cfg)

    return predictor

def get_detectron_prediction(predictor, img, categories):
  image_directory = 'temp_images'
  image_path = f'{image_directory}/image.jpg'
  isDirectory = os.path.exists(image_directory)
  
  if (not isDirectory):
    os.mkdir(image_directory)

  img.save(image_path)
  im = cv2.imread(image_path)

  outputs = predictor(im)
  
  prediction_classes = outputs['instances'].pred_classes.cpu().tolist()
  predicted_categories = list(map(lambda category_id: categories[category_id + 1], prediction_classes  ))
  first_prediction = predicted_categories[0]
  
  return first_prediction