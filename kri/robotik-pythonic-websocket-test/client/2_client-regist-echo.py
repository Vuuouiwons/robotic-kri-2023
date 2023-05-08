import asyncio
import websockets
import time

async def hello():
  uri = "ws://localhost:8765"
  id = str()
  async with websockets.connect(uri) as ws:
    ping = "somepayload"
    id = await ws.send(ping)
    while True:
      await ws.send("awk")
      pong = await ws.recv()
      print(pong)
      
      # close connection
      # await ws.close()
    # while True:
    #   recv = await ws.recv()
    #   print(recv)
      
    #   data = {"data": "this"}
    #   print(data, type(str(data)))
      
    #   await ws.send(str(data))
    #   time.sleep(1)

asyncio.get_event_loop().run_until_complete(hello())