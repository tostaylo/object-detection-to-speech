from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.logger import setup_logger
# from detectron2.utils.visualizer import Visualizer
# from detectron2.data import MetadataCatalog, DatasetCatalog

from helpers.images import get_img_from_temp_directory

setup_logger()

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
  im = get_img_from_temp_directory(img)
  outputs = predictor(im)
  instances = outputs['instances']
  scores = instances.scores.cpu().tolist()
  prediction_classes = instances.pred_classes.cpu().tolist()
  
  if (len(scores)== 0 or len(prediction_classes) == 0):
    return ('no prediction', 0)

  predicted_categories = list(map(lambda category_id: categories[category_id + 1], prediction_classes  ))
  first_prediction = predicted_categories[0]
  first_score = scores[0]
  first_score_to_percent = round(first_score * 100, 2) 

  return (first_prediction, first_score_to_percent)