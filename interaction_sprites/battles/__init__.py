import random
from typing import Any

import hit_box_and_radius
import interaction_sprites
import arcade

import sposobs
from sposobs import fiz_sposob

X_D_ZONE = 0.005
Y_D_ZONE = 5


def effect_update(effect: bool, s_effect: int, timer_for_s_effect: int):
    if effect:
        s_effect += 1
        if s_effect >= timer_for_s_effect:
            effect = False
            s_effect = 0
    return s_effect, effect


class BattleSprite(interaction_sprites.DvizhInteractionSprite, interaction_sprites.DialogSprite):
    def __init__(self, name: str, walls_list: arcade.SpriteList):
        super().__init__()
        self.name = name

        self.max_hp = 0
        self.hp = 0
        self.bessmert = False
        self.smert = False

        self.fight = False

        self.dvizh = False
        self.uzhe_dvizh = False
        self.slovar_dvizh = {}

        self.sbiv = False

        self.vel_x = 0
        self.vel_y = 0
        self.new_force = [0, 0]

        self.pers = False
        self.udaren = False

        self.fizika = interaction_sprites.DopFizikaInSprite(self, walls_list)

    def _update_hp(self):
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        elif self.hp <= 0:
            self.smert = True


class BattlePers(BattleSprite):
    def __init__(self, name: str, sprite_list, walls_list: arcade.SpriteList):
        super().__init__(name, walls_list)
        self.pers = True
        self.sprite_list = sprite_list

        self.__s_mana = 0
        self.__timer_for_s_mana = 600
        self.mana = 0
        self.max_mana = 0
        self.mor = False
        self.__s_mor = 0
        self.__timer_for_s_mor = 0
        self.__s_stamina = 0
        self.__timer_for_s_stamina = 180
        self.stamina = 0
        self.__last_stamina = self.stamina
        self.max_stamina = 0
        self.slabweak = False
        self.__s_slabweak = 0
        self.__timer_for_s_slabweak = 0

        self.sposob_list = arcade.SpriteList()

        self.oglush = False
        self.s_oglush = 0
        self.timer_for_s_oglush = 0

        self.stan = False

        self.sil = False

        self.stan_for_sposob = False
        self.s_stan_f_sp = 0
        self.timer_for_s_stan_f_sp = 0

        self.oglush_for_sposob = False

        self.tik_slovar = {}

        self.reakciya = 0

        self.uron = 0
        self.udar = fiz_sposob.Udar(self, self.sprite_list)

        self.block = self.udar
        self.avto_block = self.udar

        self.kvadrat_radius = hit_box_and_radius.KvadratRadius(self, self.scale)

        self.iskl_list = []

        self.popad = False
        self._s_popad = 0
        self.__timer_for_s_popad = 10

    def harakteristiki(self):
        self.hp = self.max_hp
        self.mana = self.max_mana
        self.stamina = self.__last_stamina = self.max_stamina

    def _update_harakteristiki(self):
        self.__s_mana += 1
        if self.__s_mana >= self.__timer_for_s_mana:
            self.s = 0
            if self.mor:
                self.mana += 0.5
                self.hp -= 0.5
            else:
                self.mana += 0

        self.__s_stamina += 1
        if self.__last_stamina > self.stamina:
            self.__last_stamina = self.stamina
            self.__s_stamina = 0
        if self.__s_stamina >= self.__timer_for_s_stamina:
            if self.slabweak:
                self.stamina += 0.2
                self.mana -= 2
            else:
                self.stamina += 1
                self.__last_stamina = self.stamina

        self._update_hp()

        if self.mor:
            self.__s_mor += 1
            if self.__s_mor >= self.__timer_for_s_mor:
                self.mor = False
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        if self.mana < 0:
            self.__s_mor = 0
            self.mor = True

        if self.slabweak:
            self.__s_slabweak += 1
            if self.__s_slabweak >= self.__timer_for_s_slabweak:
                self.slabweak = False
        if self.stamina >= self.max_stamina:
            self.stamina = self.max_stamina
        if self.stamina < 0:
            self.slabweak = True
            self.__s_slabweak = 0

    def _battle_update_storona(self, dx, x_d_zone):
        rf = False
        if self.block.tip == sposobs.COLD_ORUZHIE:
            if self.block.rf:
                rf = True

        if not rf:
            self._update_storona(dx, x_d_zone)
            def on_update_storona():
                if self.center_x > sprite.center_x:
                    self.storona = 1
                elif self.center_x < sprite.center_x:
                    self.storona = 0

            def dop_update_storona():
                for sposob in self.sposob_list:
                    if abs(dx) < X_D_ZONE or sposob.action:
                        on_update_storona()

            for sprite in self.sprite_list:
                if sprite.hp > 0:
                    if self.block.block:
                        on_update_storona()
                    elif self.kvadrat_radius.check_collision(sprite):
                        on_update_storona()
                        dop_update_storona()
                    elif sprite.pers:
                        if self.kvadrat_radius.check_collision(sprite.block) and sprite.block.block:
                            on_update_storona()
                            dop_update_storona()
        #
        # for wall in self.fizika.walls_list:
        #     if self.kvadrat_radius.check_collision(wall) and wall.top > self.bottom:
        #         if self.center_x > wall.center_x and dx > X_D_ZONE:
        #             self.storona = -1
        #         elif self.center_x < wall.center_x and dx < X_D_ZONE:
        #             self.storona = 1

        # self.animations.update_storona()

    def action(self, sposob_1, toggle=False):
        for sposob in self.sposob_list:
            # if sposob.action and sposob.sposob != sposob_1 and not sposob.action_2:
            #     if sposob_1 == sposobs.VODA_UDARS:
            #         print(0)
            #     break
            if sposob.sposob == sposob_1:
                if toggle:
                    sposob.action = not sposob.action
                else:
                    sposob.action = True

    def update_sposob_list(self, physics_engine: arcade.PymunkPhysicsEngine):
        for sposob in self.sposob_list:
            sposob.sprite_list = self.sprite_list
            sposob: sposobs.Sposob
            if sposob.tip == sposobs.COLD_ORUZHIE or sposob.dvizh_sposob or sposob.podklass == sposobs.VODA:
                sposob: Any
                sposob.on_update(physics_engine=physics_engine)
            else:
                sposob.on_update()
            sposob.update()

    def draw_sposob_list(self):
        def draw_sposob(sposob):
            if len(self.iskl_list) > 0:
                for iskl in self.iskl_list:
                    if sposob.sposob == iskl:
                        break
                    else:
                        sposob.draw()
            else:
                sposob.draw()

        for sposob in self.sposob_list:
            sposob.update_animation()
            if sposob.action:
                draw_sposob(sposob)
            elif sposob.block_sposob:
                if sposob.block or sposob.avto_block:
                    draw_sposob(sposob)

    def oglush_force(self, force, friction, a):
        if self.oglush:
            if self.s_oglush >= self.timer_for_s_oglush or self.dvizh:
                return force, friction
            return (0, 0), friction * a
        return force, friction

    def avto_block_func(self, sprite):
        if (self.slabweak or ((sprite.storona == self.storona == 0 and sprite.center_x < self.center_x) or
            (sprite.storona == self.storona == 1 and sprite.center_x > self.center_x))
                or self.oglush):
            return False

        r = 10
        if self.block.block or self.block.avto_block:
            return True

        if self.reakciya > sprite.reakciya:
            if sprite.reakciya * r <= self.reakciya:
                self.block.avto_block = True
                return True
            else:
                shanc = 0
                while r >= 0.1:
                    if (round(sprite.reakciya * (r - 0.1), 1) < round(sprite.reakciya * r, 1)
                            <= self.reakciya):
                        break
                    r -= 0.1
                    shanc += 1

                rand = random.randint(1, 100)
                while shanc > 0:
                    if rand == shanc:
                        self.block.avto_block = True
                        return True
                    shanc -= 1

                return False
        elif self.reakciya < sprite.reakciya:
            if sprite.reakciya >= self.reakciya * r:
                return False
            else:
                shanc = 100
                while r >= 0.1:
                    if round(self.reakciya * (r - 0.1), 1) < round(self.reakciya * r, 1) <= sprite.reakciya:
                        break
                    r -= 0.1
                    shanc -= 1

                rand = random.randint(1, 100)
                while shanc > 0:
                    if rand == shanc:
                        self.block.avto_block = True
                        return True
                    shanc -= 1

                return False
        else:
            if random.randint(0, 1) == 1:
                self.block.avto_block = True
                return True
            else:
                return False

    def update_popad(self):
        if self.popad:
            self._s_popad += 1
            if self._s_popad >= self.__timer_for_s_popad:
                self._s_popad = 0
                self.popad = False


class StihiyaPers(BattlePers):
    def __init__(self, name: str, sprite_list, walls_list: arcade.SpriteList):
        super().__init__(name, sprite_list, walls_list)

        self.stihiya_sposobs = arcade.SpriteList()

    def appends_stihiya_sposobs(self):
        for sposob in self.sposob_list:
            if sposob.klass == sposobs.STIHIYA:
                self.stihiya_sposobs.append(sposob)


class VodaPers(StihiyaPers):
    def __init__(self, name: str, sprite_list, walls_list: arcade.SpriteList):
        super().__init__(name, sprite_list, walls_list)
        self.v_max = 0
        self.v = self.v_max
        self.v_plus = 0

        self.kritik = False

        self.voda_list = arcade.SpriteList()

    def appends_voda_sposobs(self):
        self.appends_stihiya_sposobs()
        for stihiya in self.stihiya_sposobs:
            self.voda_list.append(stihiya)

    def update_voda_list(self, physics_engine):
        for v in self.voda_list:
            v.fizika = physics_engine
            for sprite in self.sprite_list:
                v.pred_vel_x = sprite.vel_x

    def prityag_voda(self):
        self.v += self.v_max / 2
        if self.v > self.v_max:
            self.v = self.v_max

