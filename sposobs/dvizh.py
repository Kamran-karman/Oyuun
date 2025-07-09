import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import sposobs
import arcade


class Dvizh(sposobs.Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.dvizh_sposob = True

        self.storona = 1

        self.dvizh_vel = 0
        self.dvizh_force = (0, 0)

        self.timer_for_s_dvizh = 0
        self.s_dvizh_func = 0

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        pass


class DvizhPers(Dvizh):
    def __init__(self, pers, sprite_list, igrok=False, **kwargs):
        super().__init__(pers, sprite_list)
        self.igrok = igrok

        self.dvizh = False
        self.timer_for_s_dvizh = 1
        self.stop_dvizh = False
        self.timer = False
        self.a = 0

    def update_storona_pers(self):
        if self.pers.storona == 1:
            self.storona = -1
        elif self.pers.storona == 0:
            self.storona = 1

    def dvizh_pers_func(self, physics_engine: arcade.PymunkPhysicsEngine):
        if self.s_dvizh_func == 0 and not self.dvizh:
            self.s_dvizh_func = 1
            self.dvizh = True
            if self.pers.dvizh or self.pers.uzhe_dvizh:
                self.pers.uzhe_dvizh = True
                self.update_storona_pers()
                if self.pers.new_force[0] < self.dvizh_force[0] or self.pers.new_force[0] < self.dvizh_force[0]:
                    for dvizh in self.pers.slovar_dvizh:
                        self.pers.slovar_dvizh[dvizh][1] = False
                    self.pers.slovar_dvizh.update({self: [0, True]})
                    physics_engine.apply_force(self.pers, (self.storona * self.dvizh_force[0], self.dvizh_force[1]))
                    self.pers.new_force = [self.dvizh_force[0] * self.storona, self.dvizh_force[1]]
                    if self.dvizh_vel > 0:
                        self.pers.pymunk.max_horizontal_velocity = self.dvizh_vel
                else:
                    self.pers.slovar_dvizh.update({self: [0, False]})
            else:
                self.pers.slovar_dvizh.update({self: [0, True]})
                self.pers.dvizh = True
                self.update_storona_pers()
                physics_engine.apply_force(self.pers, (self.storona * self.dvizh_force[0], self.dvizh_force[1]))
                self.pers.new_force = [self.dvizh_force[0] * self.storona, self.dvizh_force[1]]
                if self.dvizh_vel > 0:
                    self.pers.pymunk.max_horizontal_velocity = self.dvizh_vel

    def update_dvizh_pers(self, physics_engine: arcade.PymunkPhysicsEngine = None):
        if self.dvizh:
            self.a += 1
            if self.timer:
                self.pers.slovar_dvizh[self][0] += 1
                physics_engine.apply_force(self.pers, (self.storona * self.dvizh_force[0], self.dvizh_force[1]))
            if self.pers.slovar_dvizh[self][0] >= self.timer_for_s_dvizh or not self.timer:
                self.dvizh = False
                self.s_dvizh_func = 0
                self.pers.slovar_dvizh[self][0] = 0

                self.update_storona_pers()
                if self.pers.slovar_dvizh[self][1] or not self.pers.uzhe_dvizh:
                    self.pers.pymunk.max_horizontal_velocity = self.pers.vel_x
                    self.pers.slovar_dvizh[self][1] = False
                    self.pers.uzhe_dvizh = False
                    self.pers.dvizh = False
                    self.a = 0


class DvizhSprite(Dvizh):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.slovar_dvizh = {}

    def update_storona(self, sprite, a=0):
        if a == 1:
            if self.pers.storona == 0:
                self.storona = 1
            else:
                self.storona = -1
        elif a == 0:
            if sprite.center_x < self.pers.center_x:
                self.storona = -1
            elif sprite.center_x > self.pers.center_x:
                self.storona = 1

    def update_slovar_dvizh(self):
        if len(self.slovar_dvizh) < len(self.sprite_list):
            for sprite in self.sprite_list:
                self.slovar_dvizh.update({sprite: False})
                sprite.slovar_dvizh.update({self: [0, False]})
        while len(self.slovar_dvizh) > len(self.sprite_list):
            for sprite_dvizh in self.slovar_dvizh:
                s = 0
                for sprite in self.sprite_list:
                    if sprite == sprite_dvizh:
                        s += 1
                if s == 0:
                    self.slovar_dvizh.pop(sprite_dvizh)
                    return

    def update_dvizh_sprite(self, physics_engine: arcade.PymunkPhysicsEngine, timer=-1):
        if self.s_dvizh_func > 0:
            for sprite in self.slovar_dvizh:
                if sprite.hp > 0:
                    if timer > -1:
                        self.timer_for_s_dvizh = timer
                    if sprite.slovar_dvizh[self][1]:
                        sprite.slovar_dvizh[self][0] += 1
                        if arcade.check_for_collision_with_list(self, self.sprite_list):
                            physics_engine.apply_force(sprite, (self.storona * self.dvizh_force[0], self.dvizh_force[1]))
                        if sprite.slovar_dvizh[self][0] >= self.timer_for_s_dvizh:
                            sprite.slovar_dvizh[self][0] = 0

                            self.update_storona(sprite)
                            if sprite.slovar_dvizh[self][1] or not sprite.uzhe_dvizh:
                                sprite.pymunk.max_horizontal_velocity = sprite.vel_x
                                sprite.slovar_dvizh[self][1] = False
                                sprite.uzhe_dvizh = False
                                sprite.dvizh = False
                                self.s_dvizh_func -= 1
                                self.slovar_dvizh[sprite] = False
                #
                # if not arcade.check_for_collision_with_list(self, self.sprite_list) or not self.action:
                #     self.slovar_dvizh[sprite] = False

    def dvizh_sprite_func(self, sprite, physics_engine: arcade.PymunkPhysicsEngine, a=0):
        if not self.slovar_dvizh[sprite]:
            self.slovar_dvizh[sprite] = True
            self.s_dvizh_func += 1
            if sprite.dvizh or sprite.uzhe_dvizh:
                self.update_storona(sprite, a)
                sprite.uzhe_dvizh = True
                if sprite.new_force[0] < self.dvizh_force[0] or sprite.new_force[0] < self.dvizh_force[0]:
                    for dvizh in sprite.slovar_dvizh:
                        sprite.slovar_dvizh[dvizh][1] = False
                    sprite.slovar_dvizh.update({self: [0, True]})
                    physics_engine.apply_force(sprite, (self.storona * self.dvizh_force[0], self.dvizh_force[1]))
                    sprite.new_force = [self.dvizh_force[0] * self.storona, self.dvizh_force[1]]
                    sprite.pymunk.max_horizontal_velocity = self.dvizh_vel
                else:
                    sprite.slovar_dvizh.update({self: [0, False]})
            else:
                sprite.slovar_dvizh.update({self: [0, True]})
                sprite.dvizh = True
                self.update_storona(sprite, a)
                physics_engine.apply_force(sprite, (self.storona * self.dvizh_force[0], self.dvizh_force[1]))
                sprite.new_force = [self.dvizh_force[0] * self.storona, self.dvizh_force[1]]
                sprite.pymunk.max_horizontal_velocity = self.dvizh_vel


class DvizhPersAndSprite(DvizhPers, DvizhSprite):
    def __init__(self, pers, sprite_list, igrok=False):
        super().__init__(pers, sprite_list, igrok)
        self.s2_dvizh_func = 0

        self.slovar_dvizh = {}

        self.dvizh_force_sprite = (0, 0)
        self.dvizh_vel_sprite = 0

        self.timer_for_s_dvizh_sprite = 0

    def update_storona(self, sprite, a=0):
        if a == 1:
            if self.pers.storona == 0:
                self.storona = 1
            else:
                self.storona = -1
        elif a == 0:
            if sprite.center_x < self.pers.center_x:
                self.storona = -1
            elif sprite.center_x > self.pers.center_x:
                self.storona = 1

    def update_slovar_dvizh(self):
        if len(self.slovar_dvizh) < len(self.sprite_list):
            for sprite in self.sprite_list:
                self.slovar_dvizh.update({sprite: False})
                sprite.slovar_dvizh.update({self: [0, False]})
        while len(self.slovar_dvizh) > len(self.sprite_list):
            for sprite_dvizh in self.slovar_dvizh:
                s = 0
                for sprite in self.sprite_list:
                    if sprite == sprite_dvizh:
                        s += 1
                if s == 0:
                    self.slovar_dvizh.pop(sprite_dvizh)

                    return

    def update_dvizh_sprite(self, physics_engine: arcade.PymunkPhysicsEngine, timer=-1):
        if self.s2_dvizh_func > 0:
            for sprite in self.slovar_dvizh:
                if sprite.hp > 0:
                    if timer > -1:
                        self.timer_for_s_dvizh_sprite = timer
                    if sprite.slovar_dvizh[self][1]:
                        sprite.slovar_dvizh[self][0] += 1
                        # if arcade.check_for_collision_with_list(self, self.sprite_list):
                        #     print(sprite.slovar_dvizh[self][0])
                        #     physics_engine.apply_force(sprite, (self.storona * self.dvizh_force_sprite[0],
                        #                                         self.dvizh_force_sprite[1]))
                        if sprite.slovar_dvizh[self][0] >= self.timer_for_s_dvizh_sprite:
                            sprite.slovar_dvizh[self][0] = 0

                            self.update_storona(sprite)
                            if sprite.slovar_dvizh[self][1] or not sprite.uzhe_dvizh:
                                sprite.pymunk.max_horizontal_velocity = sprite.vel_x
                                sprite.slovar_dvizh[self][1] = False
                                sprite.uzhe_dvizh = False
                                sprite.dvizh = False
                                self.s2_dvizh_func -= 1
                                self.slovar_dvizh[sprite] = False

                # if not arcade.check_for_collision(self, sprite) or not self.action:
                #     self.slovar_dvizh[sprite] = False
                #     print(arcade.check_for_collision(self, sprite))

    def dvizh_sprite_func(self, sprite, physics_engine: arcade.PymunkPhysicsEngine, a=0):
        if not self.slovar_dvizh[sprite]:
            self.slovar_dvizh[sprite] = True
            self.s2_dvizh_func += 1
            if sprite.dvizh or sprite.uzhe_dvizh:
                self.update_storona(sprite, a)
                sprite.uzhe_dvizh = True
                if sprite.new_force[0] < self.dvizh_force_sprite[0] or sprite.new_force[0] < self.dvizh_force_sprite[0]:
                    for dvizh in sprite.slovar_dvizh:
                        sprite.slovar_dvizh[dvizh][1] = False
                    sprite.slovar_dvizh.update({self: [0, True]})
                    physics_engine.apply_force(sprite, (self.storona * self.dvizh_force_sprite[0],
                                                        self.dvizh_force_sprite[1]))
                    sprite.new_force = [self.dvizh_force_sprite[0] * self.storona, self.dvizh_force_sprite[1]]
                    sprite.pymunk.max_horizontal_velocity = self.dvizh_vel_sprite
                else:
                    sprite.slovar_dvizh.update({self: [0, False]})
            else:
                sprite.slovar_dvizh.update({self: [0, True]})
                sprite.dvizh = True
                self.update_storona(sprite, a)
                physics_engine.apply_force(sprite, (self.storona * self.dvizh_force_sprite[0],
                                                    self.dvizh_force_sprite[1]))
                sprite.new_force = [self.dvizh_force_sprite[0] * self.storona, self.dvizh_force_sprite[1]]
                sprite.pymunk.max_horizontal_velocity = self.dvizh_vel_sprite

