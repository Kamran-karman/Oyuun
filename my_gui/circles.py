import arcade
from arcade import Texture
import sposobs
import instruments


class Circle:
    def __init__(self, sposob: sposobs.Sposob, radius: float, center_x: float, center_y: float, texture: Texture):
        super().__init__()
        self.sposob = sposob
        self.radius = radius
        self.__angle = 360
        self.__attitude = 360 / self.sposob.timer_for_s_kd
        self.center_x = center_x
        self.center_y = center_y
        self.texture = texture

        self._s_kd = ''
        self.__text = arcade.Text(self._s_kd, 0, 0, font_size=16, width=30, align='center',
                                  font_name='Comic Sans MS')

    def draw(self, x, y):
        arcade.draw_arc_filled(self.center_x + x, self.center_y + y, self.radius, self.radius, (0, 0, 0, 100), 0, 0)
        arcade.draw_texture_rectangle(self.center_x + x, self.center_y + y, self.radius, self.radius, self.texture)
        if self.sposob.kd:
            arcade.draw_arc_filled(self.center_x + x, self.center_y + y, self.radius, self.radius, (0, 0, 0, 100),
                                   0, self.__angle)
            self.__text.text = self._s_kd
            self.__text.x = self.center_x + x - 15
            self.__text.y = self.center_y + y - 8
            self.__text.draw()

    def update(self):
        if self.sposob.kd:
            if ((self.sposob.timer_for_s_kd - self.sposob.s_kd) / 60) >= 1:
                self._s_kd = str(int((self.sposob.timer_for_s_kd - self.sposob.s_kd) / 60))
            else:
                self._s_kd = str(round((self.sposob.timer_for_s_kd - self.sposob.s_kd) / 60, 1))
            self.__angle = self.__attitude * (self.sposob.timer_for_s_kd - self.sposob.s_kd)
        else:
            self.__angle = 360
            self._s_kd = ''

    def _correct_attitude(self):
        self.__attitude = 360 / self.sposob.timer_for_s_kd


class Circles:
    def __init__(self, radius: float):
        self.__circle_list: list[Circle] = []
        self.radius = radius

    def __setitem__(self, key, value):
        self.__circle_list[key] = value

    def __getitem__(self, item):
        return self.__circle_list[item]

    def __len__(self):
        return len(self.__circle_list)

    def draw(self, x, y):
        for circle in self.__circle_list:
            circle.draw(x, y)

    def update(self):
        for circle in self.__circle_list:
            circle.update()

    def create_circles(self, sposobs_list: arcade.SpriteList, center_x: float, center_y: float, rasst: float,
                       textures_list: instruments.TextureList):
        s = 0
        for sposob in sposobs_list:
            circle = Circle(sposob, self.radius, center_x, center_y, textures_list[s])
            self.__circle_list.append(circle)
            center_x += rasst
            s += 1

    def set_sposob(self, key: int, sposob: sposobs.Sposob, texture: Texture):
        self.__circle_list[key].sposob = sposob
        self.__circle_list[key].texture = texture
        self.__circle_list[key]._correct_attitude()
