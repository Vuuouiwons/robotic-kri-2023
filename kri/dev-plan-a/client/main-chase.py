import serial
import serial.tools.list_ports as port_list
from sensors.camera import Camera
from statistics import mode
import cv2 as cv

ports = list(port_list.comports())

for i in ports:
    print("Serial connection: ", i.device)

# kalo ga bisa angka 0 ini diganti jadi 1 / 2 / 3 / 4 / ... / n

port = ports[0].device
baud_rate = 2000000
arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=.1)


def send_key_press(serial_device, key):
    serial_device.write(str(key + "\n").encode())
    print(str(key))


# init class
cams = {
    "front": Camera("front", 1),
    "back": Camera("back", 2),
    "left": Camera("left", 3),
    "right": Camera("right", 0),
}
color_hsv = {
    "orange": [[0, 191, 141], [17, 255, 255]],
    "green": [[68, 91, 121], [111, 195, 212]],
    "black": [[54, 21, 28], [137, 111, 78]],
    "yellow": [[0, 75, 191], [76, 255, 255]],
    "blue": [[95, 189, 183], [120, 255, 146]],
}

last_action = "o"

while True:
    def decision(last_action):
        temp_dec = list()
        images = list()
        for key, val in cams.items():
            action = val.chase(color_hsv["orange"])
            (image, action) = action
            temp_dec.append(action)
            images.append({
                "k": key,
                "image": image
            })
            
        print(list(cams.keys()), temp_dec)
        return [images, temp_dec]

    action = decision(last_action)

    for i in action[0]:
        cv.imshow(i['k'], i["image"])

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    key = list(filter(lambda x: x != '', action[1]))

    if key == []:
        # send_key_press(last_action)
        print(last_action)
    else:
        # send_key_press(key[0])
        print(key[0])
        last_action = key[0]