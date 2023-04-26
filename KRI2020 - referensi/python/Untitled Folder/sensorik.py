import serial
from time import sleep

class ArduinoStreamWidget(object):
    def __init__(self):
        self.arsensorikstr = 'ini string arduino sensorik'
        self.serS = serial.Serial('/dev/ttyUSB1', 500000)
        self.serM = serial.Serial('/dev/ttyUSB0', 500000)
        print('wait for 12 second')
        sleep(13)

    def update(self):
        # self.serS.write('o'.encode("utf-8"))
        msg = self.serS.read(22).decode("utf-8")
        index = msg.find('#')
        self.arsensorikstr = msg[index:] + msg[:index]
    
    def get_MPU_val(self):
        return int(self.arsensorikstr[1:4])

    def get_Y_pos(self):
        msg = self.arsensorikstr[11:16].replace('-0', '0')
        return int(msg)

    def get_X_pos(self):
        msg = self.arsensorikstr[5:10].replace('-0', '0')
        return int(msg)    

    def get_IR_val(self):
        return (int(self.arsensorikstr[17]) + 1) %2

    def set_Arduino_motorik(self, val):
        self.serM.write(val)

    def get_sensor(self):
        return self.arsensorikstr
    

def main():
    arduino = ArduinoStreamWidget()
    while True:
        try:
            arduino.update()
            # print('full : ',arduino.arsensorikstr)
            # print('mpu : ', arduino.get_MPU_val())
            # print('X : ', arduino.get_X_pos())
            # print('y : ', arduino.get_Y_pos())
            # print('ir : ', arduino.get_IR_val())
            print((arduino.get_IR_val()))
            if arduino.get_IR_val():
                print('dribbler nyala')
                arduino.set_Arduino_motorik(b'y')
            else:
                print('dribbler mati')
                arduino.set_Arduino_motorik(b'n')

            print(arduino.get_sensor())
        except Exception as e:
            print(e)

main()