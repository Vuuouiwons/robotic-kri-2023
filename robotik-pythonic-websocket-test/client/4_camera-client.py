import asyncio
import websockets
import time
import cv2 as cv
import numpy as np
import json
import pickle
import base64

def im2json(im):
  """Convert a Numpy array to JSON string"""
  imdata = pickle.dumps(im)
  jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})
  return jstr

async def main():
  # init camera
  cap = cv.VideoCapture(0)

  # set resolution
  cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
  cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

  # set fps
  cap.set(cv.CAP_PROP_FPS, 24)

  # compression quality
  quality = 20

  # Encode the frame with JPEG compression
  encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]

  host = "localhost"
  uri = f"ws://{host}:8765"
  
  username = input("username: ")
  destination = input("target connection: ")
  timeout = 18446744073709551616 # basically never
  async with websockets.connect(uri, ping_interval=timeout, ping_timeout=timeout) as ws:
    # register
    
    if destination == "self" or destination == '':
      destination = username
    
    reg_data = {
      "username": username,
      "target": destination
    }
    
    await ws.send(str(reg_data))
    
    if await ws.recv() != "SUCCESS": 
      print("Did not connect to server")
      exit(1)
    else:
      print("Initialization Sucessful Targeting to", reg_data["target"])
    
    while True:
      # Capture a frame from the camera
      ret, frame = cap.read()
      
      # check if image is succesfully captured
      if not ret:
        break
      
      # encode image
      result, encimg = cv.imencode('.jpg', frame, encode_param)
      payload = im2json(encimg)
      
      # send image
      await ws.send(payload)
      
      # print response
      pong = await asyncio.wait_for(ws.recv(), timeout=10000000)
      print("sent: ", pong)
      time.sleep(0.075)

if __name__ == "__main__":
  print("Client Initializing")
  asyncio.get_event_loop().run_until_complete(main())

