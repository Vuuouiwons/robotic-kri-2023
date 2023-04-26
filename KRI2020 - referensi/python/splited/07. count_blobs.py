import cv2 as cv


class ImageProcessingWidget(object):

    def __init__(self, maskfile, ballfile):
        self.mask = cv.imread(maskfile, 0)
        self.ball = cv.imread(ballfile, 0)

    def show_all_img(self):
        cv.imshow('mask img', self.mask)
        cv.imshow('ball img', self.ball)
        cv.imshow('ballmasked img', self.ballmasked)

    def masking(self):
        self.ball = cv.line(self.ball,
                            (235, 171),
                            (275, 70), 255, 10)
        self.ballmasked = cv.bitwise_and(self.mask, self.ball)

    def get_total_blobs(self):
        cnts = cv.findContours(
            self.ballmasked, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        blobs = 0
        for c in cnts:
            area = cv.contourArea(c)
            cv.drawContours(self.ballmasked, [c], -1, (255, 255, 255), -1)
            if area > 30:
                blobs += 1

        return blobs


def main():
    imgwidget = ImageProcessingWidget('img/lapangan.png', 'img/bolamask.png')

    imgwidget.masking()

    print(imgwidget.get_total_blobs())
    imgwidget.show_all_img()

    key = cv.waitKey(0)
    if key == ord('q'):
        cv.destroyAllWindows()


main()
