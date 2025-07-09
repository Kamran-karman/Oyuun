import arcade
from arcade import Camera

STATE0 = 0
STATE1 = 1
STATE2 = 2
STATE3 = 3
STATE4 = 4


class Line:

    DEFAULT_COLORS = {
        STATE0: (102, 205, 170, 255),
        STATE1: (50, 190, 50, 255),
        STATE2: (255, 215, 0, 255),
        STATE3: (255, 165, 0, 255),
        STATE4: (255, 25, 0, 255)
    }

    def __init__(self, max_znach: float, otnos_start: float, otnos_end: float, otnos_flatness: float,
                 kamera: Camera, line_width=30, colors=None):
        self.name = ''

        self.max_znach = max_znach
        self.otnos_start = otnos_start
        self.otnos_end = otnos_end
        self.otnos_flatness = otnos_flatness
        self._start = 0
        self._end = 0
        self._flatness = 0
        self.colors = colors or self.DEFAULT_COLORS
        self.line_width = line_width
        self.znach = self.max_znach
        self._kamera = kamera

        self.__dlina = abs(self.otnos_start - self.otnos_end)
        self.__attitude = self.__dlina / self.max_znach

        self.state = STATE1

    def update(self, znach: float, x: float, y: float):
        self._start = self.otnos_start + x + 67
        self._end = self.otnos_end + x + 67
        self._flatness = self.otnos_flatness + y - 125
        if self.znach > znach:
            raznica = self.znach - znach
            self.otnos_end -= raznica * self.__attitude
            self.znach = znach
        elif self.znach < znach:
            raznica = znach - self.znach
            self.otnos_end += raznica * self.__attitude
            self.znach = znach

        if round(self.otnos_end - self.otnos_start, 4) > self.__dlina:
            self.state = STATE0
        elif self.__dlina >= round(self.otnos_end - self.otnos_start, 4) > self.__dlina * 0.75:
            self.state = STATE1
        elif self.__dlina * 0.75 >= round(self.otnos_end - self.otnos_start, 4) > self.__dlina * 0.5:
            self.state = STATE2
        elif self.__dlina * 0.5 >= round(self.otnos_end - self.otnos_start, 4) > self.__dlina * 0.25:
            self.state = STATE3
        elif self.__dlina * 0.25 >= round(self.otnos_end - self.otnos_start, 4):
            self.state = STATE4

    def draw(self):
        color = 0
        for state in self.colors:
            if state == self.state:
                color = state

        arcade.draw_line(self._start, self._flatness, self._end, self._flatness, self.colors[color],
                         self.line_width * self._kamera.zoom)


class LineList:
    def __init__(self):
        self.__line_list: list[Line] = []
        self.znach: float = 0

    def draw(self):
        for line in self.__line_list:
            line.draw()

    def update(self, x: float, y: float, znach_slovar: dict[str:float] = dict):
        if len(znach_slovar) != 0:
            for line in self.__line_list:
                line.update(znach_slovar[line.name], x, y)
        else:
            for line in self.__line_list:
                line.update(self.znach, x, y)

    def append(self, line: Line):
        if line in self.__line_list:
            raise ValueError("Line уже есть в LineList.\nLine already in LineList")

        self.__line_list.append(line)

