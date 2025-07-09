import arcade

import hit_box_and_radius
import sposobs
from sposobs import fiz_sposob
from sposobs.stihiya import ogon


class ColdOruzhie(fiz_sposob.FizSposobFight):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = sposobs.COLD_ORUZHIE
        self.radius = hit_box_and_radius.Radius(self, 0.2)

    def update_storona(self):
        if self.action:
            self.texture = self.udar_texture[self.pers.storona]
            self.hit_box._points = self.texture.hit_box_points
            # return
        if self.pers.block.block or self.pers.block.avto_block:
            self.texture = self.block_texture[self.pers.storona]
            self.hit_box._points = self.texture.hit_box_points

    def block_functions(self):
        if self.main_block:
            self.block_block()
            self.update_block()

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        pass


class MechOgon(ColdOruzhie, ogon.Ogon):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.sposob = sposobs.MECH_OGON
        self.uron = 50
        self.tik_uron = 5
        self.minus_stamina = 5
        self.minus_block_stamina = 0.1
        self.minus_mana = 1

        self.timer_for_s_tik = 60

        self.ogon_state = False

        self.udar_texture = arcade.load_texture_pair('nuzhno/mech.png')
        self.udar_ogon_texture = arcade.load_texture_pair('nuzhno/mech_ogon.png')
        self.block_texture = arcade.load_texture_pair('nuzhno/mech_ogon_block.png')
        self.scale = 2
        self.texture = self.udar_texture[1]

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.update_mor()
        self.kd_timer_stamina()
        self.update_position()
        self.block_functions()
        self.otdacha(physics_engine)
        self.radius.position = self.pers.position

        if self.s == 1:
            self.func_stamina()
            if self.ogon_state:
                self.func_mana()

        if self.action:
            for sprite in self.sprite_list:
                if ((not sprite.fight and arcade.check_for_collision(self, sprite)) or
                        (sprite.fight and arcade.check_for_collision(self, sprite.hit_box_2))):
                    self.pred_s_popal += 1
                    if self.ogon_state:
                        self.udar_or_block(sprite, self.uron * 2)
                        self.tik(sprite)
                    else:
                        self.udar_or_block(sprite)

            if self.pred_s_popal == 0:
                self.s_popal = 0

        self.update_tik()
        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()
        if self.action and not self.block and self.ogon_state:
            self.texture = self.udar_ogon_texture[self.pers.storona]
            self.hit_box._points = self.texture.hit_box_points


class ObichMech(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.sposob = sposobs.OBICH_MECH
        self.uron = 50

        self.udar_texture = arcade.load_texture_pair('nuzhno/udar.png')
        self.block_texture = arcade.load_texture_pair('nuzhno/udar_block.png')
        self.texture = self.udar_texture[0]
        self.scale = 1.5

        self.s_kd = self.timer_for_s_kd + 5
        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.update_block()
        self.block_block()
        self.kd_timer_stamina()
        self.update_position()
        self.otdacha(physics_engine)
        self.radius.position = self.pers.position

        # if self.s == 1:
        #     self.pers.stamina -= self.minus_stamina

        if self.action:
            self.block = self.avto_block = False
            if self.pers.storona == 0:
                self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
            elif self.pers.storona == 1:
                self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar_or_block(sprite)

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class DvuruchMech(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = sposobs.DVURUCH_MECH

        self.uron = 120

        self.udar_texture = arcade.load_texture_pair('nuzhno/udar.png')
        self.texture = self.udar_texture[0]
        self.scale = 1.5

        self.s_kd = self.timer_for_s_kd + 5
        self.minus_stamina = 2

        self.probit_block = False
        self.s_probit_block = 0
        self.kombo = False
        for oruzh in self.pers.oruzh_list:
            if oruzh.tip == sposobs.RIVOK:
                self.kombo = True

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.otdacha(physics_engine)
        self.update_block()
        self.block_block()
        if self.probit_block:
            self.s_probit_block += 1
        if self.s_probit_block > 15:
            self.s_probit_block = 0
            self.probit_block = False

        self.kd_timer_stamina()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.kombo:
            for oruzh in self.pers.oruzh_list:
                if oruzh.tip == sposobs.RIVOK and oruzh.action:
                    self.probit_block = True
                    self.s_probit_block = 0

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and not self.probit_block:
                    self.udar_or_block(sprite)
                elif arcade.check_for_collision(self, sprite) and self.probit_block:
                    self.udar(sprite)

        self.update_slovar()

        self.position = self.pers.position

        if self.pers.storona == 0:
            self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
        elif self.pers.storona == 1:
            self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class Shchit(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.sposob = sposobs.SHCHIT
        self.uron = 80

        self.scale = 0.5
        self.block_texture = arcade.load_texture_pair('nuzhno/shcit.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/shcit_udar.png')
        self.texture = self.block_texture[1]

        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.otdacha(physics_engine)
        self.update_sposob()
        self.update_block()
        self.block_block()

        self.kd_timer_stamina()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        self.center_y = self.pers.center_y
        if not self.action:
            if self.pers.storona == 1:
                self.center_x = self.pers.center_x - 20
            else:
                self.center_x = self.pers.center_x + 20
        else:
            if self.pers.storona == 1:
                self.center_x = self.pers.center_x - 60
            else:
                self.center_x = self.pers.center_x + 60

        if self.action:
            self.s += 1
            self.block = self.avto_block = False
            for sprite in self.sprite_list:
                if arcade.check_for_collision(sprite, self):
                    self.udar_or_block(sprite)

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class Vila(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s=50, timer_for_s_kd=20):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = sposobs.VILA
        self.uron = 40

        self.s_kd = self.timer_for_s_kd + 5

        self.udar_texture = arcade.load_texture_pair('nuzhno/vila.png')
        self.texture = self.udar_texture[0]

        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.otdacha(physics_engine)
        self.update_block()
        self.block_block()

        self.kd_timer_mana()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.action:
            if self.pers.storona == 0:
                if self.s < self.timer_for_s // 2:
                    self.change_x = 3
                elif self.timer_for_s // 2 <= self.s < self.timer_for_s:
                    self.change_x = -3
            elif self.pers.storona == 1:
                if self.s < self.timer_for_s // 2:
                    self.change_x = -3
                elif self.timer_for_s // 2 <= self.s < self.timer_for_s:
                    self.change_x = 3

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and self.s < 30:
                    self.udar_or_block(sprite)

        self.update_slovar()

        if not self.action:
            self.center_y = self.pers.center_y
            if self.pers.storona == 0:
                self.center_x = self.pers.center_x + 20
            elif self.pers.storona == 1:
                self.center_x = self.pers.center_x - 20

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class Topor(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = sposobs.TOPOR
        self.uron = 50

        self.s_kd = self.timer_for_s_kd + 5

        self.udar_texture = arcade.load_texture_pair('nuzhno/topor0.png')
        self.texture = self.udar_texture[0]
        self.angle = 10

        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_position()
        self.update_sposob()
        self.otdacha(physics_engine)
        self.update_block()
        self.block_block()

        self.kd_timer_mana()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.action:
            if 10 <= self.s < 20:
                if self.pers.storona == 1:
                    self.change_angle = -12
                else:
                    self.change_angle = 12
            else:
                self.change_angle = 0
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar_or_block(sprite)
        else:
            self.angle = 10

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class MechBrenda(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = sposobs.MECH_BRENDA
        self.uron = 180

        self.udar_texture = arcade.load_texture_pair('nuzhno/mech_Brenda0.png')
        self.texture = self.udar_texture[0]

        self.s_kd = self.timer_for_s_kd + 5
        self.minus_stamina = 2
        self.s1 = 1

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_sposob()
        self.otdacha(physics_engine)
        self.update_block()
        self.block_block()

        self.kd_timer_mana()
        if self.s == 1 and self.action:
            self.pers.stamina -= self.minus_stamina * self.s1
            self.s1 += 1

        if self.s1 > 5:
            self.s1 = 1

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar_or_block(sprite)

        if self.pers.storona == 0:
            self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
        elif self.pers.storona == 1:
            self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()
