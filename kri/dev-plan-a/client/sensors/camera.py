import cv2 as cv
import numpy as np


class Camera:
    def __init__(self, camera_name, camera: int, width=1280, height=720) -> None:
        self.__camera_id = camera
        self.__camera_height = height
        self.__camera_width = width
        self.__image = list()

        # initialize capture device
        self.__cap = cv.VideoCapture(camera,  cv.CAP_DSHOW)
        self.__cap.set(cv.CAP_PROP_FRAME_WIDTH, self.__camera_width)
        self.__cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.__camera_height)

        # objects dict and coords
        self.__camera_name = camera_name

    def __repr__(self) -> str:
        pass

    def __eq__(self, __value: object) -> bool:
        pass

    def get_frame(self) -> np.ndarray:
        ret, img = self.__cap.read()

        if not ret:
            return f"Err in {self.__camera_id}"

        self.__image = img

        return img

    def get_processed_frame(self, color_hsv: list[list]) -> np.ndarray:
        img = None

        if type(self.__image) == type(list()):
            img = self.get_frame()
        else:
            img = self.__image

        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        _lower_bound = np.array(color_hsv[0])
        _upper_bound = np.array(color_hsv[1])
        mask = cv.inRange(hsv_img, _lower_bound, _upper_bound)

        return mask

    def get_single_center_object(self, color_hsv: list[list]) -> list:
        """get an average single object based on the image 
        ! use object.get_frame() before using this function !

        Returns:
            list: [0] image, [1] a point
        """

        image = self.get_processed_frame(color_hsv)

        M = cv.moments(image)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return [image, [[cX, cY]]]
        else:
            return [image, []]

    def get_center_object(self, color_hsv: list[list]) -> list:
        """get the averange center location of the multiple object
        ! use object.get_frame() before using this function !

        Returns:
            list: [0] image, [1] detected points
        """
        image = self.get_processed_frame(color_hsv)

        contours, hierarchy = cv.findContours(image, 1, 2)
        points = list()
        for c in contours:
            M = cv.moments(c)
            area = cv.contourArea(c)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                points.append([cX, cY])

        return [image, points]

    def get_object_location_grid(self, color_hsv: list[list]) -> list:
        """find the object based on the x and y

        Args:
            image_wxh ([width, height]): aquire image height and width
            coordinates_xy ([[x0, y0], [x1, y1], ...]): lists of the detected image center

        Returns:
            list: where does the object located based on the coordinates
        |==================================================================
        |      (0,0)    |              |  |               |               |
        |               |              |  |               |               |
        |---------------|--------------|--|---------------|---------------|
        |               |              |  |               |               |
        |               |              |  |               |               |
        |---------------|--------------|--|---------------|---------------|
        |               |              |  |               |     (4,2)     |
        |               |              |  |               |               |
        |==================================================================
        """

        image, coordinates_xy = self.get_center_object(color_hsv)

        w, h = self.__camera_width, self.__camera_height
        result = list()

        def y_coord(x_segment: int, y: int) -> list:
            if y < h/3:
                return [x_segment, 0]
            elif y >= h/3 and y <= h*2/3:
                return [x_segment, 1]
            else:
                return [x_segment, 2]

        def unique(list):
            # initialize a null list
            unique_list = []

            # traverse for all elements
            for x in list:
                # check if exists in unique_list or not
                if x not in unique_list:
                    unique_list.append(x)
            return unique_list

        for coordinate_xy in coordinates_xy:
            if coordinate_xy == []:
                return []

            x, y = coordinate_xy[0], coordinate_xy[1]
            if x < w/3:
                result.append(y_coord(0, y))
            elif x >= w/3 and x < (w/2 - w/12):
                result.append(y_coord(1, y))
            elif x >= (w/2 - w/12) and x <= (w/2 + w/12):
                result.append(y_coord(2, y))
            elif x > (w/2 + w/12) and x <= w*2/3:
                result.append(y_coord(3, y))
            else:
                result.append(y_coord(4, y))
        return [image, unique(result)]

    def chase(self, color_hsv: list[list]):
        """makes the robot chase

        Args:
            coords (list): list of coords based on the picture

        Returns:
            str: one character to send to the arduino as an action
        """

        image, coordinates_xy = self.get_object_location_grid(color_hsv)

        if coordinates_xy != []:
            if self.__camera_name == 'right':
                return [image, "r"]

            if self.__camera_name == "left":
                return [image, 'l']

        if coordinates_xy == [] and self.__camera_name == "front":
            return [image, '']

        # get ball average position
        x = []

        for i in coordinates_xy:
            x.append(i[1])
        x_average = np.average(x)

        if self.__camera_name == "back":
            if x_average < 2:
                return [image, 'r']
            if x_average >= 2:
                return [image, 'l']

        if self.__camera_name == "front":
            if x_average < 2:
                return [image, 'l']
            if x_average > 2:
                return [image, 'r']
            if x_average > 2 and x_average < 2:
                return [image, 'w']

        return [image, ""]

    def avoid_line(self, color_hsv: list[list]) -> str:

        image, coordinates_xy = self.get_object_location_grid(color_hsv)

        y = filter(lambda x: x != 2, coordinates_xy[1])

        if y == []:
            return [image, ""]

        if y[0] >= 2:
            if self.__camera_name == "front":
                return [image, "s"]
            if self.__camera_name == "back":
                return [image, "w"]
            if self.__camera_name == "left":
                return [image, "r"]
            if self.__camera_name == "right":
                return [image, "l"]

        return [image, ""]

    def find_and_face_object(self, color_hsv: list[list]):
        image, descision = self.chase(color_hsv)

        if descision == "w":
            return [image, '']

        return [image, descision]

    def avoid_object(self, color_hsv: list[list]):

        pass
