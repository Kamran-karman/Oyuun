import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import sposobs
import hit_box_and_radius
import arcade


class Stihiya(sposobs.Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.klass = sposobs.STIHIYA

        self.minus_mana = 0
        self.mana = True

        self.voda = False
        self.molniya = False
        self.ogon = False
        self.veter = False
        self.zemlya = False

    def func_mana(self, minus_mana=float(-1)):
        if self.pers.mana > 0:
            if minus_mana == -1:
                if self.pers.mana >= self.minus_mana:
                    self.mana = True
                    self.pers.mana -= self.minus_mana
                else:
                    self.s += self.timer_for_s
                    self.mana = False
                    self.pers.mana -= self.minus_mana
            else:
                if self.pers.mana >= minus_mana:
                    self.mana = True
                    self.pers.mana -= minus_mana
                else:
                    self.s += self.timer_for_s
                    self.mana = False
                    self.pers.mana -= minus_mana
        else:
            self.s += self.timer_for_s


class StihiyaFight(Stihiya, sposobs.Fight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.radius = hit_box_and_radius.Radius(self.pers)

    def update_mor(self):
        if self.pers.mor:
            self.uron *= 2 / 3


class StihiyaBlock(Stihiya, sposobs.Block):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.timer_for_s_block = 60
        self.s_block = self.timer_for_s_block

        self.minus_block_mana = 0

        self.s_body_type = 0
        self.fizika = None

    def block_block(self):
        if self.block:
            self.s_block += 1
        else:
            self.s_block = 0
        if self.s_block >= self.timer_for_s_block and self.block:
            self.s_block = 0
            self.func_mana(self.minus_block_mana)

    def update_body_type(self, state=None):
        if state is None:
            state = self.block
        if state and self.s_body_type == 0:
            self.s_body_type += 1
            self.fizika.add_sprite(self, body_type=self.fizika.KINEMATIC)
        elif not state and self.s_body_type == 1:
            self.s_body_type -= 1
            self.fizika.remove_sprite(self)


class StihiyaImitation(StihiyaBlock):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.podklass = sposobs.STIHIYA_IMITATION

        self.s_add = 0
        self.s_remove = 2

    def update_pers_body_type(self, state=None):
        if state is None:
            state = self.action
        if state:
            self.s_remove = 0
            if self.s_add == 0:
                self.fizika.sprites[self.pers].body.body_type = self.fizika.KINEMATIC
            self.s_add += 1
        else:
            self.s_add = 0
            self.s_remove += 1
            if self.s_remove == 1:
                self.fizika.remove_sprite(self.pers)
                self.fizika.add_sprite(self.pers, 1, 1,
                                       max_vertical_velocity=2000,
                                       max_horizontal_velocity=300,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)
