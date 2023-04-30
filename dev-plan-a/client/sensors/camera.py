import cv2 as cv
import numpy as np
import copy


class Camera:
    def __init__(self, camera: int, width: int, height: int, objects: dict) -> None:
        self.__camera_id = camera
        self.__camera_height = height
        self.__camera_width = width

        # initialize capture device
        self.__cap = cv.VideoCapture(camera,  cv.CAP_DSHOW)
        self.__cap.set(cv.CAP_PROP_FRAME_WIDTH, self.__camera_width)
        self.__cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.__camera_height)

        # objects dict and coords
        self.__objects = objects

    def __repr__(self) -> str:
        pass

    def __eq__(self, __value: object) -> bool:
        pass

    def get_frame(self):
        ret, img = self.__cap.read()
        if not ret:
            return f"Err in {self.__camera_id}"
        return img

    def get_processed_frame(self, color) -> np.ndarray:
        img = self.get_frame()
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        _lower_bound = np.array(color[0])
        _upper_bound = np.array(color[1])
        mask = cv.inRange(hsv_img, _lower_bound, _upper_bound)
        return mask

    def set_track_object(self, data: list) -> str:
        self.__objects[data[0]] = [data[1], data[2]]
        return f"set {data[0]} {self.__objects[data[0]]}"

    def get_track_object(self) -> dict:
        pass

    def get_single_center_object(self, image: np.ndarray) -> list:
        M = cv.moments(image)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # cv.circle(image, (cX, cY), 25, (0, 0, 0), 2)
            return [image, [cX, cY]]
        else:
            return [image, [0, 0]]

    def get_center_object(self, image: np.ndarray) -> list:
        contours, hierarchy = cv.findContours(image, 1, 2)
        points = list()
        for c in contours:
            M = cv.moments(c)
            area = cv.contourArea(c)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # cv.circle(image, (cX, cY), 2, (0, 0, 0), 5)
                points.append([cX, cY])

        return [image, points]

    def get_object_location(self, coordinates_xy: list, image_wh=list()) -> list:
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
        if image_wh == []:
            image_wh = [self.__camera_width, self.__camera_height]

        w, h = image_wh[0], image_wh[1]
        result = list()

        def y_coord(x_seg: int, y: int) -> list:
            if y < h/3:
                return [x_seg, 0]
            elif y >= h/3 and y <= h*2/3:
                return [x_seg, 1]
            elif y > h*2/3:
                return [x_seg, 2]

        def unique(list1):
            # initialize a null list
            unique_list = []

            # traverse for all elements
            for x in list1:
                # check if exists in unique_list or not
                if x not in unique_list:
                    unique_list.append(x)
            return unique_list

        for coord in coordinates_xy:
            x, y = coord[0], coord[1]
            if x < w/3:
                result.append(y_coord(0, y))
            elif x >= w/3 and x < (w/2 - w/12):
                result.append(y_coord(1, y))
            elif x >= (w/2 - w/12) and x <= (w/2 + w/12):
                result.append(y_coord(2, y))
            elif x > (w/2 + w/12) and x <= w*2/3:
                result.append(y_coord(3, y))
            elif x > w*2/3:
                result.append(y_coord(4, y))

        return unique(result)
