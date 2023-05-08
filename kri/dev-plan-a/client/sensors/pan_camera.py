import cv2 as cv
import numpy as np


class Pan_Camera:
    def __init__(self, cameras: dict) -> None:
        self.__camera_caps = dict()
        self.__image_360 = None

        for key, val in cameras.items():
            self.__camera_caps[key] = cv.VideoCapture(val, cv.CAP_DSHOW)
            self.__camera_caps[key].set(cv.CAP_PROP_FRAME_WIDTH, 1920)
            self.__camera_caps[key].set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

    def __repr__(self) -> str:
        return f"Camera({self.__camera_caps})"

    def __eq__(self, __value: object) -> bool:
        pass

    def get_360_frame(self) -> np.ndarray:
        frames = list()
        stitcher = cv.Stitcher.create()

        for key, cap in self.__camera_caps.items():

            width, height = 854, 480
            ret, frame = cap.read()

            if not ret:
                return f"Error in {key}, Message: {ret}"

            processed_frame = cv.resize(
                frame,
                (width, height),
                interpolation=cv.INTER_AREA)

            frames.append(processed_frame)

        if len(frames) > 1:
            ret, stitched_img = stitcher.stitch(frames)

            if ret:
                return f"ERR_CODE: {ret}"

            self.__image_360 = stitched_img
            return stitched_img

        else:
            return frames[0]

    def mask_image(self, lower_bound: list, upper_bound: list) -> np.ndarray:
        hsv_frame = cv.cvtColor(self.__image_360, cv.COLOR_BGR2HSV)
        mask_frame = cv.inRange(hsv_frame, lower_bound, upper_bound)
        result = cv.bitwise_and(
            self.__image_360, self.__image_360, mask=mask_frame)
        return result
