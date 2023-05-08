from threading import Thread, Event
import cv2
from time import sleep
import serial

class ArduinoStreamWidget(object):
    def __init__(self):
        self.arsensorikstr = 'ini string arduino sensorik'
        self.serS = serial.Serial('/dev/ttyUSB1', 500000)
        self.serM = serial.Serial('/dev/ttyUSB0', 500000)
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
        return (int(self.arsensorikstr[17]) + 1) %2

    def set_Arduino_motorik(self, val):
        self.serM.write(val)

    def ToString(self):
        print('MPU : ',self.get_MPU_val(),";X : ", self.get_X_pos(),";Y : ",self.get_Y_pos(),';IR : ',self.get_IR_val())

class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.green_HSV = {
            'lowH' : 60,
            'highH' : 103,
            'lowS' : 91,
            'highS' : 255,
            'lowV' : 0,
            'highV' : 140
        }

        self.orange_HSV = {
            'lowH' : 0,
            'highH' : 55,
            'lowS' : 195,
            'highS' : 255,
            'lowV' : 0,
            'highV' : 255
        }

        self.capture = cv2.VideoCapture(src)

        # Start the thread to read frames from the video stream
        # self.thread = Thread(target=self.update, args=())
        # self.thread.daemon = False
        # self.thread.start()

    def Stream(self):
        print('camera thread running')
        # Read the next frame from the stream in a different thread
        while True:
            
            if self.capture.isOpened():
                (self.status, self.oriframe) = self.capture.read()
                sleep(.01)
        
            try:
                self.oriframe = cv2.GaussianBlur(self.oriframe,(5,5),0)
                self.frame = self.mask_img(self.oriframe)
                self.green_filtering()
                self.orange_filtering()
                self.ball = cv2.bitwise_and(self.green_filtered_frame, self.orange_filtered_frame)

                global stop_threads 
                if stop_threads: 
                    print('camera thread stopped') 
                    break
            except:
                print('something here')
                return None

    def show_frame(self):
        # Display frames in main program
        
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
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
                exit(1)
            #     return None
        except :
            pass

    def get_ball_XY(self):
        return self.X_ball, self.Y_ball

    def mask_img(self, img):
        image = cv2.circle(img, (286,260), 15, (0,0,0), 51) 
        image = cv2.circle(img, (286,260), 325, (0,0,0), 251) 
        return img

    def green_filtering(self):
        self.green_filtered_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.green_filtered_frame = cv2.inRange(self.green_filtered_frame,(self.green_HSV['lowH'],self.green_HSV['lowS'],self.green_HSV['lowV']) , (self.green_HSV['highH'],self.green_HSV['highS'],self.green_HSV['highV']))

        dilatation_size = 3
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
            return 'o'
        elif self.X_ball >= 286 - 10 and self.X_ball <= 286 + 10 and self.Y_ball < 260:
            return 'w'
        elif self.X_ball >= 286  and self.Y_ball < 260:
            return 'q'
        elif self.X_ball < 286 and self.Y_ball < 260:
            return 'e'
        elif self.X_ball < 286 - 12:
            return 'e'
        elif self.X_ball > 300 + 12:
            return 'q'
        else:
            return 'o'

if __name__ == '__main__':
    try:
        stop_threads = False

        video_stream_widget = VideoStreamWidget()
        arduino = ArduinoStreamWidget()
        
        t1 = Thread(target = video_stream_widget.Stream, args = ())
        t1.start()

        t2 = Thread(target = arduino.Stream, args = ())
        t2.start()
        
        sleep(1)
        arduino.set_Arduino_motorik('y')
        while True:

            video_stream_widget.show_frame()
            video_stream_widget.show_ball_frame()
            

            # cv2.imshow('ball',  video_stream_widget.ball)
            # x,y = video_stream_widget.get_ball_XY()
            # print('x : ', x, '\t','y : ', y)
            print('x : ', arduino.get_X_pos(),' Y : ', arduino.get_Y_pos())
            ir = arduino.get_IR_val()
            print(ir)
            if ir == 0 :
                cmd = video_stream_widget.get_ball_command()
                print('motor command : ',cmd)
                arduino.set_Arduino_motorik(cmd)
            else:
                arduino.set_Arduino_motorik('o')

            # print(arduino.ToString())

    except KeyboardInterrupt:
        print ('attempting to close threads.')

        stop_threads = True
        t1.join()
        t2.join()
        print ('threads successfully closed')
     

    except Exception as e :
        print('error : ', e)
        print ('exception attempting to close threads.')

        stop_threads = True
        t1.join()
        t2.join()
        print( 'threads successfully closed')
     

exit(1)