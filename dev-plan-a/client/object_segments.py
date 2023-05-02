
def find(image_wh: list, coordinates_xy: list) -> list:
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
