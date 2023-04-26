import asyncio
import websockets
from nanoid import generate
import time
PORT = 8765

CONNECTIONS = dict()

async def main(ws):
  try:
    data = await ws.recv()
    id = generate()
    
    print("Client connected " + data)
    
    CONNECTIONS[id] = ws
    
    await ws.send(str(id))
    
    while True:
      print(await CONNECTIONS[id].recv())
      await CONNECTIONS[id].send(id)
      print(CONNECTIONS)
      time.sleep(1)
  except:
    print("something went wrong")
  else:
    print("nothing went wrong")
  finally:
    CONNECTIONS.pop(id)
    print(CONNECTIONS)

server = websockets.serve(main, "localhost", PORT)

if(__name__ == "__main__"):
  asyncio.get_event_loop().run_until_complete(server)
  asyncio.get_event_loop().run_forever()