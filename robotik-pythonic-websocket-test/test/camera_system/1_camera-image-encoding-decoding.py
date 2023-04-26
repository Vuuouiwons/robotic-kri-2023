import cv2 as cv
import numpy as np
import base64
import json
import pickle

# Open the default camera
cap = cv.VideoCapture(0)

# set resolution
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

# Set the frame rate to 30 fps
cap.set(cv.CAP_PROP_FPS, 30)

# Define the compression quality
quality = 50

def im2json(im):
  """Convert a Numpy array to JSON string"""
  imdata = pickle.dumps(im)
  jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})
  return jstr

def json2im(jstr):
  """Convert a JSON string back to a Numpy array"""
  load = json.loads(jstr)
  imdata = base64.b64decode(load['image'])
  im = pickle.loads(imdata)
  return im

while True:
  # Capture a frame from the camera
  ret, frame = cap.read()

  # Check if the frame was captured successfully
  if not ret:
      break

  # Encode the frame with JPEG compression
  encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]

  result, encimg = cv.imencode('.jpg', frame, encode_param)
  
  # to json
  img_json = im2json(encimg)
  # to img
  jsonimg = json2im(img_json)
  
  # Decode the compressed frame
  decimg = cv.imdecode(jsonimg, 1)

  # print(type(encimg), type(decimg))
  print(np.array_equal(encimg, img_json))
  
  # Display the compressed frame
  cv.imshow('Compressed Frame1', decimg)

  # Wait for a key press to exit
  if cv.waitKey(1) & 0xFF == ord('q'):
    break

# Release the camera and close the window
cap.release()
cv.destroyAllWindows()
