import asyncio
import websockets
import time
import socket
import cv2 as cv
import numpy as np
import pickle
import json
import base64

PORT = 8765
CONNECTIONS = dict()
host = socket.gethostbyname(socket.gethostname())

def json2im(jstr):
  """Convert a JSON string back to a Numpy array"""
  load = json.loads(jstr)
  imdata = base64.b64decode(load['image'])
  im = pickle.loads(imdata)
  return im

async def main(ws):
  
  try:
    data = eval(await ws.recv())
    print(f"Client connected: {str(data)}")
    
    # register 
    CONNECTIONS[data["username"]] = {
      "target": data["target"],
      "ws": ws,
    }
    
    if ws:
      await ws.send("SUCCESS")
    
    while True:
      # grab key from payload
      payload = await asyncio.wait_for(CONNECTIONS[data["username"]]["ws"].recv(), timeout=10000000)
      
      enc_img = json2im(payload)
      
      # decode payload
      img = cv.imdecode(enc_img, 1)
      cv.imwrite(".\\test.jpg", img)
      
      # show payload
      img_sys = cv.imread(".\\test.jpg")
      cv.imshow(data["username"], img)
      
      # send to robot
      await CONNECTIONS[data["username"]]["ws"].send('IT WORKED')
      
      # echo to client
      await CONNECTIONS[data["target"]]["ws"].send("IT WORKED")
      
      # terminate connection
      if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyWindow(data["username"])
        await ws.close()
        break
      
  except websockets.exceptions.ConnectionClosed as e:
    print("Error: ", e)
  else:
    print("Connection Terimnated Succesfully")
  finally:
    CONNECTIONS.pop(data["username"])
    print("Connected devices: ", CONNECTIONS)

timeout = 18446744073709551616 # basically never

server = websockets.serve(main, host, PORT, ping_interval=timeout, ping_timeout=timeout)

if(__name__ == "__main__"):
  print("server local ip:", host)
  print("WS Server Listening on port", PORT)
  asyncio.get_event_loop().run_until_complete(server)
  asyncio.get_event_loop().run_forever()

