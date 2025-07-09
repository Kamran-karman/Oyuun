import os
import random
import sys

import hit_box_and_radius
import instruments

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import sposobs
import arcade


class FizSposob(sposobs.Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.klass = sposobs.FIZ_SPOSOB

        self.minus_stamina = 0
        self.stamina = False

    def func_stamina(self, minus_stamina=-1):
        if self.pers.stamina > 0:
            if minus_stamina == -1:
                if self.pers.stamina >= self.minus_stamina:
                    self.pers.stamina -= self.minus_stamina
                    round(self.pers.stamina)
                    self.stamina = True
                else:
                    self.pers.stamina -= self.minus_stamina
                    round(self.pers.stamina)
                    self.stamina = False
                    self.s += self.timer_for_s
            else:
                if self.pers.stamina >= minus_stamina:
                    self.pers.stamina -= minus_stamina
                    round(self.pers.stamina)
                    self.stamina = True
                else:
                    self.pers.stamina -= minus_stamina
                    round(self.pers.stamina)
                    self.stamina = False
                    self.s += self.timer_for_s
        else:
            self.s += self.timer_for_s


class FizSposobFight(sposobs.Fight, FizSposob, sposobs.Block):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list)
        self.podklass = sposobs.FIZ_SPOSOB_FIGHT

        self.timer_for_s = timer_for_s
        self.timer_for_s_kd = timer_for_s_kd

        self.udar_texture = None

        self.timer_for_s_block = 60
        self.s_block = self.timer_for_s_block

        self.minus_block_stamina = 0
        self.minus_for_block = -1

        self.force_for_block = -1
        self.s_minus_block = 0
        self.return_force = 50000
        self.pred_return_force = self.return_force
        self.s_return_force = 0
        self.rf = False

        self.sposob_list = arcade.SpriteList()

    def otdacha(self, physics_engine: arcade.PymunkPhysicsEngine):
        if not self.rf:
            self.s_return_force = 0
            for sprite in self.sprite_list:
                for _sposob in sprite.sposob_list:
                    if _sposob.sposob == sposobs.VODA_UDARS:
                        for vu in _sposob.vu_list:
                            if arcade.check_for_collision(vu, self) and (self.block or self.avto_block) and vu.action:
                                if self.return_force != _sposob.force_for_block and _sposob.force_for_block != -1:
                                    self.return_force = _sposob.force_for_block
                                self.rf = True
                                if _sposob.minus_for_block != -1:
                                    self.func_stamina(_sposob.minus_for_block)
                                else:
                                    self.func_stamina(self.minus_block_stamina)
                                if not self.stamina:
                                    self.block = self.avto_block = False
                                if vu not in self.sposob_list:
                                    self.sposob_list.append(vu)
                    else:
                        if (_sposob.tip == (sposobs.VODA_FIGHT or sposobs.COLD_ORUZHIE)
                                and arcade.check_for_collision(_sposob, self)
                                and (self.block or self.avto_block) and _sposob.action and not _sposob.probit_block):
                            if self.return_force != _sposob.force_for_block and _sposob.force_for_block != -1:
                                self.return_force = _sposob.force_for_block
                            self.rf = True
                            if _sposob.minus_for_block != -1:
                                self.func_stamina(_sposob.minus_for_block)
                            else:
                                self.func_stamina(self.minus_block_stamina)
                            if not self.stamina:
                                self.block = self.avto_block = False
                            if _sposob not in self.sposob_list:
                                self.sposob_list.append(_sposob)
        else:
            self.s_return_force += 1
        if self.rf and 0 < self.s_return_force <= 7:
            if self.pers.storona == 0:
                physics_engine.apply_force(self.pers, (-self.return_force, 0))
            else:
                physics_engine.apply_force(self.pers, (self.return_force, 0))
            physics_engine.set_friction(self.pers, 0)

        for _sposob in self.sposob_list:
            if not _sposob.action and self.s_return_force >= 30:
                self.rf = False
                self.s_return_force = 0
                self.sposob_list.remove(_sposob)
                self.return_force = self.pred_return_force
            elif _sposob.action and (self.block or self.avto_block) and arcade.check_for_collision(_sposob, self):
                self.s_return_force = 0
                self.s_minus_block += 1
                if self.s_minus_block >= 30:
                    self.s_minus_block = 0
                    if _sposob.minus_for_block != -1:
                        self.func_stamina(_sposob.minus_for_block)
                    else:
                        self.func_stamina(self.minus_block_stamina)

    def block_block(self):
        if self.block:
            self.s_block += 1
        else:
            self.s_block = 0
        if self.s_block >= self.timer_for_s_block and self.block:
            self.s_block = 0
            self.func_stamina(self.minus_block_stamina)


class Udar(FizSposobFight):
    def __init__(self, pers, sprite_list, timer_for_s=45, timer_for_s_kd=105, master=False):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.sposob = sposobs.UDAR
        self.master = master

        self.radius = hit_box_and_radius.Radius(self, 0.13)

        self.s_kd = self.timer_for_s_kd + 5
        self.udar_texture = None

        self.idle_udar_texture_list = instruments.TextureList()
        self.jump_udar_texture_list = instruments.TextureList()
        self.jump_dvizh_udar_texture_list = instruments.TextureList()
        self.move_udar_texture_list = instruments.TextureList()

        self.scale = self.pers.scale + 0.06

        self.jump = False
        self.move = False

        self.main_block = True
        self.probit_block = False
        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if self.pers.sil:
            self.probit_block = True

        self.uron = self.pers.uron

        self.update_sposob()
        #self.update_scale()
        self.update_position()
        self.radius.position = self.pers.position
        self.update_block()
        self.kd_timer_stamina()

        # if self.s == 1:
        #     self.func_stamina()
        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    if not self.probit_block:
                        self.udar_or_block(sprite)
                    else:
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= self.uron

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        # self.draw_hit_box()
        self.udar_texture = self.pers.animations.udar_texture  # [self.pers.storona]
        self.texture = self.udar_texture[self.pers.storona]
        self.hit_box._points = self.texture.hit_box_points

    def update_udar(self, dx, x_d_zone, physics_engine: arcade.PymunkPhysicsEngine):
        if abs(dx) > x_d_zone:
            self.move = True
        else:
            self.move = False

        if not self.pers.fizika.is_on_ground:
            self.jump = True
        else:
            self.jump = False

        if self.action and abs(dx) < x_d_zone and not self.jump:
            if self.pers.storona == 0:
                storona = 1
            else:
                storona = -1
            physics_engine.apply_force(self.pers, (1356 * storona, 0))

    def update_udar_animation(self):
        if self.action:
            # self.udar_texture = self.pers.animations.udar_texture
            # self.texture = self.udar_texture[self.pers.storona]
            # self.hit_box._points = self.texture.hit_box_points
            self.pers.animations.tipo_return = True
        #else:
            if self.s == 1:
                if 0 < random.randint(1, 5) < 4:
                    index = 0
                else:
                    index = 1

                if self.jump and not self.move:
                    self.pers.animations.udar_texture = self.udar_texture = self.jump_udar_texture_list[index]
                    self.texture = self.jump_udar_texture_list[index][self.pers.storona]
                    self.hit_box._points = self.texture.hit_box_points
                elif self.move and not self.jump:
                    self.pers.animations.udar_texture = self.udar_texture = self.move_udar_texture_list[index]
                    self.texture = self.move_udar_texture_list[index][self.pers.storona]
                    self.hit_box._points = self.texture.hit_box_points
                elif self.move and self.jump:
                    self.pers.animations.udar_texture = self.udar_texture = self.jump_dvizh_udar_texture_list[index]
                    self.texture = self.jump_dvizh_udar_texture_list[index][self.pers.storona]
                    self.hit_box._points = self.texture.hit_box_points
                elif not self.move and not self.jump:
                    self.pers.animations.udar_texture = self.udar_texture = self.idle_udar_texture_list[index]
                    self.texture = self.idle_udar_texture_list[index][self.pers.storona]
                    self.hit_box._points = self.texture.hit_box_points

                # self.udar_texture = self.pers.animations.udar_texture  # [self.pers.storona]
                # self.texture = self.udar_texture[self.pers.storona]
                # self.hit_box._points = self.texture.hit_box_points


