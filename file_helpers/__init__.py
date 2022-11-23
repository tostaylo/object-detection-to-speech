import base64, os, cv2

def handle_file(request, redirect):
  if "file" not in request.files:
    return redirect(request.url)
  file = request.files["file"]
  if not file:
      return
  
  return file

def decode_base64_img(base_64_img_json):
  base64_image_str = base_64_img_json[base_64_img_json.find(",")+1:]
  decoded = base64.decodebytes(bytes(base64_image_str, "utf-8"))

  return decoded

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