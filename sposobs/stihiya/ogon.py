import math
import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import arcade
import sposobs
from sposobs import stihiya
from sposobs.dvizh import DvizhPers


class Ogon(stihiya.StihiyaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.podklass = sposobs.OGON
        self.ogon = True

        self.tik_uron = 0
        self.timer_for_s_tik = 0
        self.interval = 30
        self.v = 0

    def tik(self, sprite):
        s = 0
        for sposob in sprite.tik_slovar:
            if sposob == self.sposob:
                sprite.tik_slovar[sposob][0] = True
                s += 1

        if s == 0:
            sprite.tik_slovar.update({self.sposob: [True, 0]})

    def update_tik(self):
        for sprite in self.sprite_list:
            for sposob in sprite.tik_slovar:
                if sposob == self.sposob and sprite.tik_slovar[sposob][0]:
                    sprite.tik_slovar[sposob][1] += 1
                    if sprite.tik_slovar[sposob][1] % self.interval == 0:
                        sprite.hp -= self.tik_uron
                    if sprite.tik_slovar[sposob][1] >= self.timer_for_s_tik:
                        sprite.tik_slovar[sposob][0] = False
                        sprite.tik_slovar[sposob][1] = 0


class FireBall(Ogon):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.FIRE_BALL

        self.uron = 100
        self.tik_uron = 10
        self.minus_mana = 5
        self.change = 20
        self.v = 3

        self.kast = False
        self.timer_for_s_kast = 30
        self.s_kast = 0
        self.timer_for_s = 120 + self.timer_for_s_kast
        self.timer_for_s_kd = 240
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_tik = 90

        self.tex = arcade.load_texture_pair('nuzhno/fire_ball.png')
        self.scale = 0.1
        self.texture = self.tex[0]
        self.storona = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        # if self.action:
        #     print(1)
        self.update_mor()
        # if self.action:
        #     print(2)

        if self.pers.oglush and self.s_kast <= self.timer_for_s_kast:
            self.s_kast = 0
            self.s += self.timer_for_s * 2
            self.change_x = 0
            self.scale = 0.1
        # if self.action:
        #     print(3)

        self.kd_timer_mana()
        # if self.action:
        #     print(4)

        if self.action:
            if self.s == 1:
                self.func_mana()
            self.s_kast += 1
            if self.s_kast <= self.timer_for_s_kast:
                self.kast = True
                if self.pers.storona == 0:
                    self.storona = 1
                else:
                    self.storona = -1
                self.pers.stan_for_sposob = True
                self.update_position()
                self.scale += 0.03
            else:
                self.kast = False
                self.pers.stan_for_sposob = False

                self.change_x = self.change * self.storona

                for sprite in self.sprite_list:
                    if ((((not sprite.fight and arcade.check_for_collision(self, sprite))
                          or (sprite.fight and arcade.check_for_collision(self, sprite.hit_box_2)))
                            or (sprite.block.block or sprite.block.avto_block)
                         and arcade.check_for_collision(sprite.block, self)
                         and sprite.block.podtip != sposobs.VODA_IMITATION) and sprite.hp > 0):
                        self.tik(sprite)
                        self.change_x = 0
                        self.s += self.timer_for_s
                        self.udar_or_block(sprite)
                        self.s_kast = 0
                        self.scale = 0.1
        else:
            self.pers.stan_for_sposob = False
            self.kast = False
            self.s_kast = 0
            self.change_x = 0
            self.scale = 0.1
            self.update_position()

        self.update_tik()
        self.update_slovar()


class MiniFireBall(Ogon):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.MINI_FIRE_BALL

        self.uron = 10
        self.tik_uron = 1
        self.change = 15
        self.minus_mana = 1
        self.v = 1

        self.timer_for_s_zaryad = 15
        self.s_zaryad = 0
        self.timer_for_s = 45 + self.timer_for_s_zaryad
        self.timer_for_s_kd = 30
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_tik = 60

        self.tex = arcade.load_texture_pair('nuzhno/mini_fire_ball.png')
        self.scale = 0.1
        self.storona = 1
        self.texture = self.tex[1]

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor()
        if self.pers.oglush and self.s_zaryad <= self.timer_for_s_zaryad:
            self.s_zaryad = 0
            self.s += self.timer_for_s * 2
            self.change_x = 0
            self.scale = 0.1
        self.kd_timer_stamina()

        if self.s == 1:
            self.func_mana()

        if self.action:
            self.s_zaryad += 1
            if self.s_zaryad <= self.timer_for_s_zaryad:
                self.pers.stan_for_sposob = True
                if self.pers.storona == 1:
                    self.storona = -1
                else:
                    self.storona = 1
                self.update_position()
                self.scale += 0.06
            else:
                self.pers.stan_for_sposob = False
                self.change_x = self.change * self.storona

                for sprite in self.sprite_list:
                    if ((((not sprite.fight and arcade.check_for_collision(self, sprite))
                          or (sprite.fight and arcade.check_for_collision(self, sprite.hit_box_2)))
                            or (sprite.block.block or sprite.block.avto_block)
                         and arcade.check_for_collision(sprite.block, self)
                         and sprite.block.podtip != sposobs.VODA_IMITATION) and sprite.hp > 0):
                        self.tik(sprite)
                        self.change_x = 0
                        self.s_zaryad = 0
                        self.scale = 0.1
                        self.s += self.timer_for_s
                        self.udar_or_block(sprite)
        else:
            self.s_zaryad = 0
            self.update_position()
            self.change_x = 0
            self.scale = 0.1
            self.s_zaryad = 0

        self.update_tik()
        self.update_slovar()


class YazikiOgnya(Ogon):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.YAZIKI_OGNYA

        self.uron = 35
        self.tik_uron = 20
        self.minus_mana = 15

        self.timer_for_s = 180
        self.timer_for_s_kd = 420
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_tik = 120

        self.tex = arcade.load_texture_pair('nuzhno/fire_ball.png')
        self.texture = self.tex[1]
        self.normal_scale_xy = self.scale_xy
        self.max_widht = 530
        self.vr_widht = self.width
        self.stopp = False

    def update_potok(self):
        for sprite in self.sprite_list:
            for block in sprite.block_list:
                if arcade.check_for_collision(block, self) and (block.block or block.avto_block):
                    self.stopp = True
                    if self.center_x <= sprite.center_x:
                        self.vr_widht = abs(sprite.left - self.left)
                    else:
                        self.vr_widht = abs(self.right - sprite.right)
                    break
                else:
                    self.stopp = False

        if self.width <= self.max_widht and not self.stopp:
            self.scale_xy = (self.scale_xy[0] + 0.5, self.scale_xy[1])
        elif self.stopp:
            self.width = self.vr_widht
        if self.pers.storona == 0:
            self.left = self.pers.center_x
        else:
            self.right = self.pers.center_x
        self.center_y = self.pers.center_y

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor()
        self.kd_timer_mana()
        if self.pers.oglush:
            self.s += self.timer_for_s
            self.pers.stan_for_sposob = False
            self.scale_xy = self.normal_scale_xy
            self.update_position()

        if self.action:
            self.pers.stan_for_sposob = True
            if self.s == 1:
                self.func_mana()

            self.update_potok()

            # if self.width <= self.max_widht and not self.stopp:
            #     self.scale_xy = (self.scale_xy[0] + 0.5, self.scale_xy[1])
            #     self.vr_widht = self.width
            # if self.pers.storona == 0:
            #     self.left = self.pers.center_x
            # else:
            #     self.right = self.pers.center_x
            # self.center_y = self.pers.center_y

            for sprite in self.sprite_list:
                if ((((not sprite.fight and arcade.check_for_collision(self, sprite))
                          or (sprite.fight and arcade.check_for_collision(self, sprite.hit_box_2)))
                            or (sprite.block.block or sprite.block.avto_block)
                         and arcade.check_for_collision(sprite.block, self)
                         and sprite.block.podtip != sposobs.VODA_IMITATION) and sprite.hp > 0):
                    if self.s % 15 == 0:
                        sprite.tik_slovar[self.sposob][1] = 0
                        self.tik(sprite)
                        self.udar_or_block(sprite, popal=False)
        else:
            self.stopp = False
            self.pers.stan_for_sposob = False
            self.scale_xy = self.normal_scale_xy
            self.update_position()

        self.update_tik()
        self.update_slovar()


class KulakOgnya(Ogon):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.KULAK_OGNYA
        self.uron = 40
        self.tik_uron = 10
        self.minus_mana = 3
        self.change = 15

        self.kast = False
        self.s_kast = 0
        self.timer_for_s_kast = 5
        self.timer_for_s = 45 + self.timer_for_s_kast
        self.timer_for_s_kd = 60
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_tik = 90

        self.tex = arcade.load_texture_pair('nuzhno/fire_ball.png')
        self.scale_xy = (self.scale_xy[0] + 3, self.scale_xy[1])
        self.texture = self.tex[1]
        self.storona = 0

        self.radius.scale = 0.5

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor()
        self.kd_timer_mana()
        self.radius.position = self.pers.position

        if self.action:
            if self.s == 1:
                self.func_mana()

            self.s_kast += 1
            if self.s_kast <= self.timer_for_s_kast:
                self.kast = True
                if self.pers.storona == 0:
                    self.storona = 1
                else:
                    self.storona = -1
                self.update_position()
            else:
                self.kast = False
                self.change_x = self.change * self.storona

                for sprite in self.sprite_list:
                    if ((((not sprite.fight and arcade.check_for_collision(self, sprite))
                          or (sprite.fight and arcade.check_for_collision(self, sprite.hit_box_2)))
                            or (sprite.block.block or sprite.block.avto_block)
                         and arcade.check_for_collision(sprite.block, self)
                         and sprite.block.podtip != sposobs.VODA_IMITATION) and sprite.hp > 0):
                        self.tik(sprite)
                        self.udar_or_block(sprite)
                        self.change_x = 0
                        self.s += self.timer_for_s
        else:
            self.kast = False
            self.update_position()
            self.s_kast = 0
            self.change_x = 0

        self.update_tik()
        self.update_slovar()


class Polet(Ogon, DvizhPers):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.POLET

        self.minus_mana = 7

        self.dvizh_force = (0, 60000)
        self.dvizh_vel = 500

        self.timer_for_s = 80

        self.texture = arcade.load_texture("resources/Sposob_animations/polet.png")

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.update_mor()
        self.center_x, self.top = self.pers.center_x, self.pers.bottom

        if self.action:
            if self.s == 0:
                self.func_mana()
                self.dvizh_pers_func(physics_engine)
            self.s += 1
            self.pers.pymunk.max_horizontal_velocity = self.dvizh_vel
            if self.s >= self.timer_for_s:
                self.s = 0
                self.action = False

        self.update_dvizh_pers()
        self.update_tik()
        self.update_slovar()


