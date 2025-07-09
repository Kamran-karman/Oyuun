import math

import instruments

import arcade
import sposobs
from sposobs import dvizh
import arcade.texture.transforms
from sposobs.stihiya import voda
from sposobs.stihiya.voda import voda_h, v_dop
from animations import sposob_animations
from animations.sposob_animations import ACTION, DEACTION
from interaction_sprites.battles import mobs


class Volna(voda.VodaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list, voda_h.VOLNA_MINUS_V)
        self.uron = voda_h.VOLNA_URON
        self.minus_mana = voda_h.VOLNA_MINUS_MANA
        self.sposob = sposobs.VOLNA

        self.osn = True

        self.action_2 = True
        self.timer_for_s_2 = voda_h.VOLNA_TIMER_FOR_S_2
        self.timer_for_s = voda_h.VOLNA_TIMER_FOR_S
        self.timer_for_s_kd = voda_h.VOLNA_TIMER_FOR_S_KD
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = voda_h.VOLNA_TIMER_FOR_S_OGLUSH

        self.dvizh_force = voda_h.VOLNA_DVIZH_FORCE_SPRITE
        self.dvizh_vel = voda_h.VOLNA_DVIZH_VEL_SPRITE
        self.timer_for_s_dvizh = voda_h.VOLNA_TIMER_FOR_S_DVIZH

        self.volna_tex = arcade.load_texture_pair('resources/Sposob_animations/volna.png')
        self.scale = 3
        self.texture = self.volna_tex[0]
        self.radius.radius = 15 * 180
        self.s1 = 0

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_mor()
        self.update_sposob()
        self.update_v()
        if self.s == 1:
            self.func_mana()
        self.kd_timer_mana()

        if not self.action:
            self.update_position()
        else:
            if self.s_2 <= self.timer_for_s_2:
                self.pers.stan_for_sposob = True
                self.s_2 += 1
                self.action_2 = False
                self.update_position()
            else:
                self.pers.stan_for_sposob = False
                self.action_2 = True
            if self.s == self.timer_for_s_2 + 1:
                if self.pers.storona == 0:
                    self.change_x = voda_h.VOLNA_CHANGE_X
                else:
                    self.change_x = -voda_h.VOLNA_CHANGE_X

            if self.action_2:
                for sprite in self.sprite_list:
                    if arcade.check_for_collision(sprite, self) and sprite.hp > 0:
                        for i in self.slovar:
                            if i == sprite and not self.slovar[i]:
                                self.dvizh_sprite_func(sprite, physics_engine)
                        self.udar(sprite)
                        self.oglush(sprite)
                        self.sbiv(sprite)
                        if self.s < self.timer_for_s - 5:
                            self.s = self.timer_for_s - 5
                        # self.s += self.timer_for_s

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)


class BigVolna(Volna):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.uron = voda_h.BIG_VOLNA_URON
        self.minus_mana = voda_h.BIG_VOLNA_MINUS_MANA
        self.minus_v = voda_h.BIG_VOLNA_MINUS_V
        self.sposob = sposobs.BIG_VOLNA

        self.timer_for_s_2 = voda_h.BIG_VOLNA_TIMER_FOR_S_2
        self.timer_for_s = voda_h.BIG_VOLNA_TIMER_FOR_S
        self.timer_for_s_kd = voda_h.BIG_VOLNA_TIMER_FOR_S_KD
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = self.timer_for_s

        self.dvizh_force = voda_h.BIG_VOLNA_DVIZH_FORCE_SPRITE
        self.dvizh_vel = voda_h.BIG_VOLNA_DVIZH_VEL_SPRITE
        self.timer_for_s_dvizh = voda_h.BIG_VOLNA_TIMER_FOR_S

        self.scale = 6
        self.radius.radius = 1350

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        if self.pers.block.block:
            self.action = False
        super().on_update(delta_time, physics_engine)
        s = self.s - self.timer_for_s
        if self.s >= s + self.timer_for_s > self.timer_for_s:
            self.s -= self.timer_for_s


class RechnoyDrakon(voda.VodaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list, voda_h.RD_MINUS_V)
        self.sposob = sposobs.RECHNOY_DRAKON

        self.osn = True

        self.uron = voda_h.RD_URON
        self.min_uron = voda_h.RD_MIN_URON
        self.minus_mana = voda_h.RD_MINUS_MANA

        self.timer_for_s_zaderzh = voda_h.RD_TIMER_FOR_S_ZADERZH
        self.s_zaderzh = 0
        self.timer_for_s = voda_h.RD_TIMER_FOR_S
        self.timer_for_s_kd = voda_h.RD_TIMER_FOR_S_KD
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = self.timer_for_s
        self.dvizh_force = voda_h.RD_DVIZH_FORCE_SPRITE
        self.dvizh_vel = voda_h.RD_DVIZH_VEL_SPRITE

        self.force_for_block = voda_h.RD_FORCE_FOR_BLOCK
        self.minus_for_block = voda_h.RD_MINUS_FOR_BLOCK
        self.probit_block = False

        self.rechnoy_drakon_tex = arcade.load_texture_pair('resources/Sposob_animations/rechnoy_drakon.png')
        self.scale = voda_h.RD_SCALE
        self.texture = self.rechnoy_drakon_tex[1]

        self.normal_scale_xy = self.scale_xy
        self.max_widht = voda_h.RD_MAX_WIDHT
        self.vr_widht = voda_h.RD_VR_WIDHT
        self.plus = True
        self.blizh_sprite = None

        self.radius.radius = self.max_widht

        self.s1 = 0

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        super().on_update()
        self.update_sposob()
        self.update_slovar()
        self.update_v()
        if self.s == 1:
            self.func_mana()
        self.update_mor()
        if self.s >= self.timer_for_s:
            self.pers.stan_for_sposob = False
        self.kd_timer_mana()

        if self.action:
            self.pers.stan_for_sposob = True
            if self.s_zaderzh <= self.timer_for_s_zaderzh:
                self.s_zaderzh += 1
            else:
                rast_list = []
                for sprite in self.sprite_list:
                    if sprite.hp > 0:
                        rast_list.append(abs(sprite.center_x - self.pers.center_x))

                if len(rast_list) > 0:
                    min_rast = min(rast_list)
                    for sprite in self.sprite_list:
                        if abs(sprite.center_x - self.pers.center_x) == min_rast:
                            self.vr_widht = min_rast
                            self.blizh_sprite = sprite

                    if arcade.check_for_collision(self.blizh_sprite, self):
                        self.plus = False
                    else:
                        self.plus = True

                if self.vr_widht < self.width and not self.plus:
                    self.width = self.vr_widht
                if self.width <= self.max_widht and self.plus:
                    self.scale_xy = (self.scale_xy[0] + 1.45, self.scale_xy[1])
                if self.pers.storona == 0:
                    self.left = self.pers.center_x
                else:
                    self.right = self.pers.center_x
                self.center_y = self.pers.top - self.pers.width * 0.3

                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self, sprite):
                        if self.s1 == 0:
                            if self.udar_or_block(sprite, popal=False):
                                self.timer_for_s_oglush = (self.timer_for_s - self.s) + 90
                                self.oglush(sprite)
                                self.dvizh_sprite_func(sprite, physics_engine)
                            self.s1 += 1
                        elif self.s1 != 0 and self.s % 20 == 0:
                            if self.udar_or_block(sprite, self.min_uron, False):
                                self.timer_for_s_oglush = (self.timer_for_s - self.s) + 90
                                self.oglush(sprite)
                                self.dvizh_sprite_func(sprite, physics_engine)
        else:
            self.s1 = 0
            self.s_zaderzh = 0
            self.scale_xy = self.normal_scale_xy
            self.update_position((self.pers.center_x, self.pers.top - self.pers.width * 0.3))
            # if self.pers.fight:
            #     self.position = self.pers.position
            # else:
            #     self.update_position()

        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine, self.timer_for_s - self.s)


class UdarKita(voda.VodaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list, voda_h.UK_MINUS_V)
        self.sposob = sposobs.UDAR_KITA

        self.osn = True

        self.uron = voda_h.UK_URON
        self.minus_mana = voda_h.UK_MINUS_MANA

        self.timer_for_zaderzh = voda_h.UK_TIMER_FOR_S_ZADERZH
        self.timer_for_s = voda_h.UK_TIMER_FOR_S
        self.timer_for_s_kd = voda_h.UK_TIMER_FOR_S_KD
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = voda_h.UK_TIMER_FOR_S_OGLUSH
        self.timer_for_s_dvizh = voda_h.UK_TIMER_FOR_S_DVIZH_SPRITE
        self.dvizh_force = voda_h.UK_DVIZH_FORCE_SPRITE
        self.dvizh_vel = voda_h.UK_DVIZH_VEL_SPRITE

        self.tex_udar_kita = arcade.load_texture_pair('resources/Sposob_animations/UdarKita.png')
        self.scale = voda_h.UK_SCALE
        self.texture = self.tex_udar_kita[0]
        self.radius.radius = self.height

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        super().on_update()
        self.update_sposob()
        self.update_v()
        if self.s == 1:
            self.func_mana()
        self.update_mor()
        self.update_position()
        self.kd_timer_mana()

        if self.action:
            self.pers.bessmert = True
            self.bottom = self.pers.bottom
            if self.s <= self.timer_for_zaderzh:
                self.pers.stan_for_sposob = True
            else:
                self.pers.stan_for_sposob = False
                if self.s == self.timer_for_zaderzh + 1:
                    if self.pers.storona == 0:
                        self.change_angle = 5
                    else:
                        self.change_angle = -5
                if self.change_angle > 0:
                    self.left = self.pers.center_x - 32
                else:
                    self.right = self.pers.center_x + 32

                for sprite in self.sprite_list:
                    if arcade.check_for_collision(sprite, self) and sprite.hp > 0:
                        self.udar(sprite)
                        self.oglush(sprite)
                        self.dvizh_sprite_func(sprite, physics_engine)
                        self.sbiv(sprite)
        else:
            self.pers.stan_for_sposob = False
            self.pers.bessmert = False
            self.angle = 0
            self.change_angle = 0

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)


class Tayfun(voda.VodaFight, dvizh.DvizhPersAndSprite):
    def __init__(self, pers, sprite_list, igrok):
        super().__init__(pers, sprite_list, voda_h.TAYF_MINUS_V)
        self.sposob = sposobs.TAYFUN

        self.osn = True

        self.uron = voda_h.TAYF_URON
        self.minus_mana = voda_h.TAYF_MINUS_MANA

        self.igrok = igrok

        self.timer_for_s = voda_h.TAYF_TIMER_FOR_S
        self.timer_for_s_kd = voda_h.TAYF_TIMER_FOR_S_KD
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = voda_h.TAYF_TIMER_FOR_S_OGLUSH

        self.timer_for_s_dvizh_sprite = voda_h.TAYF_TIMER_FOR_S_DVIZH_SPRITE
        self.dvizh_force_sprite = voda_h.TAYF_DVIZH_FORCE_SPRITE
        self.dvizh_vel_sprite = voda_h.TAYF_DVIZH_VEL_SPRITE

        self.dvizh_force = voda_h.TAYF_DVIZH_FORCE_PERS

        self.texture_tayfun = arcade.load_texture_pair('resources/Sposob_animations/tayfun.png')
        self.texture = self.texture_tayfun[0]

        self.normal_scale_xy = self.scale_xy

        self.radius.radius = self.width * 10

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        super().on_update()
        self.update_sposob()
        self.update_v()
        if self.s == 1:
            self.func_mana()
            self.dvizh_pers_func(physics_engine)
        self.update_mor()
        self.center_x, self.top = self.update_position((self.pers.center_x, self.pers.bottom), True)
        self.top += 24
        self.kd_timer_mana()

        if self.action:
            self.scale_xy = (self.scale_xy[0] + 0.2, self.scale_xy[1] + 0.3)
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar(sprite)
                    self.dvizh_sprite_func(sprite, physics_engine)
                    self.oglush(sprite)
                    self.sbiv(sprite)
        else:
            self.scale_xy = self.normal_scale_xy

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)
        self.update_dvizh_pers()


class Hlist(voda.VodaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list, voda_h.HLIST_MINUS_V)
        self.sposob = sposobs.HLIST

        self.osn = True

        self.uron = voda_h.HLIST_URON
        self.minus_mana = voda_h.HLIST_MINUS_MANA

        self.probit_block = False

        self.timer_for_s = voda_h.HLIST_TIMER_FOR_S
        self.timer_for_s_kd = voda_h.HLIST_TIMER_FOR_S_KD
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_zaderzh = voda_h.HLIST_TIMER_FOR_S_ZADERZH
        self.s_zaderzh = 0
        self.timer_for_s_oglush = voda_h.HLIST_TIMER_FOR_S_OGLUSH
        self.timer_for_s_dvizh = voda_h.HLIST_TIMER_FOR_S_DVIZH_SPTITE
        self.dvizh_force = voda_h.HLIST_DVIZH_FORCE_SPRITE
        self.dvizh_vel = voda_h.HLIST_DVIZH_VEL_SPRITE

        self.texture_hlist = arcade.load_texture_pair('resources/Sposob_animations/hlist1.png')
        self.scale = voda_h.HLIST_SCALE
        self.texture = self.texture_hlist[0]

        self.normal_scale_xy = self.scale_xy
        self.radius.radius = self.width * 36
        self.max_widht = 576

        self.last_storona = self.pers.storona

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.update_v()
        if self.s == 1:
            self.func_mana()
        self.update_mor()
        self.kd_timer_mana()
        self.radius.position = self.pers.position

        self.bottom = self.pers.center_y
        self.left = self.pers.center_x
        if self.pers.storona == 0:
            self.left = self.pers.center_x
        else:
            self.right = self.pers.center_x

        if self.action:
            if self.s_zaderzh < self.timer_for_s_zaderzh:
                self.last_storona = self.pers.storona
                self.s_zaderzh += 1
                self.scale_xy = (self.scale_xy[0], self.scale_xy[1] + 1.75)
            else:
                if self.pers.storona == 0:
                    self.change_angle = 4.5
                else:
                    self.change_angle = -4.5

                if self.last_storona != self.pers.storona:
                    self.last_storona = self.pers.storona
                    self.angle *= -1

                self.scale_xy = (self.scale_xy[0], self.scale_xy[1] + 1.25)

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and sprite.hp > 0:
                    self.s += self.timer_for_s
                    if self.udar_or_block(sprite):
                        self.oglush(sprite)
                        self.dvizh_sprite_func(sprite, physics_engine)
        else:
            self.angle = self.change_angle = self.s_zaderzh = 0
            self.scale_xy = self.normal_scale_xy

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)


class Lezviya(voda.VodaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list, 0)
        self.sposob = sposobs.LEZVIYA

        self.osn = True

        self.uron = voda_h.LEZVIYA_URON
        self.minus_mana = voda_h.LEZVIYA_MINUS_MANA

        self.timer_for_s = voda_h.LEZVIYA_TIMER_FOR_S
        self.timer_for_s_kd = voda_h.LEZVIYA_TIMER_FOR_S_KD
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = voda_h.LEZVIYA_TIMER_FOR_S_OGLUSH

        self.timer_for_s_dvizh = voda_h.LEZVIYA_TIMER_FOR_S_DVIZH
        self.dvizh_force = voda_h.LEZVIYA_DVIZH_FORCE
        self.dvizh_vel = voda_h.LEZVIYA_DVIZH_VEL

        self.animations = sposob_animations.SposobAnimation(self)
        self.animations.slovar_animation[ACTION][1] = 7
        self.animations.slovar_animation[ACTION][2] = 0.5
        self.animations.slovar_animation[ACTION][3].load_textures(8, f"{self.animations.main_patch}lezviya", instruments.PNG)

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        super().on_update()
        self.update_sposob()
        self.update_v()
        if self.s == 1:
            self.func_mana()
        self.update_mor()
        self.kd_timer_mana()
        self.update_position()

        if self.action:
            self.change_x = 0.1 * self.storona
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and sprite.hp > 0 and self.udar_or_block(sprite):
                    self.oglush(sprite)
                    self.dvizh_sprite_func(sprite, physics_engine)
        else:
            self.change_x = 0

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.animations.action_animation()
        self.draw_hit_box(arcade.color.RED)


class Briz(voda.VodaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list, 300)
        self.sposob = sposobs.BRIZ

        self.osn = True

        self.uron = 200
        self.minus_mana = 5

        self.timer_for_s = 90
        self.timer_for_s_kd = self.s_kd = 180
        self.timer_for_s_oglush = 120

        self.timer_for_s_dvizh = 30
        self.dvizh_force = (-80000, 0)
        self.dvizh_vel = 1000

        self.radius.scale = 1.5

        self.slovar_rast = {}
        self.change = 15
        self.rast = 0
        self.v_nikuda = False
        self.calc = True

        self.sprite = None
        self.kombo = False
        self.s_kombo = 0
        self.s_k = 0
        self.action_storona = 0

        self.dlan_texture = arcade.load_texture_pair('resources/Sposob_animations/briz0.png')
        self.hvat_texture = arcade.load_texture_pair('resources/Sposob_animations/briz1.png')
        self.udar_texture = arcade.load_texture_pair('resources/Sposob_animations/briz2.png')

        self.scale = 3

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.update_v()
        if self.s == 1:
            self.func_mana()
            self.action_storona = self.pers.storona
        self.update_mor()
        self.kd_timer_mana()
        self.radius.position = self.pers.position
        if not self.radius.check_collision(sprite_list=self.sprite_list):
            self.v_nikuda = True
        else:
            self.v_nikuda = False
            s = 0
            for sprite in self.sprite_list:
                if sprite.hp <= 0:
                    s += 1

            if len(self.sprite_list) == s:
                self.v_nikuda = True

        if self.action:
            if self.s < self.timer_for_s / 2:
                self.s_k = 1
                if not self.v_nikuda:
                    if self.calc:
                        self.calc = False
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
                            self.change_y = 0
                    else:
                        for sprite in self.slovar_rast:
                            if self.slovar_rast[sprite] == self.rast and sprite.hp > 0:
                                self.update_storona(sprite)
                                self.change_x = self.change * self.storona
                else:
                    self.update_storona(self.pers, 1)
                    self.change_x = self.change * self.storona
                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self, sprite) and sprite.hp > 0:
                        self.s = self.timer_for_s / 2
                        self.change_x *= -1
                        self.sprite = sprite
                        self.oglush(sprite)
                        self.timer_for_s_dvizh = self.timer_for_s / 2
                        self.dvizh_sprite_func(sprite, physics_engine)

                if self.sprite is None and self.s == self.timer_for_s / 2 - 1:
                    self.v_nikuda = True
            else:
                if self.v_nikuda or self.sprite is None:
                    self.s += self.timer_for_s
                    return
                else:
                    if abs(self.pers.center_x - self.sprite.center_x) < 150:
                        self.s_k = 3
                        if self.action_storona == 1:
                            self.right = self.pers.center_x
                        else:
                            self.left = self.pers.center_x
                        self.center_y = self.pers.center_y
                        self.change_x = 0
                        if arcade.check_for_collision(self.sprite, self) and not self.kombo:
                            self.kombo = True
                            self.s_kombo = self.s
                            self.dvizh_force = (80000, 3000)
                            self.dvizh_vel = 450
                            self.sbiv(self.sprite)
                            self.oglush(self.sprite)
                            self.udar(self.sprite)
                            self.timer_for_s_dvizh = 30
                            self.dvizh_sprite_func(self.sprite, physics_engine)
                            self.s_k = 0
                    if self.kombo and abs(self.s_kombo - self.s) > 30:
                        self.s += self.timer_for_s
                if self.s_k != 3:
                    self.s_k = 2
                    if abs(self.sprite.center_x - self.center_x) > 50:
                        if self.action_storona == 0:
                            self.right = self.sprite.center_x
                        else:
                            self.left = self.sprite.center_x
        else:
            self.kombo = False
            self.dvizh_force = (-80000, 0)
            self.dvizh_vel = 1000
            self.update_position()
            self.calc = True
            self.v_nikuda = False
            self.change_x = self.s_k = 0

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.s_k == 1:
            self.texture = self.dlan_texture[self.action_storona]
        elif self.s_k == 2:
            self.texture = self.hvat_texture[self.action_storona]
        elif self.s_k == 3:
            self.texture = self.udar_texture[self.action_storona]


class Priliv(voda.VodaFight, dvizh.DvizhPersAndSprite):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list, 200)
        self.sposob = sposobs.PRILIV
        self.osn = True

        self.uron = 200
        self.minus_mana = 5

        self.timer_for_s = 60
        self.timer_for_s_kd = self.s_kd = 180
        self.timer_for_s_oglush = 90

        self.timer_for_s_dvizh = self.timer_for_s_dvizh_sprite = 30
        self.dvizh_force = (70000, 0)
        self.dvizh_vel = 1000
        self.dvizh_vel_sprite = 900
        self.timer = True

        self.dvizh_force_sprite = (20000, 0)

        self.priliv_texture = arcade.load_texture_pair("resources/Sposob_animations/priliv.png")
        self.texture = self.priliv_texture[0]

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        super().on_update()
        self.update_sposob()
        self.update_v()
        if self.s == 1:
            self.pers.oglush_for_sposob = True
            self.dvizh_pers_func(physics_engine)
            self.func_mana()
        self.update_mor()
        self.kd_timer_mana()
        self.update_position()

        if self.action:
            self.pers.oglush_for_sposob = True
            physics_engine.set_friction(self.pers, 0)
            for sprite in self.sprite_list:
                if arcade.check_for_collision(sprite, self):
                    self.timer_for_s_dvizh_sprite = self.timer_for_s_oglush = self.timer_for_s - self.s + 30
                    self.udar(sprite)
                    self.dvizh_sprite_func(sprite, physics_engine)
                    self.oglush(sprite)
                    self.sbiv(sprite)
        else:
            self.pers.oglush_for_sposob = False

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)
        self.update_dvizh_pers(physics_engine)

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        super().draw(pixelated=pixelated)
        self.texture = self.priliv_texture[self.pers.storona]


class VodMarionetki(voda.Voda):
    def __init__(self, pers, sprite_list, walls_list):
        super().__init__(pers, sprite_list, 80)
        self.__walls_list = walls_list
        self.__mari_list = arcade.SpriteList()
        self.__x_list = [300, 250, -300]

        self.sposob = sposobs.VOD_MARIONETKA
        self.osn = True

        self.timer_for_s = 1800
        self.timer_for_s_kd = 1

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.update_v()
        if self.s > self.timer_for_s:
            self.action = False
            self.kd = True
            self.s = 0
        elif self.s == 1:
            self.func_mana()
            self.__create(physics_engine)
        if self.kd:
            self.s_kd += 1
            if self.s_kd > self.timer_for_s_kd:
                self.s_kd = 0
                self.kd = False

        if self.action:
            self.s += 1
            for mari in self.__mari_list:
                mari.on_update()
                mari.action(self.sposob)
        else:
            self.__remove(physics_engine)

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        super().draw(pixelated=pixelated)
        self.__mari_list.draw(pixelated=pixelated)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        for mari in self.__mari_list:
            mari.update_animation()

    def __create(self, physics_engine: arcade.PymunkPhysicsEngine):
        def create_sposob(mari):
            hlist = Hlist(mari, self.sprite_list)
            mari.sposob_list.append(hlist)
            rech_drakon = RechnoyDrakon(mari, self.sprite_list)
            mari.sposob_list.append(rech_drakon)
            volna = Volna(mari, self.sprite_list)
            mari.sposob_list.append(volna)
            tayfun = Tayfun(mari, self.sprite_list, True)
            mari.sposob_list.append(tayfun)
            udar_kita = UdarKita(mari, self.sprite_list)
            mari.sposob_list.append(udar_kita)
            lezviya = Lezviya(mari, self.sprite_list)
            mari.sposob_list.append(lezviya)
            big_volna = BigVolna(mari, self.sprite_list)
            mari.sposob_list.append(big_volna)
            briz = Briz(mari, self.sprite_list)
            mari.sposob_list.append(briz)
            priliv = Priliv(mari, self.sprite_list)
            mari.sposob_list.append(priliv)
            voda_udars = v_dop.VodaFightUdars(mari, self.sprite_list)
            mari.sposob_list.append(voda_udars)
            for sposob in mari.sposob_list:
                sposob.uron /= 1.5
                sposob.minus_mana /= 1.5
                sposob.minus_v /= 1.5
                sposob.scale /= 1.5

        for x in self.__x_list:
            mari = mobs.Marionetka(f"Marionetka {x}", self.sprite_list, self.__walls_list, self.pers)
            mari.position = self.pers.center_x + x, self.pers.center_y
            voda.V_LIST.append(mari)
            create_sposob(mari)
            self.__mari_list.append(mari)
            physics_engine.add_sprite(mari, friction=0, elasticity=1, moment_of_inertia=physics_engine.MOMENT_INF,
                                      max_horizontal_velocity=300, collision_type="vod_marionetka")

    def __remove(self, physics_engine: arcade.PymunkPhysicsEngine):
        if len(self.__mari_list) > 0:
            for mari in self.__mari_list:
                voda.V_LIST.remove(mari)
                physics_engine.remove_sprite(mari)
            self.__mari_list.clear()
