def handle_file(request, redirect):
  if "file" not in request.files:
    return redirect(request.url)
  file = request.files["file"]
  if not file:
      return
  
  return file

def print_versions(torch, detectron2):
  TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
  print("torch: ", TORCH_VERSION)
  print("detectron2:", detectron2.__version__)