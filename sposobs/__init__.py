import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import arcade
# from interaction_sprites import battles

# ___________________

FIZ_SPOSOB = 10000

FIZ_SPOSOB_FIGHT = 11000

SHCHITS = 11000
SHCHIT = 11001

COLD_ORUZHIE = 12000
OBICH_MECH = 12001
MECH_OGON = 12002
DVURUCH_MECH = 12002
VILA = 12004
TOPOR = 12005
MECH_BRENDA = 12006

DAL_ORUZH = 13000

RUKOPASH = 14000
UDAR = 14001

RIVOKS = 311000
RIVOK = 311100

# __________________

STIHIYA = 20000

STIHIYA_FIGHT = 21000
STIHIYA_BLOCK = 22000
STIHIYA_IMITATION = 23000

MOLNIAY = 21100
CEPNAYA_MOLNIYA = 21101
GNEV_TORA = 21102
STRELI_PERUNA = 21103
SHAR_MOLNIYA = 21104
UDAR_ZEVSA = 21105

VODA = 21200
VODA_FIGHT = 21210
SPUTNIK = 21211
SPUTNIKI = 21212
VOLNA = 21213
RECHNOY_DRAKON = 21214
UDAR_KITA = 21215
TAYFUN = 21216
HLIST = 21217
VODA_UDAR = 21218
VODA_UDARS = 21219
KARAKATICA = 212110
VODOHOD = 212111
TECHENIE = 212112
REKA = 212113
BIG_VOLNA = 212114
LEZVIYA = 212115
BRIZ = 212116
PRILIV = 212117
VOD_MARIONETKA = 212118
VODA_BLOCK = 22100
VODA_SHCHIT = 22101
VODA_IMITATION = 23200

ZEMLYA = 21300

VETER = 21400
PORIV = 21401

OGON = 21500
FIRE_BALL = 21501
YAZIKI_OGNYA = 21502
KULAK_OGNYA = 21503
MINI_FIRE_BALL = 21504
POLET = 21505


class Sposob(arcade.Sprite):
    def __init__(self, pers, sprite_list: arcade.SpriteList):
        super().__init__()
        self.pers = pers
        self.sprite_list = sprite_list

        self.action = False
        self.action_2 = False

        self.osn = False

        self.timer_for_s = 0
        self.timer_for_s_2 = 0
        self.timer_for_s_kd = 0
        self.timer_for_s_oglush = 0

        self.s = 0
        self.s_2 = 0
        self.s_kd = 0
        self.kd = False

        self.fight_sposob = False
        self.block_sposob = False
        self.dvizh_sposob = False

        self.klass = 0
        self.podklass = 0
        self.tip = 0
        self.podtip = 0
        self.nadsposob = 0
        self.sposob = 0

    def update_sposob(self):
        for sprite in self.sprite_list:
            if sprite.hp <= 0:
                self.sprite_list.remove(sprite)

        if self.pers.hp <= 0 or self.pers.oglush:
            self.s += self.timer_for_s

    def oglush(self, sprite):
        if sprite.max_hp == 6100:
            return
        if not sprite.oglush:
            sprite.oglush = True
            sprite.timer_for_s_oglush = self.timer_for_s_oglush
            sprite.s_oglush = 0


class Fight(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.fight_sposob = True

        self.uron = 0
        self.degree_block = 0
        self.probit_block = False

        self.slovar = {}

        self.s_popal = 0
        self.pred_s_popal = 0
        self.popal = False

    def update_slovar(self):
        if len(self.slovar) < len(self.sprite_list):
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
        while len(self.slovar) > len(self.sprite_list):
            for i in self.slovar:
                s = 0
                for sprite in self.sprite_list:
                    if sprite == i:
                        s += 1
                if s == 0:
                    self.slovar.pop(i)
                    return
        if not self.action:
            self.popal = False
            self.pred_s_popal = 0
            for i in self.slovar:
                self.slovar[i] = False

    def update_position(self, position_pers: tuple[float, float] = None, return_position: bool = False):
        if position_pers is None:
            if not return_position:
                self.position = self.pers.position
            else:
                center_x, center_y = self.pers.position
                return center_x, center_y
        else:
            if not return_position:
                self.position = position_pers
            else:
                center_x, center_y = position_pers
                return center_x, center_y

    def udar(self, sprite, uron=-1., popal=True):
        for i in self.slovar:
            if i == sprite and not self.slovar[i] and not sprite.bessmert:
                if self.popal:
                    self.popal = False
                    self.s_popal += 1
                self.slovar[i] = popal
                sprite.popad = True
                sprite._s_popad = 0
                if uron == -1:
                    sprite.hp -= round(self.uron)
                else:
                    sprite.hp -= round(uron)

    def kd_timer_stamina(self):
        if self.s_kd < self.timer_for_s_kd and self.s >= self.timer_for_s:
            self.kd = True
        elif self.s_kd >= self.timer_for_s_kd:
            self.kd = False

        if self.kd:
            self.action = False
            self.s_kd += 1

        if self.s >= self.timer_for_s:
            self.action = False
            self.s = 0

        if self.action:
            self.s += 1
        if self.action and self.s == 1:
            self.s_kd = 0

    def kd_timer_mana(self):
        self.s_kd += 1

        if self.s_kd <= self.timer_for_s_kd:
            self.kd = True
            self.action = False
        else:
            self.kd = False

        if self.s >= self.timer_for_s:
            self.action = False
            self.action_2 = False
            self.kd = True
            self.s_kd = 0
            self.s = 0
            self.s_2 = 0

        if self.action:
            self.kd = False
            self.s += 1

    def udar_or_block(self, sprite, uron=-1., popal=True):
        if sprite.max_hp == 6100:
            if uron != -1:
                self.udar(sprite, uron, popal)
            else:
                self.udar(sprite, popal=popal)
            return True
        if not sprite.avto_block_func(self.pers):
            self.popal = True
            if uron != -1:
                self.udar(sprite, uron, popal)
            else:
                self.udar(sprite, popal=popal)
            return True
        else:
            self.s_popal = 0
            for sposob in sprite.sposob_list:
                if sposob.sposob == UDAR and sposob.block:
                    if uron != -1:
                        self.udar(sprite, uron, popal)
                    else:
                        self.udar(sprite, popal=popal)
                    return False
                if self.sposob == UDAR:
                    if sposob.sposob == self.sposob and sposob.block:
                        if uron != -1:
                            self.udar(sprite, uron * 0.5, popal)
                        else:
                            self.udar(sprite, self.uron * 0.5, popal)
                        return False
                    return False
            if uron != -1:
                self.udar(sprite, uron * self.degree_block, popal)
            else:
                self.udar(sprite, self.uron * self.degree_block, popal)
            return False


class Block(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.block_sposob = True

        self.block_texture = None

        self.main_block = False
        self.block = False
        self.avto_block = False
        self.s_avto_block = 0
        self.timer_for_s_ab = 30

        self.block_vel = 0
        self.obich_vel = 0

    def update_block(self):
        # if self.main_block:
        #     self.block = self.pers.block.block
        #     self.avto_block = self.pers.block.avto_block
        if self.action:
            self.avto_block = self.block = self.pers.block.block = self.pers.block.avto_block = False
            return
        if self.avto_block or self.block:
            self.action = False

        if self.avto_block:
            #print(self.s_avto_block)
            self.s_avto_block += 1

        if self.s_avto_block >= self.timer_for_s_ab:
            self.pers.block.avto_block = False
            self.avto_block = False
            self.s_avto_block = 0
            #print(100)

