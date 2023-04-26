import asyncio
import websockets

connected = dict()

async def echo(ws, path):
  print("client connected")
  # register
  connected.add(ws)
  async for msg in ws:
    test_dict = eval(msg)
    print("ping: " + str(msg))
    await ws.send("pong:" + str(msg))

start_server = websockets.serve(echo, "localhost", 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

