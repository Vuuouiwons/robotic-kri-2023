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
baud_rate = 500000
arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=.1)


def send_key_press(serial_device, key):
    serial_device.write(str(key + "\n").encode())
    print(str(key))


# init class
cams = {
    "front": Camera("front", 1, 1280, 720, {}),
    "back": Camera("back", 2, 1280, 720, {}),
    "left": Camera("left", 3, 1280, 720, {}),
    "right": Camera("right", 0, 1280, 720, {}),
}

orange = [[0, 177, 168], [12, 255, 255]]
green = [[68, 91, 121], [111, 195, 212]]

last_action = "o"

while True:
    def decision(last_action):
        temp_dec = list()
        images = list()
        for key, val in cams.items():
            image = val.get_processed_frame(orange)
            coords = val.get_single_center_object(image)
            coords_processed = val.get_object_location(
                [coords[1]], [1280, 720])
            action = val.chase_emergency(coords_processed, last_action)
            temp_dec.append(action)

            images.append({
                "k": key,
                "image": image
            })
        print(temp_dec[1])
        return [images, mode(temp_dec[1])]

    action = decision(last_action)

    for i in action[0]:
        cv.imshow(i['k'], i["image"])

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    key = list(filter(lambda x: x != '', action[1]))

    send_key_press(arduino, key[0])
    last_action = key[0]
