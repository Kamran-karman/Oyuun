import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import arcade
import sposobs
from sposobs import stihiya, dvizh


class Veter(stihiya.StihiyaFight, dvizh.DvizhSprite):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = sposobs.VETER


class Poriv(Veter):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.uron = 100
        self.minus_mana = 10
        self.change = 15
        self.sposob = sposobs.PORIV

        self.timer_for_s = 90
        self.timer_for_s_kd = 240
        self.s_kd = self.timer_for_s_kd

        self.dvizh_force = (80000, 0)
        self.dvizh_vel = 300

        self.text = arcade.load_texture_pair('nuzhno/radius_porazheniya.png')
        self.scale = 0.2
        self.texture = self.text[0]

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor()
        self.kd_timer_mana()

        if self.s == 1:
            self.func_mana()

        if self.action:
            if self.s == 1:
                if self.pers.storona == 0:
                    self.change_x = self.change
                else:
                    self.change_x = -self.change

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar(sprite)
                    self.dvizh_sprite_func(sprite)
        else:
            self.update_position()
            self.change_x = 0

        self.update_slovar_dvizh()
        self.update_dvizh_sprite(self.timer_for_s - self.s)
        self.update_slovar()


class VeterOtalkivanie(arcade.Sprite):
    def __init__(self, igok, sprite_list):
        super().__init__()
        self.uron = 4

        self.igrok = igok
        self.sprite_list = sprite_list
        self.slovar = {}
        self.s3 = 0

        self.udar = False
        self.atak = False
        self.d = True
        self.s = 0
        self.s1 = 300

        self.force_x = 3000
        self.force_y = 5000

        #self.rad = hit_box_and_radius.Radius(0.5)
        self.tex = arcade.load_texture_pair('nuzhno/radius_porazheniya.png')
        self.scale = 0.5
        self.texture = self.tex[1]

        self.max = 5

    def on_update(self, delta_time: float = 1 / 60):
        if self.s3 == 0:
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
            self.s3 += 1

        self.s1 += 1

        if self.s1 < 300 and not self.d:
            self.udar = False
        else:
            self.d = True

        if self.s1 >= 300 and self.s == 1:
            self.s1 = 0

        if self.udar:
            start = self.igrok.position
            if self.change_x == 0:
                self.position = start

            if self.igrok.storona == 0 and not self.atak:
                self.atak = True
                self.change_x = 10
            elif self.igrok.storona == 1 and not self.atak:
                self.atak = True
                self.change_x = -10
        else:
            self.d = False
            self.atak = False
            self.change_x = 0
            self.s = 0

        if self.s >= 120:
            self.udar = False
            self.s = 0
        if self.udar:
            self.s += 1

        for sprite in self.sprite_list:
            if arcade.check_for_collision(sprite, self) and self.udar:
                for i in self.slovar:
                    if i == sprite and not self.slovar[i]:
                        self.slovar[i] = True
                        sprite.hp -= self.uron

        if not self.udar:
            for i in self.slovar:
                self.slovar[i] = False

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.tex[self.igrok.storona]

    def return_force(self, mass, xy: str):
        force_x = self.force_x
        force_y = self.force_y
        if xy == 'x':
            if mass < self.max:
                procent_max = self.max / 100
                procent_x = force_x / 100
                force_x -= procent_x * (mass / procent_max)
                if self.igrok.storona == 1:
                    return force_x
                else:
                    return -force_x
            else:
                return 0
        elif xy == 'y':
            if mass < self.max:
                procent_max = self.max / 100
                procent_y = force_y / 100
                force_y -= procent_y * (mass / procent_max)
                return force_y
            else:
                return 0
        elif xy == 'xy':
            if mass < self.max:
                procent_max = self.max / 100
                procent_x = force_x / 100
                procent_y = force_y / 100
                force_x -= procent_x * (mass / procent_max)
                force_y -= procent_y * (mass / procent_max)
                return (force_x, force_y)
            else:
                return 0
