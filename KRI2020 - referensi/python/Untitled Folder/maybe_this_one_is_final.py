from threading import Thread
import cv2, time

class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.green_HSV = {
            'lowH' : 69,
            'highH' : 88,
            'lowS' : 82,
            'highS' : 215,
            'lowV' : 141,
            'highV' : 254
        }

        self.orange_HSV = {
            'lowH' : 0,
            'highH' : 18,
            'lowS' : 149,
            'highS' : 255,
            'lowV' : 222,
            'highV' : 255
        }

        self.capture = cv2.VideoCapture(src)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = False
        self.thread.start()
        # self.update()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
                time.sleep(.01)
        
            try:
                self.frame = cv2.GaussianBlur(self.frame,(5,5),0)
                self.frame = self.mask_img(self.frame)
                self.green_filtering()
                self.orange_filtering()
                self.ball = cv2.bitwise_and(self.green_filtered_frame, self.orange_filtered_frame)
            except:
                pass
                
            

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
        pass

if __name__ == '__main__':
    video_stream_widget = VideoStreamWidget()
    time.sleep(1)
    while True:
        try:
            # video_stream_widget.show_frame()
            # video_stream_widget.show_ball_frame()
            cv2.imshow('ball',  video_stream_widget.ball)
            x,y = video_stream_widget.get_ball_XY()
            print('x : ', x, '||y : ', y)


            
                # return None
            
            
        except AttributeError:
            pass

