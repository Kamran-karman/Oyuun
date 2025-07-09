import random

from interaction_sprites import battles
from interaction_sprites.battles import mobs, effect_update, X_D_ZONE, Y_D_ZONE
from animations.pers_animations import spec_battle_animations, spec_plus_animations
import arcade
from sposobs.fiz_sposob import cold_oruzhie
from sposobs.stihiya import ogon

B_VEL_X = 300


class Balvanchik(mobs.Vrag):
    def __init__(self, igrok: battles.BattlePers, name: str, walls_list: arcade.SpriteList):
        super().__init__(igrok, name, walls_list)
        self.max_hp = 2000
        self.max_mana = 150
        self.max_stamina = 200
        self.harakteristiki()

        self.scale = 1.5

        self.reakciya = 60
        self.vel_x = self.walk_vel_x = B_VEL_X
        self.beg_vel_x = self.vel_x * 2

        self.block.timer_for_s_ab = 30

        self.animations = spec_battle_animations.BalvanchikAnimations(self)

        self.udar.scale = self.scale + 0.05
        self.uron = 10
        self.udar.main_block = False
        self.udar.timer_for_s_kd = 15
        self.sposob_list.append(self.udar)

        # self.mech = cold_oruzhie.ObichMech(self, self.sprite_list, 30, 30)
        # self.sposob_list.append(self.mech)
        # self._slovar_timer.update({self.mech: [30, False, 1]})

        self.mech = cold_oruzhie.MechOgon(self, self.sprite_list, 20, 25)
        self.mech.main_block = True
        self.mech.timer_for_s_kd = 50
        self.block = self.mech
        self.sposob_list.append(self.mech)

        self.kulak_ognya = ogon.KulakOgnya(self, self.sprite_list)
        self.kulak_ognya.timer_for_s_kd = 60
        self.sposob_list.append(self.kulak_ognya)

        self.fire_ball = ogon.FireBall(self, self.sprite_list)
        self.fire_ball.timer_for_s_kd = 300
        self.sposob_list.append(self.fire_ball)

        self.polet = ogon.Polet(self, self.sprite_list)
        self.sposob_list.append(self.polet)

        self.color_hit_box = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)

        self.povedenie = 0

        self.s_polet = 0
        self.polet_storona = 0
        self.p = 0

        self.otstup = False
        self.s_otstup = 0
        self.timer_for_s_otstup = 300
        self.otstup_rasst = 500

        self.s_kombo = 0
        self.mech_s_popal = 0
        self.kombo_mech = 2
        self.kombo_mech2 = 4

        self.s_mimo = 0

        self.s_block = 0
        self.timer_for_s_block = 30

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.fizika.update(physics_engine, dx, dy)
        if self.povedenie != 6:
            self._battle_update_storona(dx, X_D_ZONE)

        # self.udar.update_udar(dx, battles.X_D_ZONE, physics_engine)
        # print(self.block.avto_block, self.udar.avto_block)

        self.animations.tipo_return = False

        self.animations.smert_animation()
        if self.animations.tipo_return:
            return

        self.animations.sbiv_animation()
        if self.animations.tipo_return:
            return

        if not self.oglush and not self.oglush_for_sposob:
            self.animations.vstat_animation()
            if self.animations.tipo_return:
                return

            self.animations.udaren_animation()
            if self.animations.tipo_return:
                return

            self.animations.block_animation()
            if self.animations.tipo_return:
                return

            self.animations.udar_animations()
            if self.animations.tipo_return:
                return

            self.animations.plus_animations(dx, dy, self.fizika.is_on_ground, battles.X_D_ZONE, battles.Y_D_ZONE,
                                            self.fizika.x_odometr, 1)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._update_harakteristiki()
        self.update_sposob_list(self.fizika.fizika)

        if self.povedenie != 6:
            self._update_beg()
        self.ii()
        self.update_popad()

        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)

        if self.hp <= self.max_hp * 0.25 and self.povedenie < 4:
            self.povedenie = 4
            self.otstup = True
            self.mech.ogon_state = self.beg = self.popad = False
            self.mech_s_popal = self.s_kombo = self.mech.s_popal = self.s_mimo = self.force_x = 0
            self.mech.timer_for_s_kd = 50
        if self.popad and (self.povedenie < 3 or self.povedenie == 6):
            self.povedenie = 3
            self.mech_s_popal = self.s_kombo = self.mech.s_popal = self.s_mimo = self.force_x = 0
            self.mech.timer_for_s_kd = 50
            self.otstup = self.mech.ogon_state = self.beg = self.popad = False

        if not self.oglush and not self.kast_scena:
            rasst = abs(self.center_x - self.igrok.center_x)
            rasst_block = abs(self.center_x - self.igrok.block.center_x)

            if len(self.drug_list) != 0:
                dl = 0
                dr = 0
                sp = 0
                s = 0
                for drug in self.drug_list:
                    drug : Balvanchik
                    if drug.povedenie == 6:
                        sp += 1
                    if abs(drug.center_x - self.igrok.center_x) > rasst or drug.povedenie == 5:
                        s += 1

                    if drug.center_x < self.igrok.center_x:
                        dl += 1
                    elif drug.center_x > self.igrok.center_x:
                        dr += 1

                # minimum = round(len(self.drug_list) )* 0.4 if len(self.drug_list) * 0.4 > 0.5 else 1
                if sp == 0 and self.povedenie != 6 and (rasst <= 300 or rasst_block <= 300 and self.igrok.block.block):
                    if ((dr < self.perem and self.center_x < self.igrok.center_x)
                            or (dl < self.perem and self.center_x > self.igrok.center_x)):
                        self.povedenie = 6
                        self.mech_s_popal = self.s_kombo = self.mech.s_popal = self.s_mimo = self.force_x = 0
                        self.mech.timer_for_s_kd = 50
                        self.mech.ogon_state = self.beg = self.popad = False
                        if self.center_x > self.igrok.center_x:
                            self.polet_storona = 1
                        else:
                            self.polet_storona = 0
                        self.otstup = True
                        self.otstup_rasst = 200

                if not self.fire_ball.kd and not self.fire_ball.action and self.povedenie < 5 and s == 0:
                    self.povedenie = 5
                    self.mech_s_popal = self.s_kombo = self.mech.s_popal = self.s_mimo = self.force_x = 0
                    self.mech.timer_for_s_kd = 50
                    for drug in self.drug_list:
                        drug: Balvanchik
                        drug.fire_ball.s += drug.fire_ball.timer_for_s

            match self.povedenie:
                case 0:
                    if rasst <= self.d_zone * 2 or (rasst_block <= self.d_zone * 2 and self.igrok.block.block):
                        if not self.mech.kd and not self.mech.action:
                            self.mech.ogon_state = False
                            self.mech_s_popal += 1
                            self.action(self.mech.sposob)

                    if self.mech.s_popal == 2:
                        self.povedenie = 1
                    elif self.mech_s_popal == 4:
                        self.mech_s_popal = self.s_kombo = 0
                        self.mech.timer_for_s_kd = 50
                        self.povedenie = 2
                        self.otstup = True
                case 1:
                    if rasst <= self.d_zone * 2 or (rasst_block <= self.d_zone * 2 and self.igrok.block.block):
                        if (not self.mech.kd and not self.mech.action and ((self.mech_s_popal < self.kombo_mech
                                                                            and self.s_kombo == 0) or
                                     (self.mech_s_popal < self.kombo_mech2 and self.s_kombo == 1)) and not self.udar.action
                                and not self.kulak_ognya.action):
                            self.mech_s_popal += 1
                            self.action(self.mech.sposob)
                        elif (not self.udar.kd and not self.udar.action and self.s_kombo == 0
                              and self.mech_s_popal == self.kombo_mech and not self.mech.action):
                            if not self.udar.radius.check_collision(self.igrok):
                                self.apply_force_x(7500)
                                self.s_mimo += 1
                            else:
                                self.s_mimo = 0
                                self.force_x = 0
                                self.mech.ogon_state = True
                                self.s_kombo += 1
                                self.action(self.udar.sposob)
                        elif (not self.kulak_ognya.kd and not self.kulak_ognya.action
                              and self.s_kombo == 1 and self.mech_s_popal == self.kombo_mech2 and not self.mech.action):
                            self.s_kombo = self.mech_s_popal = 0
                            self.action(self.kulak_ognya.sposob)
                            self.mech.timer_for_s_kd = 25
                            self.s_mimo += 1

                        if self.s_mimo >= 60:
                            self.mech_s_popal = self.s_kombo = self.mech.s_popal = 0
                            self.force_x = 0
                            self.mech.timer_for_s_kd = 50
                            self.mech.ogon_state = True
                    if self.mech.s_popal == 0:
                        self.povedenie = 0
                        self.mech_s_popal = self.s_kombo = self.force_x = self.s_mimo = 0
                        self.mech.ogon_state = False
                        self.mech.timer_for_s_kd = 50
                case 2:
                    if self.otstup:
                        self.otstuplenie()
                    else:
                        self.force_x = 0
                        if self.s_kombo == 0 and not self.kulak_ognya.kd and not self.kulak_ognya.action:
                            self.action(self.kulak_ognya.sposob)
                            self.s_kombo += 1
                            self.mech.ogon_state = True
                        elif self.s_kombo == 1:
                            if self.kulak_ognya.kast:
                                self.force_x = 0
                            else:
                                if ((rasst_block > self.d_zone * 1.5 and self.igrok.block.block) or
                                        (rasst > self.d_zone * 1.5 and not self.igrok.block.block)):
                                    self.apply_force_x(10000)
                                    self.beg = True
                                    self.action(self.mech.sposob)
                                    self.mech.s = 2
                                else:
                                    self.beg = False
                                    self.s_kombo = 0
                                    self.povedenie = 0
                case 3:
                    if self.oglush:
                        self.block.block = False
                        self.s_kombo = 0
                    else:
                        if not self.block.block and self.s_kombo == 0:
                            self.s_kombo = 1
                            self.block.block = True
                        if self.popad and self.block.block:
                            self.s_block = 0

                        if self.block.block:
                            self.s_block += 1
                            if self.s_block >= self.timer_for_s_block:
                                self.s_block = 0
                                self.block.block = False
                        if ((not self.block.block or (rasst <= self.d_zone * 2 or (rasst_block <= self.d_zone * 2
                             and self.igrok.block.block))) and not self.kulak_ognya.kd and not self.kulak_ognya.action):
                            self.block.block = False
                            self.action(self.kulak_ognya.sposob)
                            self.apply_force_x(0)
                            self.s_kombo = 2

                    if self.s_kombo == 2 and not self.kulak_ognya.action:
                        self.povedenie = 0
                        self.s_kombo = 0
                case 4:
                    if self.otstup:
                        self.otstuplenie()
                    else:
                        if ((self.s_kombo == 0 or self.s_kombo == 2) and not self.kulak_ognya.kd
                                and not self.kulak_ognya.action):
                            self.action(self.kulak_ognya.sposob)
                            self.s_kombo += 1
                        elif not self.kulak_ognya.kast:
                            if self.s_kombo == 1 or self.s_kombo == 3:
                                self.block.block = True
                                self.pymunk.max_horizontal_velocity = 200
                                if rasst < 300 or (rasst_block < 300 and self.igrok.block.block):
                                    if not self.kulak_ognya.kd and not self.kulak_ognya.action:
                                        self.action(self.kulak_ognya.sposob)
                                        self.s_kombo += 1
                                        if self.s_kombo == 4:
                                            self.mech.ogon_state = True
                                            self.block.block = False
                                            self.pymunk.max_horizontal_velocity = self.walk_vel_x
                                    if not self.kulak_ognya.kast and self.s_kombo == 2:
                                        self.otstup = True
                            if self.s_kombo > 3 and (rasst < self.d_zone * 2 or rasst_block < self.d_zone * 2 and self.igrok.block.block) \
                                    and not self.mech.kd and not self.mech.action:
                                self.mech_s_popal += 1
                                self.action(self.mech.sposob)

                            if self.mech_s_popal >= 2:
                                self.mech_s_popal = self.mech.s_popal = self.s_kombo = 0
                                self.mech.ogon_state = False
                                self.otstup = True
                case 5:
                    if rasst < 800:
                        self.beg = True
                        self.apply_force_x(-10000)
                    else:
                        self.force_x = 0
                        self.beg = False
                        if abs(self.fizika.dx) <= X_D_ZONE and not self.fire_ball.kd and not self.fire_ball.action:
                            self.action(self.fire_ball.sposob)
                        if not self.fire_ball.kast and self.fire_ball.action:
                            self.povedenie = 0
                case 6:
                    if self.otstup:
                        self.otstuplenie()
                    else:
                        self.not_ii = True
                        if self.polet_storona == 0:
                            if self.center_x > self.igrok.center_x:
                                self.storona = 1
                                if rasst > 300:
                                    self.p = 1

                            if self.center_x < self.igrok.center_x and self.p == 0:
                                self.force_x = 5000
                            elif self.center_x > self.igrok.center_x and self.p == 1:
                                if self.polet.action:
                                    self.force_x = -3000
                                else:
                                    self.force_x = 0
                        elif self.polet_storona == 1:
                            if self.center_x < self.igrok.center_x:
                                self.storona = 0
                                if rasst > 300:
                                    self.p = 1

                            if self.center_x > self.igrok.center_x and self.p == 0:
                                self.force_x = -5000
                            elif self.center_x < self.igrok.center_x and self.p == 1:
                                if self.polet.action:
                                    self.force_x = 3000
                                else:
                                    self.force_x = 0

                        if not self.polet.action and not self.polet.kd and self.s_polet == 0:
                            self.s_polet = 1
                            self.action(self.polet.sposob)

                        if self.s_polet == 1 and self.fizika.is_on_ground and not self.polet.action:
                            self.s_polet = self.povedenie = 0
                            self.force_x = 0
                            self.otstup_rasst = 500
                            self.p = 0
                            self.not_ii = False
        else:
            if self.povedenie == 3:
                self.block.block = False
                self.s_kombo = 0
            elif self.povedenie == 6:
                self.not_ii = False
                self.otstup_rasst = 500
                self.povedenie = 0
                self.otstup = False
                self.s_kombo = 0

        if self.not_ii and self.povedenie != 6:
            self.not_ii = False

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.draw_sposob_list()

        self.draw_hit_box(self.color_hit_box)

    def otstuplenie(self):
        def konec():
            self.force_x = 0
            self.pymunk.max_horizontal_velocity = self.walk_vel_x
            if abs(self.fizika.dx) < X_D_ZONE:
                self.otstup = False
                self.block.block = False
                self.s_otstup = 0

        self.s_otstup += 1
        if self.s_otstup >= self.timer_for_s_otstup:
            konec()
            return
        elif abs(self.center_x - self.igrok.center_x) < self.otstup_rasst:
            self.pymunk.max_horizontal_velocity = 200
            if not self.oglush:
                self.block.block = True
            self.apply_force_x(-3000)
        elif abs(self.center_x - self.igrok.center_x) >= self.otstup_rasst:
            konec()

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        super().draw(pixelated=pixelated)


class First(mobs.Vrag):
    def __init__(self, igrok: battles.BattlePers, name: str, walls_list: arcade.SpriteList):
        super().__init__(igrok, name, walls_list)
        self.max_hp = 2000
        self.max_mana = 150
        self.max_stamina = 200
        self.harakteristiki()

        self.scale = 1.5

        self.reakciya = 60
        self.vel_x = self.walk_vel_x = B_VEL_X
        self.beg_vel_x = self.vel_x * 2

        self.animations = spec_plus_animations.FirstAnimations(self)

        self.fire_ball = ogon.FireBall(self, self.sprite_list)
        self.fire_ball.timer_for_s_kd = 300
        self.sposob_list.append(self.fire_ball)

        self.poiman = False

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.fizika.update(physics_engine, dx, dy)
        self._battle_update_storona(dx, X_D_ZONE)

        self.animations.tipo_return = False

        self.animations.poiman_udaren_animation()
        if self.animations.tipo_return:
            return

        self.animations.poiman_animation()
        if self.animations.tipo_return:
            return

        self.animations.ataka_animations()
        if self.animations.tipo_return:
            return

        self.animations.jump_and_fall_animation(dx, self.fizika.is_on_ground, Y_D_ZONE)
        if self.animations.tipo_return:
            return
        self.animations.base_animations(dx, X_D_ZONE, self.fizika.x_odometr, 1)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if self.poiman:
            self.position = self.igrok.center_x + 200, self.igrok.center_y + 40
            # if (self.center_x - self.igrok.center_x) >= 200:
            #     self.position = self.igrok.center_x + 200, self.igrok.center_y + 40
            # elif (self.igrok.center_x - self.center_x) >= 200:
            #     self.position = self.igrok.center_x - 200, self.igrok.center_y + 40




    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.animations.poiman_animation()


    # def poiman_func(self):
    #     if self.poiman:
