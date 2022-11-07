def handle_file(request, redirect):
  if "file" not in request.files:
    return redirect(request.url)
  file = request.files["file"]
  if not file:
      return
  
  return file