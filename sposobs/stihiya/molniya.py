import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import arcade
import math
import sposobs
import hit_box_and_radius
from sposobs import stihiya

# (44, 117, 255, 255)


# ___SharMolniay___
SKOROST_SHAR_MOL = 20

S_KD_SHAR_MOL = 300
MAX_S_ZARYAD_SHAR_MOL = 360
MAX_BAF_S_ZARYAD_SHAR_MOL = 300
S_DO_PROMAH_SHAR_MOL = 45

VZRIV_BAF_URON_SHAR_MOL = 1.5
PROMAH_DEBAF_URON_SHAR_MOL = 1.5
BAF_URON_SHAR_MOL = 19.067

S_OGLUSH_SHAR_MOL = 6
DEBAF_FOR_OGLUSH_SHAR_MOL = 2
BAF_FOR_OGLUSH_SHAR_MOL = 294
VZRIV_BAF_OGLUSH_SHAR_MOL = 1.5
# ___________________________________


# ___UdarZevsa___
BAF_URON_UDAR_ZEVSA = 1.5

BAF_FOR_OGLUSH_UDAR_ZEVSA = 1.4788
# ___________________________________


class Molniya(stihiya.StihiyaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.tip = sposobs.MOLNIAY

        self.timer_for_s = 3


class CepnayaMolniay(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.CEPNAYA_MOLNIYA

        self.uron = 300

        self.minus_mana = 20

        self.en_x = 0
        self.en_y = 0

        self.radius = hit_box_and_radius.Radius(self)

        self.timer_for_s_kd = 360
        self.s_kd = self.timer_for_s_kd

        self.timer_for_s_oglush = 90

        self.tp = False
        self.spisok = []

    def update_animation(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_radius_position()
        self.update_sposob()
        self.update_mor()

        self.kd_timer_stamina()

        if self.action:
            spisok_rast = []
            spisok_xy = []
            spisok3 = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite=sprite) and sprite.hp > 0:
                    poz_x, poz_y = abs(sprite.center_x - self.pers.center_x), \
                        abs(sprite.center_y - self.pers.center_y)
                    pozi = (poz_x, poz_y)
                    spisok_rast.append(pozi)
                    x, y = sprite.center_x, sprite.center_y
                    xy = (x, y)
                    spisok_xy.append(xy)
            if len(spisok_rast) == 0:
                self.en_x, self.en_y = self.pers.position
                self.action = False
                self.s_kd = self.timer_for_s_kd + 1
            elif len(spisok_rast) > 0:
                if self.s == 1:
                    self.func_mana()
                    if self.mana:
                        self.tp = True
                    else:
                        self.s = 0
                        self.s_kd = self.timer_for_s_kd + 1
                else:
                    self.tp = False
                stx, sty = self.pers.position
                en = spisok_rast.index(min(spisok_rast))
                enx, eny = spisok_xy[en]
                spisok3.append(spisok_xy[en])
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny):
                        self.udar(sprite)
                        self.oglush(sprite)

                arcade.draw_line(stx, sty, enx, eny, (44, 117, 255, 255), 30)
                arcade.draw_circle_filled(stx, sty, 50, (44, 117, 255, 255))
                arcade.draw_circle_filled(enx, eny, 30, (44, 117, 255, 255))
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                arcade.draw_circle_filled(stx, sty, 45, arcade.color.WHITE)
                arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                radius = hit_box_and_radius.Radius()
                radius.position = enx, eny
                self.spisok.append([stx, sty, enx, eny])
                w = 1

                while w < 4:
                    if radius.check_collision(sprite_list=self.sprite_list):
                        if self.pers.position == (stx, sty):
                            pred_poz = 0, 0
                        else:
                            pred_poz = stx, sty
                        spisok_rast = []
                        spisok_xy = []
                        for sprite in self.sprite_list:
                            if radius.check_collision(sprite) and sprite.position != radius.position \
                                    and sprite.position != pred_poz and sprite.hp > 0:
                                poz_x, poz_y = abs(radius.center_x - sprite.center_x), abs(
                                    radius.center_y - sprite.center_y)
                                pozi = (poz_x, poz_y)
                                x, y = sprite.center_x, sprite.center_y
                                xy = (x, y)
                                e = 0
                                for i in spisok3:
                                    if xy[0] == i[0] and xy[1] == i[1]:
                                        e += 1
                                if e == 0:
                                    spisok_rast.append(pozi)
                                    spisok_xy.append(xy)
                        if len(spisok_rast) == 0:
                            if stx > enx:
                                self.en_x, self.en_y = enx - 250, eny + 150
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 250, eny + 150
                            break
                        elif w == 2 and len(spisok_rast) != 0:
                            en = spisok_rast.index(min(spisok_rast))
                            stx, sty = radius.position
                            enx, eny = spisok_xy[en]
                            for sprite in self.sprite_list:
                                if sprite.position == (enx, eny):
                                    self.udar(sprite)
                                    self.oglush(sprite)

                            arcade.draw_line(stx, sty, enx, eny, (44, 117, 255, 255), 30)
                            arcade.draw_circle_filled(enx, eny, 30, (44, 117, 255, 255))
                            arcade.draw_circle_filled(stx, sty, 30, (44, 117, 255, 255))
                            arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                            arcade.draw_circle_filled(stx, sty, 25, arcade.color.WHITE)
                            arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                            if stx > enx:
                                self.en_x, self.en_y = enx - 250, eny + 150
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 250, eny + 150
                            break
                        else:
                            if len(spisok_rast) != 0:
                                en = spisok_rast.index(min(spisok_rast))
                                stx, sty = radius.position
                                enx, eny = spisok_xy[en]
                                spisok3.append(spisok_xy[en])
                                for sprite in self.sprite_list:
                                    if sprite.position == (enx, eny):
                                        self.udar(sprite)
                                        self.oglush(sprite)

                                arcade.draw_line(stx, sty, enx, eny, (44, 117, 255, 255), 30)
                                arcade.draw_circle_filled(enx, eny, 30, (44, 117, 255, 255))
                                arcade.draw_circle_filled(stx, sty, 30, (44, 117, 255, 255))
                                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                                arcade.draw_circle_filled(stx, sty, 25, arcade.color.WHITE)
                                arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                                radius.position = enx, eny
                    w += 1

        self.update_slovar()

    def return_position(self):
        if self.tp:
            return self.en_x, self.en_y


class GnevTora(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.GNEV_TORA
        self.uron = 400

        self.radius = hit_box_and_radius.Radius(0.5)

        self.timer_for_s_kd = 600
        self.s_kd = self.timer_for_s_kd

        self.timer_for_s_oglush = 240

        self.minus_mana = 30

    def update_animation(self, delta_time: float = 1 / 60):
        if self.action and self.mana and not self.kd:
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 250, (44, 117, 255, 255))
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 150, arcade.color.WHITE)

    def on_update(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_radius_position()
        self.update_sposob()
        self.update_mor()

        self.kd_timer_stamina()

        for sprite in self.sprite_list:
            if self.radius.check_collision(sprite) and self.action and self.mana:
                self.udar(sprite)
                self.oglush(sprite)

        if self.s == 1:
            self.func_mana()

        self.update_slovar()


class StreliPeruna(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.STRELI_PERUNA
        self.uron = 150

        self.radius = hit_box_and_radius.Radius(2.5)

        self.timer_for_s_kd = 45
        self.s_kd = self.timer_for_s_kd

        self.timer_for_s_oglush = 45

        self.minus_mana = 4

    def update_animation(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_radius_position()
        self.update_sposob()
        self.update_mor()

        self.kd_timer_stamina()

        if self.action and self.radius.check_collision(sprite_list=self.sprite_list):
            spis_pos = []
            spis1 = []
            spis_rast = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite) and sprite.hp > 0:
                    spis_pos.append(sprite.position)
                    rx = abs(self.pers.center_x - sprite.center_x)
                    ry = abs(self.pers.center_y - sprite.center_y)
                    rast = math.hypot(rx, ry)
                    spis_rast.append((rx, ry))
                    spis1.append(rast)

            if len(spis_rast) <= 0:
                self.action = False
                self.s_kd = self.timer_for_s_kd

            for i in spis1:
                if len(spis1) > 5:
                    index = spis1.index(max(spis1))
                    spis_pos.pop(index)
                    spis1.remove(max(spis1))
                    spis_rast.pop(index)
                elif len(spis1) < 1:
                    return
                else:
                    break

            stx, sty = self.radius.position

            mnozh = len(spis1)

            while len(spis1) >= 1:
                enx, eny = min(spis_pos)
                arcade.draw_line(stx, sty, enx, eny, (44, 117, 255, 255), 25)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 15)
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny) and self.action and self.mana:
                        self.udar(sprite)
                        self.oglush(sprite)

                spis1.remove(spis1[spis_pos.index(min(spis_pos))])
                spis_pos.remove(min(spis_pos))

            if self.s == 1:
                self.timer_for_s_kd *= mnozh
                self.func_mana(self.minus_mana * mnozh)
        if not self.kd and not self.action:
            self.timer_for_s_kd = 30

        self.update_slovar()


class SharMolniay(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.SHAR_MOLNIYA

        self.uron = 35
        self.uron1 = self.uron // 5
        self.minus_mana = 1

        self.tex_shar = arcade.load_texture_pair('nuzhno/radius_porazheniya.png')
        self.texture = self.tex_shar[1]
        self.scale = 0.01

        self.radius = hit_box_and_radius.Radius()
        self.radius1 = hit_box_and_radius.Radius()

        self.zaryad = False
        self.zaryad_b = False
        self.vzriv = False
        self.promah = False
        self.baf_uron = 1

        self.s_zaryad = 0
        self.timer_for_s_kd = 300
        self.s_kd = self.timer_for_s_kd + 1
        self.s_do_promah = 0
        self.s_change_x = 0
        self.s = 0
        self.atak = False

        self.timer_for_s_oglush = 6
        self.oglush1 = 5

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_mor()
        uron = self.uron
        self.update_sposob()

        self.s_kd += 1
        self.update_radius_position()
        self.radius1.position = self.position
        if self.s_kd <= self.timer_for_s_kd:
            self.zaryad = False

        if self.change_x == 0:
            self.update_position()

        self.update_slovar()

        if self.zaryad:
            self.action = False
            self.zaryad_b = True
            self.s_zaryad += 1
            if self.s_zaryad < MAX_BAF_S_ZARYAD_SHAR_MOL:
                self.scale += 0.05 / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.baf_uron += BAF_URON_SHAR_MOL / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.minus_mana = 100 / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.timer_for_s_oglush += BAF_FOR_OGLUSH_SHAR_MOL / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.func_mana(self.minus_mana)
                if not self.mana:
                    self.zaryad = False
                    self.s_zaryad = 0
                    self.vzriv = True
                    self.atak = True
                    self.timer_for_s_oglush = 6

        if self.s_zaryad > MAX_S_ZARYAD_SHAR_MOL:
            self.vzriv = True
            self.atak = True
            self.pers.hp -= uron * VZRIV_BAF_URON_SHAR_MOL * round(self.baf_uron)
            self.timer_for_s_oglush *= VZRIV_BAF_OGLUSH_SHAR_MOL
            self.oglush(self.pers)
            self.radius1.scale = self.scale * 2
            for sprite in self.sprite_list:
                if self.radius1.check_collision(sprite) and sprite.hp > 0:
                    self.action = False
                    for i in self.slovar:
                        if sprite == i and not self.slovar[i]:
                            self.slovar[i] = True
                            sprite.hp -= uron * VZRIV_BAF_URON_SHAR_MOL * round(self.baf_uron)
                            self.oglush(sprite)
            self.s_zaryad = 0
            self.zaryad = False
            self.s_kd = 0

        if (self.action and self.zaryad_b) or self.atak:
            self.zaryad = False
            self.s_do_promah += 1
            self.s_zaryad = 0
            if self.s_change_x == 0:
                self.s_kd = 0
                self.s_change_x = 1
                if self.pers.storona == 0:
                    self.change_x = SKOROST_SHAR_MOL
                else:
                    self.change_x = -SKOROST_SHAR_MOL

            if arcade.check_for_collision_with_list(self, self.sprite_list):
                self.atak = True
                self.radius1.scale = self.scale * 1.5
                for sprite in self.sprite_list:
                    if self.radius1.check_collision(sprite) and sprite.hp > 0:
                        self.action = False
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= uron * round(self.baf_uron)
                                self.oglush(sprite)

            if self.s_do_promah >= S_DO_PROMAH_SHAR_MOL:
                self.promah = True
                self.action = False
                self.atak = True
                self.s_do_promah = 0
                self.timer_for_s_oglush /= DEBAF_FOR_OGLUSH_SHAR_MOL
                for sprite in self.sprite_list:
                    if self.radius1.check_collision(sprite) and sprite.hp > 0:
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= uron * round(self.baf_uron) / PROMAH_DEBAF_URON_SHAR_MOL
                                self.oglush(sprite)

        elif not self.action and not self.atak:
            self.change_x = 0
            if not self.promah and self.vzriv:
                for i in self.slovar:
                    self.slovar[i] = False
            if not self.zaryad:
                self.baf_uron = 1
                self.zaryad_b = False
                self.scale = 0.01
                self.s_change_x = 0
                self.minus_mana = 1

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        uron1 = self.uron1
        if self.atak or self.zaryad or self.action:
            arcade.draw_circle_filled(self.center_x, self.center_y, 90, (44, 117, 255, 50), 5)
        if self.atak:
            self.timer_for_s_oglush /= self.oglush1
            self.s += 1
            if self.s > self.timer_for_s:
                self.atak = False
                self.promah = False
                self.vzriv = False
                self.s = 0
            spisok_rast = []
            spisok_xy = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite) and sprite.position != self.radius.position and sprite.hp > 0:
                    rast = (abs(self.radius.center_x - sprite.center_x),
                            abs(self.radius.center_y - sprite.center_y))
                    xy = sprite.position
                    spisok_rast.append(rast)
                    spisok_xy.append(xy)

            if len(spisok_rast) > 0:
                if self.vzriv:
                    self.timer_for_s_oglush *= VZRIV_BAF_OGLUSH_SHAR_MOL
                elif self.promah:
                    self.timer_for_s_oglush /= PROMAH_DEBAF_URON_SHAR_MOL

            if len(spisok_rast) > 5:
                while len(spisok_rast) > 5:
                    max_index = spisok_rast.index(max(spisok_rast))
                    spisok_rast.remove(spisok_rast[max_index])
                    spisok_xy.remove(spisok_xy[max_index])

            stx, sty = self.position
            while len(spisok_rast) >= 1:
                min_index = spisok_rast.index(min(spisok_rast))
                enx, eny = spisok_xy[min_index]
                arcade.draw_line(stx, sty, enx, eny, (44, 117, 255, 255), 25)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 15)
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny):
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                if self.vzriv:
                                    sprite.hp -= uron1 * VZRIV_BAF_URON_SHAR_MOL * round(self.baf_uron)
                                    self.oglush(sprite)
                                elif self.promah:
                                    sprite.hp -= uron1 * round(self.baf_uron) / PROMAH_DEBAF_URON_SHAR_MOL
                                    self.oglush(sprite)
                                else:
                                    sprite.hp -= uron1 * round(self.baf_uron)
                                    self.oglush(sprite)
                spisok_rast.remove(spisok_rast[min_index])
                spisok_xy.remove(spisok_xy[min_index])

        if self.s == 1:
            if self.vzriv:
                self.func_mana(round(self.minus_mana * 1.2))
            else:
                self.func_mana(self.minus_mana)


class UdarZevsa(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = sposobs.UDAR_ZEVSA
        self.uron = 20

        self.timer_for_s_kd = 600
        self.s_kd = self.timer_for_s_kd + 5

        self.timer_for_s = 300
        self.timer_for_s_oglush = 12

        self.radius = hit_box_and_radius.Radius(1.5)

        self.rast = 0
        self.slovar_rast = {}
        self.s1 = 0
        self.line_width = 15
        self.minus_mana = 2

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_position()
        self.update_radius_position()
        self.update_sposob()
        self.update_mor()

        self.kd_timer_mana()

        if self.action:
            self.s1 = 1
            if len(self.slovar_rast) == 0:
                for sprite in self.sprite_list:
                    if self.radius.check_collision(sprite) and sprite.hp > 0:
                        rast_x = abs(sprite.center_x - self.pers.center_x)
                        rast_y = abs(sprite.center_y - self.pers.center_y)
                        rast = math.hypot(rast_x, rast_y)
                        self.slovar_rast.update({sprite: rast})

            if len(self.slovar_rast) == 0:
                self.action = False
                self.s_kd = self.timer_for_s_kd + 1
            else:
                if self.s % 30 == 0:
                    self.timer_for_s_kd += 30
                    self.uron *= BAF_URON_UDAR_ZEVSA
                    self.minus_mana *= 1.35
                    self.timer_for_s_oglush *= BAF_FOR_OGLUSH_UDAR_ZEVSA
                    self.func_mana(round(self.minus_mana))
                    self.line_width *= 1.1
                    for i in self.slovar:
                        self.slovar[i] = False

                self.rast = min(self.slovar_rast.values())
                for sprite in self.slovar_rast:
                    if self.slovar_rast[sprite] == self.rast:
                        if sprite.hp <= 0:
                            self.action = False
                            break
                        else:
                            self.udar(sprite)
                            self.oglush(sprite)
        else:
            if self.s1 == 1:
                self.s_kd = 0
                self.s1 -= 1
            if self.s_kd > self.timer_for_s_kd:
                self.timer_for_s_kd = 600
            self.rast = 0
            self.slovar_rast.clear()
            self.uron = 20
            self.line_width = 15
            self.minus_mana = 2
            self.timer_for_s_oglush = 12

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.action:
            for sprite in self.slovar_rast:
                if self.slovar_rast[sprite] == self.rast:
                    arcade.draw_line(self.pers.center_x, self.pers.center_y, sprite.center_x, sprite.center_y,
                                     (44, 117, 255, 255), self.line_width)
                    break
