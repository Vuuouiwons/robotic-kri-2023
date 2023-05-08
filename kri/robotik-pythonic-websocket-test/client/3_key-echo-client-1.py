import asyncio
import websockets
import time
import keyboard

async def main():
  
  host = "localhost"
  
  uri = f"ws://{host}:8765"
  
  username = input("username: ")
  destination = input("target connection: ")
  timeout = 18446744073709551616 # basically never
  async with websockets.connect(uri, ping_interval=timeout, ping_timeout=timeout) as ws:
    # register
    
    if(destination == "self"):
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
      # get key
      key = keyboard.read_key()
      
      if(key == '\''):
        await ws.close()
        exit(0)
      
      # send key
      await ws.send(key)
      
      # print response
      pong = await asyncio.wait_for(ws.recv(), timeout=10000000)
      print("sent: ", pong)
      
      time.sleep(0.005)

if __name__ == "__main__":
  print("Client Initializing")
  asyncio.get_event_loop().run_until_complete(main())

