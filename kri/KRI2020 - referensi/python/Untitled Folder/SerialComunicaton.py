import serial

class SerialCommunication:

    def __init__(self, name, baudrate):
        self.serialPort = serial.Serial(name, baudrate)

    def isOpen(self):
        return self.serialPort.isOpen()

    def get_full_string(self):
        self.serialPort.write('o'.encode("utf-8"))
        msg = self.serialPort.read(22).decode("utf-8")
        index = msg.find('#')
        msg = msg[index:] + msg[:index]
        return (msg)

    def get_mpu_value(self):
        self.serialPort.write('o'.encode("utf-8"))
        msg = self.serialPort.read(22).decode("utf-8")
        index = msg.find('#')
        msg = msg[index:] + msg[:index]
        return (int(msg[1:4]))

    def get_xy_position(self):
        self.serialPort.write('o'.encode("utf-8"))
        msg = self.serialPort.read(22).decode("utf-8")
        index = msg.find('#')
        msg = msg[index:] + msg[:index]
        return [int(msg[5:10]),int(msg[11:16])]

    def get_ir_value(self):
        self.serialPort.write('o'.encode("utf-8"))
        msg = self.serialPort.read(22).decode("utf-8")
        index = msg.find('#')
        msg = msg[index:] + msg[:index]
        return (int(msg[17:18]))

    def get_button_value(self):
        self.serialPort.write('o'.encode("utf-8"))
        msg = self.serialPort.read(22).decode("utf-8")
        index = msg.find('#')
        msg = msg[index:] + msg[:index]
        return [int(msg[19:20], int(msg[21:22]))]