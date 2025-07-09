import os
import sys
from typing import Any

import instruments
from sposobs.stihiya.voda.voda_h import TIMER_FOR_S_OBRAT, TIMER_FOR_S_VERTIK, VERTIK_CHANGE_Y, POGRESHOST, VERTIK_KOEF, \
    VVERH_KOEF, VVERH_CHANGE_Y, SUMMA_RAZNICA, VVERH_RAZNICA, VERTIK_ANGLE, VVERH_ANGLE, FALL_CHANGE, \
    FIRST_GRANICA_Y_EJECTION, FIRST_CHANGE_Y_EJECTION, SECOND_GRANICA_Y_EJECTION, SECOND_CHANGE_Y_EJECTION, \
    THIRD_GRANICA_Y_EJECTION, THIRD_CHANGE_Y_EJECTION, ELSE_CHANGE_Y_EJECTION, CHANGE_X_EJECTION

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import arcade
import sposobs
from sposobs import stihiya, dvizh
import arcade.texture.transforms
from sposobs.stihiya.voda import voda_h

V_LIST = []
'''list[str]'''

class Voda(stihiya.Stihiya):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list)
        self.voda = True
        self.podklass = sposobs.VODA

        self.minus_v = self.minus_max_v = minus_v
        self.v_max_minus = False
        self.s_v_max_minus = 0
        self.kritik = False

    def update_v(self):
        if self.s == 1:
            s = 0
            for pers in V_LIST:
                if pers.v >= self.minus_v and pers == self.pers:
                    pers.v -= self.minus_v
                else:
                    s += 1

            if s == len(V_LIST):
                if self.action and self.pers.name == "Oyuun":
                    print(self.pers)
                self.action = False
                self.s += self.timer_for_s

        for pers in V_LIST:
            if self.v_max_minus and self.s_v_max_minus == 0:
                self.s_v_max_minus = 1
                pers.v_max -= self.minus_max_v
                pers.v -= self.minus_max_v
            elif not self.v_max_minus and self.s_v_max_minus == 1:
                self.s_v_max_minus = 0
                pers.v_max += self.minus_max_v
                pers.v += self.minus_max_v
            elif self.v_max_minus and self.s_v_max_minus == 1 and pers.kritik:
                self.v_max_minus = False
                self.s_v_max_minus = 0
                pers.v_max += self.minus_max_v
                pers.v += self.minus_max_v

            if pers.v < 0:
                pers.v *= 0

            if pers.v < pers.v_max:
                pers.v += pers.v_plus
            elif pers.v > pers.v_max:
                pers.v = pers.v_max

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        if self.pers.block.block:
            self.action = False

    # def func_for_init(self):
    #     self.scale = self.minus_v / 100


class VodaFight(Voda, stihiya.StihiyaFight, dvizh.DvizhSprite):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.tip = sposobs.VODA_FIGHT

        self.degree_block = 0.2
        self.force_for_block = -1
        self.minus_for_block = -1
        self.probit_block = True

        self.minus_max_v = 0
        self.v_max_minus = False
        self.s_v_max_minus = 0
        self.kritik = False

    def sbiv(self, sprite):
        if not sprite.smert:
            sprite.sbiv = True
            sprite.fizika.update_poly = True
            # sprite.position_new = True
            # sprite.new_position = (sprite.center_x, 160)


class VodaBlock(Voda, stihiya.StihiyaBlock):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.tip = sposobs.VODA_BLOCK

        self.s_block_texture = 0
        self.block_texture_list = []

        self.s_body_type = 0

        self.fizika = None

    def block_animation(self, speed=0.1):
        if self.avto_block:
            self.texture = self.pers.animations.jump_texture[self.pers.storona]
        elif self.block:
            if self.s_block_texture < 2:
                self.texture = self.block_texture_list[round(self.s_block_texture)][self.pers.storona]
                self.hit_box._points = self.texture.hit_box_points
                self.s_block_texture += speed
            else:
                self.texture = self.block_texture[self.pers.storona]
                self.hit_box._points = self.texture.hit_box_points
            self.draw()
        else:
            self.s_block_texture = 0


class VodaImitation(VodaFight, stihiya.StihiyaImitation):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.podtip = sposobs.VODA_IMITATION

        self.baff_uron = 3
        self.kombo_baff_uron = 6

        self.kombo_texture_list = instruments.TextureList()
        self.obich_texture = None
        self.kol_vo_udar_textures = 0
        self.kol_vo_kombo_textures = 0

        self.kombo = False
        self.s_kombo = 0
        self.s_kombo_texture = 0
        self.s_udar_texture = -1
        self.kol_vo_udars = 0
        self.sprite_udar = arcade.Sprite()

        self.fight = False

    def update_kombo(self):
        if self.s == 1:
            self.func_mana()
        if self.kombo:
            self.s = 3

        if not self.action:
            self.sprite_udar = arcade.Sprite()
            if self.s_kombo >= self.kol_vo_udars:
                self.s_kombo = 0
                self.kombo = True

    def atak(self, sprite, physics_engine: arcade.PymunkPhysicsEngine):
        if self.sprite_udar != sprite:
            if not self.kombo:
                self.s_kombo += 1
            self.sprite_udar = sprite
        if self.kombo:
            if self.s_kombo_texture < 3:
                self.udar(sprite, self.uron * self.baff_uron)
            else:
                self.udar(sprite, self.uron * self.kombo_baff_uron)
        else:
            self.udar(sprite)
        self.oglush(sprite)
        self.dvizh_sprite_func(sprite, physics_engine)


class VodoHod(VodaFight):
    def __init__(self, pers, sprite_list, minus_v, igrok=False):
        super().__init__(pers, sprite_list, minus_v)
        self.podtip = sposobs.VODOHOD
        self.igrok = igrok

        self.storona = 0

        self.obrat = False
        self.s_obrat = 0
        self.timer_for_s_obrat = TIMER_FOR_S_OBRAT
        self.s_vertik = 0
        self.timer_for_s_vertik = TIMER_FOR_S_VERTIK
        self.vverh = False
        self.vertik = False
        self.big = False

        self.fizika: arcade.PymunkPhysicsEngine = Any

        self.otnos = 0
        self.point = (0, 0)
        self.pred_change_x = 0

    def hod(self, change_x, walls_list):
        if self.pers.oglush:
            self.action = False
        if self.action:
            def obich():
                self.s_vertik = 0
                self.vverh = self.vertik = self.big = False
                self.change_x = change_x

            def vertik_func():
                self.vverh = self.vertik = True
                self.change_y = VERTIK_CHANGE_Y

            def set_angle(angle: int):
                if self.pers.storona == 1:
                    self.pers.angle = self.angle = angle
                else:
                    self.pers.angle = self.angle = -angle

            height = self.height / 4
            if change_x > 0:
                self.storona = 0
            elif change_x < 0:
                self.storona = 1

            if self.storona == 0:
                self.point = (self.right, self.center_y - height)
            else:
                self.point = (self.left, self.center_y - height)

            self.pers.oglush_for_sposob = True

            nearest_wall_list = instruments.nearest(self.point, walls_list, 7)
            near_wall = nearest_wall_list[0]
            if near_wall.top < self.center_y - height:# and abs(near_wall.top - (self.center_y - height)) > 3:
                for i in range(1, 3):
                    if nearest_wall_list[i].height > near_wall.height and near_wall.center_y < nearest_wall_list[i].center_y:
                        near_wall = nearest_wall_list[i]

            if self.pred_change_x != change_x and self.pred_change_x != 0 and self.vertik:
                self.vertik = False
                self.obrat = True
                self.s_obrat = 0
            if change_x != 0:
                self.pred_change_x = change_x

            if self.obrat:
                self.vverh = True
                self.change_x = change_x
                self.s_obrat += 1
                if self.s_obrat >= self.timer_for_s_obrat:
                    self.s_obrat = 0
                    self.obrat = False

            if not self.obrat:
                if change_x != 0:
                    height = self.height / 2

                    if near_wall.top > self.center_y - height / 2 and abs(
                            near_wall.top - (self.center_y - height / 2)) > POGRESHOST:
                        if near_wall.height >= height * VERTIK_KOEF and arcade.check_for_collision_with_list(self, walls_list):
                            self.big = True
                            if abs(near_wall.top - (self.center_y - height / 2)) <= height * VVERH_KOEF:
                                self.vverh = True
                                self.vertik = False
                                self.change_x = change_x
                                self.change_y = VVERH_CHANGE_Y
                            else:
                                vertik_func()
                                self.change_x = change_x
                        elif near_wall.height >= height * VVERH_KOEF and arcade.check_for_collision_with_list(self, walls_list):
                            self.big = False
                            self.vverh = True
                            self.vertik = False
                            self.change_x = change_x
                            self.change_y = VVERH_CHANGE_Y
                        else:
                            obich()
                    else:
                        obich()

                    if self.vverh and not self.big:
                        summa = near_wall.height
                        nearest_wall_list.remove(near_wall)
                        s = 0
                        for i in range(len(nearest_wall_list)):
                            if (near_wall.center_y < nearest_wall_list[i].center_y
                                    and abs(near_wall.center_x - nearest_wall_list[i].center_x) < SUMMA_RAZNICA):
                                summa += nearest_wall_list[i].height
                                s += 1

                        nearest_wall_list.append(near_wall)

                        if summa > height * VERTIK_KOEF:
                            vertik_func()
                else:
                    obich()

            if self.vverh:
                raznica = VVERH_RAZNICA
                if self.vertik:
                    self.s_vertik += 1
                    if self.s_vertik >= self.timer_for_s_vertik and arcade.check_for_collision(near_wall, self):
                        self.change_x = 0
                        set_angle(VERTIK_ANGLE)
                    else:
                        if self.s_vertik < self.timer_for_s_vertik:
                            set_angle(VVERH_ANGLE)
                else:
                    self.s_vertik = 0
                    set_angle(VVERH_ANGLE)
            else:
                raznica = 0
                self.pers.angle = self.angle = 0
                if not arcade.check_for_collision_with_list(self, walls_list):
                    if self.change_y >= 0:
                        self.change_y = FALL_CHANGE
                else:
                    for wall in walls_list:
                        if wall.center_y < self.center_y and abs(wall.top - self.bottom) >= POGRESHOST and arcade.check_for_collision(self, wall): #  and abs(self.center_x - wall.center_x) < 10:
                            if abs(wall.top - self.bottom) < FIRST_GRANICA_Y_EJECTION:
                                self.change_y = FIRST_CHANGE_Y_EJECTION
                            elif SECOND_GRANICA_Y_EJECTION > abs(wall.top - self.bottom) >= FIRST_CHANGE_Y_EJECTION:
                                self.change_y = SECOND_CHANGE_Y_EJECTION
                            elif THIRD_GRANICA_Y_EJECTION > abs(wall.top - self.bottom) >= SECOND_GRANICA_Y_EJECTION:
                                self.change_y = THIRD_CHANGE_Y_EJECTION
                            else:
                                self.change_y = ELSE_CHANGE_Y_EJECTION
                            break
                        else:
                            self.change_y = 0

            if (arcade.check_for_collision(self, near_wall) and ((self.storona == 0 and
                abs(self.right - near_wall.left) > raznica) or (self.storona == 1 and abs(self.left - near_wall.right) > raznica))
                and near_wall.center_y > self.bottom) and not self.obrat:
                if self.vverh:
                    self.change_x = 0
                else:
                    if self.storona == 0:
                        self.change_x = -CHANGE_X_EJECTION
                    else:
                        self.change_x = CHANGE_X_EJECTION

    def update_pers_body_type(self):
        if self.action:
            self.pers.position = self.position
            self.s_kd = 0
            if self.s == 0:
                self.fizika.remove_sprite(self.pers)
                # self.fizika.sprites[self.pers].body.body_type = self.fizika.KINEMATIC
            self.s += 1
        else:
            self.s = 0
            self.s_kd += 1
            if self.s_kd == 1:
                self.pers.angle = 0
                self.fizika.add_sprite(self.pers, 1, 1,
                                       max_vertical_velocity=2000,
                                       max_horizontal_velocity=300,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.fizika = physics_engine
        self.update_sposob()
        self.update_v()
        self.update_mor()
        self.update_pers_body_type()

        if self.action and not self.kritik:
            self.pers.toggle = True
            self.func_mana()
            self.v_max_minus = True

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and self.change_x != 0:
                    self.oglush(sprite)
                    self.dvizh_sprite_func(sprite, physics_engine, 1)
                    self.udar(sprite)
                    self.sbiv(sprite)
        else:
            self.pers.angle = self.angle = 0
            self.pers.toggle = False
            self.bottom = self.pers.bottom
            self.center_x = self.pers.center_x
            self.v_max_minus = False

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)

