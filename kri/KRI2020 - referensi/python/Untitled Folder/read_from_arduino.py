import serial, cv2

ser = serial.Serial('/dev/ttyUSB0', 2000000)

while(ser.isOpen()):
    msg = ser.read(22).decode("utf-8")
    index = msg.find('#')
    msg = msg[index:] + msg[:index]
    print(msg)

    if cv2.waitKey(1) == 27:
        break
