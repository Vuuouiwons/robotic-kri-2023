from threading import Thread, Event
import cv2
from time import sleep
import serial
import sys, os
from numpy import rad2deg, arctan2

class ArduinoStreamWidget(object):
    def __init__(self):
        self.arsensorikstr = 'ini string arduino sensorik'
        self.serS = serial.Serial('/dev/ttyACM1', 500000)
        self.serM = serial.Serial('/dev/ttyACM0', 500000)
        print('Arduino Thread running, wait for 12 second')
        sleep(13)

    def Stream(self):
        while True:
            self.serS.write('o'.encode("utf-8"))
            msg = self.serS.read(22).decode("utf-8")
            index = msg.find('#')
            self.arsensorikstr = msg[index:] + msg[:index]

            global stop_threads 
            if stop_threads: 
                print('Arduino thread stopped') 
                break
    
    def get_MPU_val(self):
        return int(self.arsensorikstr[1:4])

    def get_Y_pos(self):
        msg = self.arsensorikstr[11:16].replace('-0', '0')
        return int(msg)

    def get_X_pos(self):
        msg = self.arsensorikstr[5:10].replace('-0', '0')
        return int(msg)    

    def get_IR_val(self):
        return (int(self.arsensorikstr[17]) + 1) % 2

    def set_Arduino_motorik(self, val):
        self.serM.write(val)

    def ToString(self):
        print('MPU : ',self.get_MPU_val(),";X : ", self.get_X_pos(),";Y : ",self.get_Y_pos(),';IR : ',self.get_IR_val())

class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.green_HSV = {
            'lowH' : 68,
            'highH' : 111,
            'lowS' : 91,
            'highS' : 195,
            'lowV' : 121,
            'highV' : 212
        }

        self.orange_HSV = {
            'lowH' : 0,
            'highH' : 21,
            'lowS' : 87,
            'highS' : 248,
            'lowV' : 107,
            'highV' : 255
        }

        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def Stream(self):
        print('camera thread running')
        # Read the next frame from the stream in a different thread
        while True:
            
            if self.capture.isOpened():
                (self.status, self.oriframe) = self.capture.read()
                sleep(.01)
        
            try:
                self.oriframe = cv2.GaussianBlur(self.oriframe,(5,5),0)
                # self.frame = self.mask_img(self.oriframe)
                self.frame = self.oriframe
                self.green_filtering()
                self.orange_filtering()
                self.ball = cv2.bitwise_and(self.green_filtered_frame, self.orange_filtered_frame)

                global stop_threads 
                if stop_threads: 
                    print('camera thread stopped') 
                    break
            except Exception as e :
                exc_type, _, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno, e)
                return None

    def show_frame(self):
        # Display frames in main program
        
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            global stop_threads 
            stop_threads = True
            exit(1)

    def show_ball_frame(self):
        # Display frames in main program 
        try:   
            self.get_ball_coordinate()
            cv2.imshow('ball', self.ball)
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.capture.release()
                cv2.destroyAllWindows()
                global stop_threads 
                stop_threads = True

                exit(1)
            #     return None
        except Exception as e :
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, e)
    def get_ball_XY(self):
        return self.X_ball, self.Y_ball

    def mask_img(self, img):
        img = cv2.circle(img, (288,258), 15, (0,0,0), 51) 
        img = cv2.circle(img, (288,258), 325, (0,0,0), 251) 
        return img

    def green_filtering(self):
        self.green_filtered_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.green_filtered_frame = cv2.inRange(self.green_filtered_frame,(self.green_HSV['lowH'],self.green_HSV['lowS'],self.green_HSV['lowV']) , (self.green_HSV['highH'],self.green_HSV['highS'],self.green_HSV['highV']))

        dilatation_size = 2
        element = cv2.getStructuringElement(2, (2*dilatation_size + 1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
        self.green_filtered_frame = cv2.dilate(self.green_filtered_frame, element)

    def orange_filtering(self):
        self.orange_filtered_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.orange_filtered_frame = cv2.inRange(self.orange_filtered_frame,(self.orange_HSV['lowH'],self.orange_HSV['lowS'],self.orange_HSV['lowV']) , (self.orange_HSV['highH'],self.orange_HSV['highS'],self.orange_HSV['highV']))

        dilatation_size = 5
        element = cv2.getStructuringElement(2, (2*dilatation_size + 1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
        self.orange_filtered_frame = cv2.dilate(self.orange_filtered_frame, element)

    def get_ball_coordinate(self):
        self.X_ball,self.Y_ball=0,0
        M = cv2.moments(self.ball)
        if int(M["m00"])>100:
            self.X_ball = int(M["m10"] / M["m00"])
            self.Y_ball = int(M["m01"] / M["m00"])
            cv2.circle(self.frame, (self.X_ball, self.Y_ball), 10, (0, 255, 0), 1)

    def get_ball_command(self):
        if self.X_ball ==0 and self.Y_ball == 0 :
            return 'q'.encode()
        elif self.X_ball >= 320 - 12 and self.X_ball <= 320 + 12 :
            return 'w'.encode()
        elif self.X_ball < 320 - 12:
            return 'q'.encode()
        elif self.X_ball > 320 + 12:
            return 'e'.encode()
        else:
            return 'o'.encode()

gawangX, gawangY = 260, 300

def getTargetXY(targetX, targetY, currentX, currentY):
    return targetX-currentX, targetY-currentY

def transform_XY(x, y):
    x = -1 * x
    y = 600-y
    return x, y


def cartesian2polar(x, y):
    # 1. Rotasi -90 d + convert to polar
    Theta = rad2deg(arctan2(-x, y))
    # 2. konversi ke format yg diinginkan
    if(Theta > 0):
        Theta = 360-Theta
    else:
        Theta = Theta*-1
    return(Theta)

if __name__ == '__main__':
    prevmpu = 0
    try:
        stop_threads = False

        video_stream_widget = VideoStreamWidget()
        arduino = ArduinoStreamWidget()
        
        t1 = Thread(target = video_stream_widget.Stream, args = ())
        t1.start()

        t2 = Thread(target = arduino.Stream, args = ())
        t2.start()
        
        sleep(1)
        arduino.set_Arduino_motorik('y'.encode())
        while True:

            video_stream_widget.show_frame()
            video_stream_widget.show_ball_frame()
            

            # cv2.imshow('ball',  video_stream_widget.ball)
            # x,y = video_stream_widget.get_ball_XY()
            # print('x : ', x, '\t','y : ', y)
            print('x : ', arduino.get_X_pos(),' Y : ', arduino.get_Y_pos())
            ir = arduino.get_IR_val()
            # print(ir)
            if ir == 0 :
                cmd = video_stream_widget.get_ball_command()
                print('motor command : ',cmd)
            else:
                arduino.set_Arduino_motorik('y'.encode())

                # arduino.set_Arduino_motorik('o'.encode())
                # arduino.set_Arduino_motorik('n'.encode())
                tx,ty = getTargetXY(-300, 230,arduino.get_X_pos(), arduino.get_Y_pos())
                dir = round(cartesian2polar(tx,ty)) 

                mpunow = round(arduino.get_MPU_val()) 

                if abs(mpunow - prevmpu > 300):
                    sleep(1)

                posisiX = arduino.get_X_pos()
                print(dir,mpunow)

                if mpunow < dir - 3 or mpunow > dir + 3:
                    if mpunow-dir < -7:
                        print('kiri')
                        arduino.set_Arduino_motorik('q'.encode())
                    elif mpunow - dir > 7:
                        print('kanan')
                        arduino.set_Arduino_motorik('e'.encode())
                    elif mpunow-dir < 7 and mpunow - dir > -7:
                        print('benar')

                        if posisiX < 50:
                            arduino.set_Arduino_motorik('w'.encode())
                            sleep(0.2)
                        else:
                            arduino.set_Arduino_motorik('o'.encode())
                            arduino.set_Arduino_motorik('n'.encode())
                            arduino.set_Arduino_motorik('+'.encode())
            #     arduino.set_Arduino_motorik(cmd)
            # else:
            #     arduino.set_Arduino_motorik('o'.encode())
            #     arduino.set_Arduino_motorik('n'.encode())
            #     # sleep(1)
            #     arduino.set_Arduino_motorik('+'.encode())
                

            # print(arduino.ToString())

    except KeyboardInterrupt:
        print ('attempting to close threads.')

        stop_threads = True
        t1.join()
        t2.join()
        print ('threads successfully closed')
     

    except Exception as e :
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)
        print ('exception attempting to close threads.')

        stop_threads = True
        t1.join()
        t2.join()
        print ('threads successfully closed')
     

exit(1)