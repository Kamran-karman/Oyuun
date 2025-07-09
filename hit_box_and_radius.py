from instruments import poisk_path
import arcade


class Radius(arcade.Sprite):
    def __init__(self, pers, razmer=1):
        """
        :param razmer: 1 = 1000x1000
        """
        super().__init__()

        self.pers = pers

        self.radius = arcade.load_texture("nuzhno/radius_porazheniya.png")
        self.hit_box._points = self.texture.hit_box_points

        self.scale = razmer

        self.texture = self.radius

    def check_collision(self, sprite=None, sprite_list=None):
        if sprite_list is not None:
            if arcade.check_for_collision_with_list(self, sprite_list):
                return True
            else:
                return False
        elif sprite is not None:
            if arcade.check_for_collision(self, sprite):
                return True
            else:
                return False


    def update(self) -> None:
        self.position = self.pers.position


class KvadratRadius(Radius):
    def __init__(self, pers, razmer=1):
        """
        :param razmer: 127x127
        """
        super().__init__(pers, razmer)
        self.radius = arcade.load_texture('nuzhno/kvadrat_radius.png')
        self.texture = self.radius
        self.hit_box._points = self.texture.hit_box_points

    def update(self) -> None:
        self.scale = self.pers.scale
        self.position = self.pers.position


class HitBox(Radius):
    def __init__(self, texture_pair, pers):
        super().__init__(pers)
        self.texture_pair = texture_pair
        self.pers = pers
        self.texture = self.texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.texture_pair[self.pers.storona]
        self.hit_box._points = self.texture.hit_box_points
