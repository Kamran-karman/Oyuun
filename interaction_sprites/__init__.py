import arcade
import pymunk


class InteractionSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.name = ''

        self.animations = None


class DvizhInteractionSprite(InteractionSprite):
    def __init__(self):
        super().__init__()
        self.walk = False
        self.beg = False
        self.kast_scena = False

        self.storona = 0

    def _update_storona(self, speed_x, x_d_zone=0):
        if speed_x < -x_d_zone and self.storona == 0:
            self.storona = 1
        elif speed_x > x_d_zone and self.storona == 1:
            self.storona = 0


class DialogSprite(InteractionSprite):
    def __init__(self):
        super().__init__()
        self.speak = False
        self.sulky = False
        self.ulibka = False


class DopFizikaInSprite:
    def __init__(self, sprite: DvizhInteractionSprite, walls_list: arcade.SpriteList):
        self.__sprite = sprite
        self.walls_list = walls_list

        self.x_odometr = 0
        self.is_on_ground = False
        self.in_air = False
        self.dx = 0
        self.dy = 0

        self.fizika = arcade.PymunkPhysicsEngine()

        self.update_poly = False

        self.__rasst = 40

        self.__prizem = False
        self.__s_prizem = 0
        self.__max_s_prizem = 60

        self.__s = 0
        self.__timer_for_s = 10

    def update(self, physics_engine: arcade.PymunkPhysicsEngine, dx, dy):
        self.fizika = physics_engine
        self.x_odometr += dx
        self.is_on_ground = physics_engine.is_on_ground(self.__sprite)
        self.dx = dx
        self.dy = dy
        if abs(dy) >= 3 and not self.is_on_ground:
            self.in_air = True
        elif self.is_on_ground:
            self.in_air = False

        self.__update_prizem(physics_engine)

        # if abs(dx) < 0.005:
        if self.update_poly:
            self.__update_poly(physics_engine)
            self.update_poly = False

        self.__s += 1
        if self.__s >= self.__timer_for_s:
            self.__s = 0
            self.__update_poly(physics_engine)
        # else:
        #     self.__s = 0

    def __update_prizem(self, physics_engine: arcade.PymunkPhysicsEngine):
        for wall in self.walls_list:
            if not self.is_on_ground and not self.__prizem:
                rasst = abs(wall.top - self.__sprite.bottom)
                if rasst <= self.__rasst:
                    self.__prizem = True
                    break

        if self.__prizem:
            self.__update_poly(physics_engine)
            if self.is_on_ground:
                self.__s_prizem += 1
                if self.__s_prizem >= self.__max_s_prizem:
                    self.__prizem = False
                    self.__s_prizem = 0

    def __update_poly(self, physics_engine: arcade.PymunkPhysicsEngine):
        physics_object = physics_engine.sprites[self.__sprite]
        poly = self.__sprite.hit_box.points
        scaled_poly = [[x * self.__sprite.scale for x in z] for z in poly]
        shape = pymunk.Poly(physics_object.body, scaled_poly, radius=0)
        shape.friction = physics_object.shape.friction
        shape.elasticity = physics_object.shape.elasticity
        shape.collision_type = physics_object.shape.collision_type
        new_physics_object = arcade.PymunkPhysicsObject(physics_object.body, shape)
        physics_engine.sprites[self.__sprite] = new_physics_object
        physics_engine.space.remove(physics_object.shape)
        physics_engine.space.add(shape)
