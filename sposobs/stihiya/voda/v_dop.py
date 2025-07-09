import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import hit_box_and_radius
import instruments
import arcade
import sposobs
import arcade.texture.transforms
from sposobs.stihiya import voda
from sposobs.stihiya.voda import voda_h
import math


class VodaFightUdar(voda.VodaFight):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.sposob = sposobs.VODA_UDAR
        self.uron = voda_h.VFU_URON
        self.change = voda_h.VFU_CHANGE
        self.probit_block = False

        self.timer_for_s = voda_h.VFU_TIMER_FOR_S
        self.timer_for_s_kd = voda_h.VFU_TIMER_FOR_S_KD
        self.timer_for_s_oglush = voda_h.VFU_TIMER_FOR_S_OGLUSH
        self.timer_for_s_dvizh = voda_h.VFU_TIMER_FOR_S_DVIZH_SPRITE
        self.s_kd = self.timer_for_s_kd
        self.minus_mana = voda_h.VFU_MINUS_MANA
        self.dvizh_force = voda_h.VFU_DVIZH_FORCE_SPRITE
        self.dvizh_vel = voda_h.VFU_DVIZH_VEL_SPRITE

        self.rast = 0
        self.slovar_rast = {}
        self.calc = False
        self.v_nikuda = False

        self.minus_change_x = voda_h.VFU_MINUS_CHANGE_X
        self.minus_change_y = voda_h.VFU_MINUS_CHANGE_Y

        self.radius = hit_box_and_radius.Radius(1.5)
        self.tex_voda_fight_udar = arcade.load_texture_pair('resources/Sposob_animations/sputnik.png')
        self.texture = self.tex_voda_fight_udar[0]
        self.position = self.pers.center_x, self.pers.center_y - 64

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.update_mor()
        self.update_v()
        self.kd_timer_mana()
        self.radius.position = self.pers.position
        if not self.radius.check_collision(sprite_list=self.sprite_list):
            self.v_nikuda = True
        else:
            s = 0
            for sprite in self.sprite_list:
                if sprite.hp <= 0:
                    s += 1

            if len(self.sprite_list) == s:
                self.v_nikuda = True

        if self.action:
            if not self.calc:
                if self.v_nikuda:
                    self.update_storona(None, 1)
                    self.change_x = self.change * self.storona
                    self.change_y = 1
                    if self.change_y < 0:
                        self.change_y *= -1
                else:
                    for sprite in self.sprite_list:
                        if self.radius.check_collision(sprite) and sprite.hp > 0:
                            rast_x = abs(self.center_x - sprite.center_x)
                            rast_y = abs(self.center_y - sprite.center_y)
                            rast = math.hypot(rast_x, rast_y)
                            self.slovar_rast.update({sprite: rast})

                    if len(self.slovar_rast) > 0:
                        self.rast = min(self.slovar_rast.values())
                    else:
                        self.v_nikuda = True
                        self.update_storona(self.pers)
                        self.change_x = self.change * self.storona
                        self.change_y = 1000 / self.change_x
                        if self.change_y < 0:
                            self.change_y *= -1

                    if not self.v_nikuda:
                        for sprite in self.slovar_rast:
                            if self.slovar_rast[sprite] == self.rast and sprite.hp > 0:
                                rast_x = abs(sprite.center_x - self.center_x)
                                rast_y = abs(sprite.center_y - self.center_y)
                                self.update_storona(sprite)
                                self.change_x = self.change * self.storona
                                if self.center_y <= sprite.center_y:
                                    self.change_y = rast_y / (rast_x / self.change_x) * self.storona
                                else:
                                    self.change_y = rast_y / (rast_x / self.change_x)
                                    if self.change_y > 0:
                                        self.change_y *= -1
            self.calc = True

            self.change_y -= self.minus_change_y / 60

            if self.change_x >= 0:
                self.change_x -= self.minus_change_x / 60
            else:
                self.change_x += self.minus_change_x / 60

            if arcade.check_for_collision_with_list(self, self.pers.fizika.walls_list):
                self.s += self.timer_for_s

            for sprite in self.sprite_list:
                if arcade.check_for_collision(sprite, self) and sprite.hp > 0:
                    self.s += self.timer_for_s
                    if self.udar_or_block(sprite):
                        self.oglush(sprite)
                        self.dvizh_sprite_func(sprite, physics_engine)
        else:
            self.calc = self.v_nikuda = False
            self.change_x = self.change_y = 0
            self.slovar_rast.clear()
            self.update_position()

        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)
        self.update_slovar()


class VodaFightUdars(voda.VodaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list, voda_h.VFUs_MINUS_V)
        self.sposob = sposobs.VODA_UDARS

        self.timer_for_s_kd = voda_h.VFUs_TIMER_FOR_S_KD

        self.vu_list = arcade.SpriteList()
        for i in range(voda_h.VFUs_KOL_VO):
            voda_udar = VodaFightUdar(self.pers, self.sprite_list, self.minus_v)
            self.vu_list.append(voda_udar)

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        if self.timer_for_s_kd >= self.s_kd > 0:
            self.s_kd += 1
            self.action = False
        else:
            self.s_kd = 0
            self.s += 1

        self.update_sposob()
        self.update_v()

        if not self.kritik:
            self.v_max_minus = True
        if self.kritik:
            self.kol_vo = 0
        else:
            self.kol_vo = 6
        # self.stihiya_kd_timer()

        for vu in self.vu_list:
            vu: VodaFightUdar
            vu.on_update(physics_engine=physics_engine)
            vu.update()
            vu.dvizh_vel = self.dvizh_vel
            vu.sprite_list = self.sprite_list

        if self.action:
            for vu in self.vu_list:
                if not vu.action and not vu.kd:
                    vu.action = True
                    self.action = False
                    self.s_kd += 1
                    self.s = 0
                    break

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        for vu in self.vu_list:
            if vu.action:
                vu.draw()


class Karakatica(voda.VodaImitation):
    def __init__(self, pers, sprite_list, idle_udar_texture_list, idle_kombo_texture_list, obich_texture,
                 block_texture):
        super().__init__(pers, sprite_list, 200)
        self.sposob = sposobs.KARAKATICA

        self.uron = voda_h.KARA_URON
        self.minus_mana = voda_h.KARA_MINUS_MANA
        self.kol_vo_udars = voda_h.KARA_KOL_VO_UDARS
        self.baff_uron = voda_h.KARA_BAFF_URON
        self.kombo_baff_uron = voda_h.KARA_KOMBO_BAFF_URON

        self.probit_block = False

        self.timer_for_s = voda_h.KARA_TIMER_FOR_S
        self.timer_for_s_kd = voda_h.KARA_TIMER_FOR_S_KD
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_oglush = voda_h.KARA_TIMER_FOR_S_OGLUSH
        self.timer_for_s_dvizh_sprite = voda_h.KARA_TIMER_FOR_S_DVIZH_SPRITE

        self.dvizh_vel = voda_h.KARA_DVIZH_VEL_SPRITE
        self.dvizh_force = voda_h.KARA_DVIZH_FORCE_SPRITE

        self.idle_texture = self.pers.idle_texture
        self.obich_texture = obich_texture
        self.kol_vo_udar_textures = 4
        self.kol_vo_kombo_textures = 8
        self.kombo_texture_list.load_textures(self.kol_vo_kombo_textures,
                                              'resources/Sposob_animations/Karakatica/kombo', instruments.PNG)
        self.idle_kombo_texture_list = idle_kombo_texture_list
        self.udar_texture_list = instruments.TextureList()
        self.udar_texture_list.load_textures(self.kol_vo_udar_textures,
                                             'resources/Sposob_animations/Karakatica/udar', instruments.PNG)
        self.idle_udar_texture_list = idle_udar_texture_list
        self.block_texture = block_texture
        self.main_block = True

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.update_v()
        self.update_mor()
        self.kd_timer_stamina()
        self.update_kombo()
        self.update_block()
        self.block_block()
        self.bottom = self.pers.bottom
        self.center_x = self.pers.center_x
        self.fight = self.pers.fight
        if self.s == 1:
            self.s_udar_texture += 1

        if int(self.s_kombo_texture) == 2:
            if self.pers.storona == 0:
                self.fizika.apply_force(self.pers, (10000, 500))
            else:
                self.fizika.apply_force(self.pers, (-10000, 500))

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and sprite.hp > 0:
                    self.atak(sprite, physics_engine)

        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)
        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        #self.draw_hit_box()
        if self.fight:
            if self.action:
                if not self.kombo:
                    if self.s_udar_texture >= self.kol_vo_udar_textures:
                        self.s_udar_texture = 0
                    self.texture = self.udar_texture_list[self.s_udar_texture][self.pers.storona]
                    self.hit_box._adjusted_cache_dirty = True
                    self.hit_box._points = self.texture.hit_box_points
                    self.pers.texture = self.idle_udar_texture_list[self.s_udar_texture][self.pers.storona]
                else:
                    self.s_kombo_texture += 0.01
                    if self.s_kombo_texture >= self.kol_vo_kombo_textures:
                        self.s_kombo_texture = 0
                        self.kombo = False
                        self.s += self.timer_for_s
                    self.pers.texture = self.idle_kombo_texture_list[int(self.s_kombo_texture)][self.pers.storona]
                    self.texture = self.kombo_texture_list[int(self.s_kombo_texture)][self.pers.storona]
                    self.hit_box._adjusted_cache_dirty = True
                    self.hit_box._points = self.texture.hit_box_points
                self.draw()
            elif self.block or self.avto_block:
                self.pers.texture = self.block_texture[self.pers.storona]
                self.texture = self.block_texture[self.pers.storona]
            else:
                self.pers.texture = self.obich_texture[self.pers.storona]
        else:
            #self.pers.texture = self.idle_texture[self.pers.storona]
            if self.pers.oglush_for_sposob:
                self.pers.texture = self.pers.idle_texture[self.pers.storona]


class Techenie(voda.VodoHod):
    def __init__(self, pers, sprite_list, vel: int, igrok=False):
        super().__init__(pers, sprite_list, igrok)
        self.minus_mana = voda_h.TECH_MINUS_MANA
        self.sposob = sposobs.TECHENIE
        self.uron = voda_h.TECH_URON

        self.dvizh_vel = vel
        self.dvizh_force = voda_h.TECH_DVIZH_FORCE_SPRITE
        self.timer_for_s_dvizh = voda_h.TECH_TIMER_FOR_S_DVIZH_SPRITE
        self.s_kd = 2

        self.timer_for_s_oglush = voda_h.TECH_TIMER_FOR_S_OGLUSH

        self.minus_max_v = 0

        self.techenie_texture = arcade.load_texture_pair('resources/Sposob_animations/techenie.png')
        self.texture = self.techenie_texture[0]
        self.otnos = voda_h.TECH_OTNOS
        self.scale = voda_h.TECH_SCALE
        self.hit_box._points = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.techenie_texture[self.pers.storona]


class Reka(voda.VodoHod):
    def __init__(self, pers, sprite_list, vel: int, igrok=False):
        super().__init__(pers, sprite_list, igrok, voda_h.REKA_MINUS_V)
        self.sposob = sposobs.REKA

        self.minus_mana = voda_h.REKA_MINUS_MANA
        self.uron = voda_h.REKA_URON
        self.minus_max_v = 0

        self.dvizh_vel = vel
        self.dvizh_force = voda_h.REKA_DVIZH_FORCE_SPRITE
        self.timer_for_s_dvizh = voda_h.REKA_TIMER_FOR_S_DVIZH_SPRITE

        self.s_kd = 2
        self.timer_for_s_oglush = voda_h.REKA_TIMER_FOR_S_OGLUSH

        self.reka_texture = arcade.load_texture_pair('resources/Sposob_animations/reka.png')
        self.priziv_list = []
        self.texture = self.reka_texture[0]
        self.otnos = voda_h.REKA_OTNOS
        self.hit_box._points = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.reka_texture[self.storona]
        self.hit_box._points = self.texture.hit_box_points

class VodaShchit(voda.VodaBlock):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list, voda_h.VSH_MINUS_V)
        self.position = 100, 200

        self.minus_mana = voda_h.VSH_MINUS_MANA

        self.block_texture = arcade.load_texture_pair('resources/Sposob_animations/BlockVoda/block_voda2.png')
        self.texture = self.block_texture[1]
        self.s_block_texture = 0
        self.block_texture_list = instruments.TextureList()
        self.block_texture_list.load_textures(3, 'resources/Sposob_animations/BlockVoda/block_voda',
                                              instruments.PNG)
        self.scale = 1.5

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.update_v()
        self.update_block()
        self.block_block()

        # for sprite in self.sprite_list:
        #     if abs(sprite.center_x - self.pers.center_x) <= 125 and sprite.storona != self.pers.storona:
        #         self.block = self.pers.block.block = False
        if self.fizika:
            if self.block:
                self.scale = 1.5
                if self not in self.fizika.sprites:
                    self.fizika.add_sprite(self, body_type=physics_engine.KINEMATIC, friction=0, elasticity=1)

                if self.pers.storona == 1:
                    self.fizika.set_position(self, (self.pers.center_x - 100, self.pers.center_y))
                else:
                    self.fizika.set_position(self, (self.pers.center_x + 100, self.pers.center_y))
            elif not self.block:
                if self in self.fizika.sprites:
                    self.fizika.remove_sprite(self)
            elif self.avto_block:
                self.position = self.pers.position
                self.scale = 1
        # else:
        #     if self in self.fizika.sprites:
        #         self.fizika.remove_sprite(self)
        #         self.fizika.sprites.pop(self)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.block_animation()

