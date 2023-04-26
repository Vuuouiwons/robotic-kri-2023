import asyncio
import websockets
import time
import serial
import serial.tools.list_ports as port_list

ports = list(port_list.comports())

for i in ports:
    print("Serial connection: ", i.device)

port = ports[0].device # kalo ga bisa angka 0 ini diganti jadi 1 / 2 / 3 / 4 / ... / n
baud_rate = 500000
arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=.1)


def send_key_press(serial_device, key):
    serial_device.write(str(key + "\n").encode())
    print(str(key))

async def main():  
  
  host = input("host: ")
  
  uri = f"ws://{host}:8765"
  
  username = input("username(only a-z): ")
  timeout = 18446744073709551616 # basically never
  
  async with websockets.connect(uri, ping_interval=timeout, ping_timeout=timeout) as ws:
    # register
    
    reg_data = {
      "username": username,
      "target" : "none"
    }
    
    await ws.send(str(reg_data))
    
    if await ws.recv() != "SUCCESS": 
      print("Did not connect to server")
      exit(1)
    else:
      print("Initialization Sucessful Targeting to", reg_data["target"])
    
    while True:
      payload = await asyncio.wait_for(ws.recv(), timeout=timeout)
      print(payload)
      
      send_key_press(arduino, payload)
      time.sleep(0.005)

if __name__ == "__main__":
  print("Client Initializing")
  asyncio.get_event_loop().run_until_complete(main())

