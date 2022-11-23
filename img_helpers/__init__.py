import io, os, cv2
from PIL import Image

def get_img_from_file(file):
  contents = file.read()
  img = Image.open(io.BytesIO(contents))

  return img

def get_img_from_decoded(decoded):
  img = Image.open(io.BytesIO(decoded))
  
  return img


def get_img_from_temp_directory(img):
  # workaround function for being able to convert images to format needed by prediction models
  image_directory = 'temp_images'
  image_path = f'{image_directory}/image.jpg'
  isDirectory = os.path.exists(image_directory)
  
  if (not isDirectory):
    os.mkdir(image_directory)

  img.save(image_path)
  im = cv2.imread(image_path)

  return im