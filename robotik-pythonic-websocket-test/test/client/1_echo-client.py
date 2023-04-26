import asyncio
import websockets
import time

async def hello():
  uri = "ws://localhost:8765"
  
  async with websockets.connect(uri) as ws:
    id = {"id":"robot1"}
    await ws.send(str(id))
    
    while True:
      recv = await ws.recv()
      print(recv)
      
      data = {"data": "this"}
      print(data, type(str(data)))
      await ws.send(str(data))
      time.sleep(1)

asyncio.get_event_loop().run_until_complete(hello())