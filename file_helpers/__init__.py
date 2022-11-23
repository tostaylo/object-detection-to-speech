import base64

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
