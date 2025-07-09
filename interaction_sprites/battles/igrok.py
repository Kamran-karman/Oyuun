import arcade
import random

import animations.pers_animations
import sposobs
from instruments import PNG
from interaction_sprites.battles import effect_update
from interaction_sprites import battles
from sposobs import fiz_sposob
from sposobs.stihiya import voda
from sposobs.stihiya.voda import v_osn
from sposobs.stihiya.voda import v_dop
from animations.pers_animations import spec_battle_animations


class Oyuun(battles.VodaPers):
    def __init__(self, sprite_list, walls_list: arcade.SpriteList):
        super().__init__('Oyuun', sprite_list, walls_list)
        self.max_hp = 2500
        self.max_mana = 10000
        self.max_stamina = 300
        self.harakteristiki()

        self.reakciya = 75
        self.vel_x = 300

        self.udar = fiz_sposob.Udar(self, sprite_list, 15, 30, True)
        self.udar.main_block = False
        self.uron = 30
        self.sposob_list.append(self.udar)

        self.animations = spec_battle_animations.OyuunAnimations(self)

        # self.hit_box_2 = hit_box_and_radius.HitBox(self.animations.idle_texture, self)

        self.v_max = 4000
        self.v = self.v_max
        self.v_plus = 1 / 6
        self.kritik = False
        voda.V_LIST.append(self)

        self.toggle = False

        self.five_sposobs = arcade.SpriteList()

        self.hlist = v_osn.Hlist(self, self.sprite_list)
        self.sposob_list.append(self.hlist)
        self.five_sposobs.append(self.hlist)
        self.rech_drakon = v_osn.RechnoyDrakon(self, self.sprite_list)
        self.sposob_list.append(self.rech_drakon)
        self.five_sposobs.append(self.rech_drakon)
        # self.iskl_list.append(self.rech_drakon.sposobs)
        self.volna = v_osn.Volna(self, self.sprite_list)
        self.sposob_list.append(self.volna)
        self.five_sposobs.append(self.volna)
        self.tayfun = v_osn.Tayfun(self, self.sprite_list, True)
        self.sposob_list.append(self.tayfun)
        self.five_sposobs.append(self.tayfun)
        self.udar_kita = v_osn.UdarKita(self, self.sprite_list)
        self.sposob_list.append(self.udar_kita)
        self.five_sposobs.append(self.udar_kita)
        self.techenie = v_dop.Reka(self, self.sprite_list, 900, True)
        self.sposob_list.append(self.techenie)
        self.voda_udars = v_dop.VodaFightUdars(self, self.sprite_list)
        self.sposob_list.append(self.voda_udars)
        self.iskl_list.append(self.voda_udars.sposob)
        self.voda_shchit = v_dop.VodaShchit(self, self.sprite_list)
        self.voda_shchit.main_block = True
        self.iskl_list.append(self.voda_shchit.sposob)
        self.sposob_list.append(self.voda_shchit)

        self.block = self.voda_shchit

        self.appends_voda_sposobs()

        self.color_hit_box = []
        for i in range(9):
            self.color_hit_box.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def pymunk_moved(self, physics_engine: arcade.PymunkPhysicsEngine, dx, dy, d_angle):
        if self.voda_shchit.fizika != physics_engine:
            self.voda_shchit.fizika = physics_engine
        self._battle_update_storona(dx, battles.X_D_ZONE)
        self.fizika.update(physics_engine, dx, dy)
        self.udar.update_udar(dx, battles.X_D_ZONE, physics_engine)
        # self.fizika.is_on_ground = physics_engine.is_on_ground(self)
        self.kvadrat_radius.update()

        # for sposob in self.sposob_list:
        #     sposob.position = self.position

        self.animations.tipo_return = False
        self.update_voda_list(physics_engine)

        if not self.oglush_for_sposob:
            self.animations.chest_animation()
            if self.animations.tipo_return:
                return
            self.animations.read_animation()
            if self.animations.tipo_return:
                return
            self.animations.gotov_animation()
            if self.animations.tipo_return:
                return

            self.animations.udaren_animation()
            if self.animations.tipo_return:
                return
            self.udar.update_udar_animation()
            self.animations.udar_animations()
            if self.animations.tipo_return:
                return
            self.animations.block_animation()
            if self.animations.tipo_return:
                return

        self.animations.plus_animations(dx, dy, self.fizika.is_on_ground, battles.X_D_ZONE, battles.Y_D_ZONE,
                                        self.fizika.x_odometr, 5)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._update_hp()

        self.update_sposob_list(self.fizika.fizika)

        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.draw_sposob_list()
        self.voda_udars.draw()

        # self.draw_hit_box(arcade.color.RED)


class BetaOyuun(battles.VodaPers):
    def __init__(self, sprite_list, walls_list: arcade.SpriteList):
        super().__init__('Oyuun', sprite_list, walls_list)
        self.max_hp = 40000
        self.max_mana = 10000
        self.max_stamina = 12000
        self.harakteristiki()

        self.reakciya = 75
        self.vel_x = 300

        self.udar = fiz_sposob.Udar(self, self.sprite_list, 15, 30, True)
        self.udar.main_block = False
        self.uron = 30
        self.sposob_list.append(self.udar)
        udar_main_patch = 'nuzhno/Oyuun/master/udar'
        self.udar.idle_udar_texture_list.load_textures(2, udar_main_patch, PNG)
        self.udar.jump_udar_texture_list.load_textures(2, udar_main_patch + '_W', PNG)
        self.udar.jump_dvizh_udar_texture_list.load_textures(2, udar_main_patch + '_WAD', PNG)
        self.udar.move_udar_texture_list.load_textures(2, udar_main_patch + '_move', PNG)

        self.animations = spec_battle_animations.OyuunAnimations(self)
        texture_toggle = arcade.load_texture_pair("resources/Pers_animations/battle/Oyuun/idle/0.png")
        self.toggle_animations = animations.pers_animations.ToggleAnimation(self, texture_toggle[0], texture_toggle[1])

        self.v_max = 10000
        self.v = self.v_max
        self.v_plus = 1 / 3
        voda.V_LIST.append(self)

        self.toggle = False

        self.five_sposobs = arcade.SpriteList()
        self.osn_sposobs = arcade.SpriteList()

        self.hlist = v_osn.Hlist(self, sprite_list)
        self.sposob_list.append(self.hlist)
        self.five_sposobs.append(self.hlist)
        self.rech_drakon = v_osn.RechnoyDrakon(self, sprite_list)
        self.sposob_list.append(self.rech_drakon)
        self.five_sposobs.append(self.rech_drakon)
        # self.iskl_list.append(self.rech_drakon.sposobs)
        self.volna = v_osn.Volna(self, sprite_list)
        self.sposob_list.append(self.volna)
        self.five_sposobs.append(self.volna)
        self.tayfun = v_osn.Tayfun(self, sprite_list, True)
        self.sposob_list.append(self.tayfun)
        self.five_sposobs.append(self.tayfun)
        self.udar_kita = v_osn.UdarKita(self, sprite_list)
        self.sposob_list.append(self.udar_kita)
        self.five_sposobs.append(self.udar_kita)
        self.lezviya = v_osn.Lezviya(self, sprite_list)
        self.sposob_list.append(self.lezviya)
        self.big_volna = v_osn.BigVolna(self, sprite_list)
        self.sposob_list.append(self.big_volna)
        self.briz = v_osn.Briz(self, sprite_list)
        self.sposob_list.append(self.briz)
        self.priliv = v_osn.Priliv(self, sprite_list)
        self.sposob_list.append(self.priliv)
        self.vod_marionetki = v_osn.VodMarionetki(self, sprite_list, walls_list)
        self.sposob_list.append(self.vod_marionetki)
        self.techenie = v_dop.Reka(self, self.sprite_list, 900, True)
        self.sposob_list.append(self.techenie)
        self.voda_udars = v_dop.VodaFightUdars(self, sprite_list)
        self.sposob_list.append(self.voda_udars)
        self.iskl_list.append(self.voda_udars.sposob)
        self.voda_shchit = v_dop.VodaShchit(self, sprite_list)
        self.voda_shchit.main_block = True
        self.iskl_list.append(self.voda_shchit.sposob)
        self.sposob_list.append(self.voda_shchit)

        self.block = self.voda_shchit

        self.appends_voda_sposobs()
        self.appends_osn_sposobs()

        self.color_hit_box = []
        for i in range(9):
            self.color_hit_box.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def pymunk_moved(self, physics_engine: arcade.PymunkPhysicsEngine, dx, dy, d_angle):
        if self.voda_shchit.fizika != physics_engine:
            self.voda_shchit.fizika = physics_engine
        self._battle_update_storona(dx, battles.X_D_ZONE)
        self.fizika.update(physics_engine, dx, dy)
        if abs(dx) > battles.X_D_ZONE and not self.beg:
            self.walk = True
        else:
            self.walk = False
        self.udar.update_udar(dx, battles.X_D_ZONE, physics_engine)
        # self.fizika.is_on_ground = physics_engine.is_on_ground(self)

        # for sposob in self.sposob_list:
        #     sposob.position = self.position

        self.animations.tipo_return = False
        self.update_voda_list(physics_engine)

        if not self.oglush_for_sposob and not self.toggle:
            self.animations.chest_animation()
            if self.animations.tipo_return:
                return
            self.animations.read_animation()
            if self.animations.tipo_return:
                return
            self.animations.gotov_animation()
            if self.animations.tipo_return:
                return

            self.animations.udaren_animation()
            if self.animations.tipo_return:
                return
            self.udar.update_udar_animation()
            self.animations.udar_animations()
            if self.animations.tipo_return:
                return
            self.animations.block_animation()
            if self.animations.tipo_return:
                return

            self.animations.plus_animations(dx, dy, self.fizika.is_on_ground, battles.X_D_ZONE, battles.Y_D_ZONE,
                                            self.fizika.x_odometr, 5)
        if self.toggle:
            if self.storona == 0:
                self.toggle_animations.animation(True)
            else:
                self.toggle_animations.animation(False)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob_list(self.fizika.fizika)

        self._update_harakteristiki()
        self._update_hp()
        self.kvadrat_radius.update()

        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.draw_sposob_list()
        self.voda_udars.draw()

        # self.draw_hit_box(arcade.color.RED)

    def appends_osn_sposobs(self):
        for sposob in self.sposob_list:
            if sposob.osn:
                self.osn_sposobs.append(sposob)

