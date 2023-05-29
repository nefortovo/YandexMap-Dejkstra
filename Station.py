
class Station:
    def __init__(self, id, true_id,x, y, color):
        self.__id = id
        self.__true_id = true_id
        self.__x = x
        self.__y = y
        self.__color = color
        self.__to = set()
        self.__weight = 1

    def get_true_id(self):
        return self.__true_id

    def add_way(self, to):
        self.__to.add(to)

    def get_id(self):
        return self.__id

    def get_ways(self):
        return self.__to

    def get_way_count(self):
        return len(self.__to)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_color(self):
        return self.__color

    def get_color(self):
        return self.__weight