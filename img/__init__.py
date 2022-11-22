import io
from PIL import Image

def get_img_from_file(file):
  contents = file.read()
  img = Image.open(io.BytesIO(contents))

  return img

def get_img_from_decoded(decoded):
  img = Image.open(io.BytesIO(decoded))
  
  return img