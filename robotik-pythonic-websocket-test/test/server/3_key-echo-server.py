import asyncio
import websockets
import time
import socket

PORT = 8765
CONNECTIONS = dict()

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
      
      # check payload
      print("sent by", data["username"], payload)
      
      # send to robot
      await CONNECTIONS[data["username"]]["ws"].send(payload)
      
      # echo to client
      await CONNECTIONS[data["target"]]["ws"].send(payload)
      
  except websockets.exceptions.ConnectionClosed as e:
    print("Error: ", e)
  else:
    print("Connection Terimnated Succesfully")
  finally:
    CONNECTIONS.pop(data["username"])
    print("Connected devices: ", CONNECTIONS)

timeout = 18446744073709551616 # basically never

server = websockets.serve(main, "localhost", PORT, ping_interval=timeout, ping_timeout=timeout)

if(__name__ == "__main__"):
  print("server local ip:", socket.gethostbyname(socket.gethostname()))
  print("WS Server Listening on port", PORT)
  asyncio.get_event_loop().run_until_complete(server)
  asyncio.get_event_loop().run_forever()