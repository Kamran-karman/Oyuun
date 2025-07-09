import animations.pers_animations
import hit_box_and_radius
import sposobs
from interaction_sprites import battles
from interaction_sprites.battles import effect_update
from animations.pers_animations import spec_base_animations
import arcade
import copy


X_D_ZONE = 0.005
Y_D_ZONE = 3


class Rock(battles.BattleSprite):
    def __init__(self, walls_list: arcade.SpriteList):
        super().__init__('Rock', walls_list)
        self.max_hp = self.hp = 6100
        self.scale = 2

        self.animations = spec_base_animations.RockAnimations(self)

        self.angle = 0
        self.rotation = False

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:

        # if self.s_tresk < 1:
        #     self.rotation = False
        # else:
        #     self.rotation = True
        self.animations.tresk_animation()
        # if self.rotation:
        #     self.angle = 90
        #     #self.center_y = 160
        # else:
        #     self.angle = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self._update_hp()


class Mob(battles.BattlePers):
    def __init__(self, name, sprite_list, walls_list):
        super().__init__(name, sprite_list, walls_list)
        self.klass = 0

        self.force_x = 0
        self.force_y = 0

        self.beg_vel_x = 0
        self.walk_vel_x = 0

        self.radius_list = arcade.SpriteList()
        self.radius_list.append(self.kvadrat_radius)
        self.radius_vid = hit_box_and_radius.Radius(self, 5)
        self.radius_list.append(self.radius_vid)
        self.radius_action = hit_box_and_radius.Radius(self, 0.25)
        self.radius_list.append(self.radius_action)
        self.drug_list = arcade.SpriteList()
        self.perem = 0

        self.walls_list = walls_list

        self.go = True
        self.d_zone = 75

        self.udar.sprite_list = self.sprite_list

    def update_radius_list(self):
        for radius in self.radius_list:
            radius.position = self.position
        self.kvadrat_radius.scale = self.scale

    def append_drug(self, drug):
        if drug != self:
            self.drug_list.append(drug)
            self.perem = round(len(self.drug_list) )* 0.4 if len(self.drug_list) * 0.4 >= 0.5 else 1

    def update_drug_list(self):
        for drug in self.drug_list:
            if drug.hp < 0:
                self.drug_list.remove(drug)

    def _update_beg(self):
        if not self.dvizh:
            if self.beg:
                if self.pymunk.max_horizontal_velocity != self.beg_vel_x:
                    self.pymunk.max_horizontal_velocity = self.beg_vel_x
            else:
                if self.pymunk.max_horizontal_velocity != self.walk_vel_x:
                    self.pymunk.max_horizontal_velocity = self.walk_vel_x


class Marionetka(Mob, battles.VodaPers):
    def __init__(self, name, sprite_list, walls_list, igrok):
        super().__init__(name, sprite_list, walls_list)
        self.igrok = igrok

        self.v_max = igrok.v_max
        self.v = igrok.v
        self.v_plus = igrok.v_plus

        self.voda_udars = None

        self.__action_list = []

        self.max_hp = 1000
        self.max_mana = igrok.max_mana
        self.max_stamina = igrok.max_stamina
        self.harakteristiki()

        self.vel_x = self.walk_vel_x = 300
        self.beg_vel_x = 600

        self.block = copy.copy(igrok.block)
        self.block.pers = self

        self.idle_texture = arcade.load_texture_pair("resources/Pers_animations/battle/VodMarionetka/idle.png")
        self.texture = self.idle_texture[0]

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.uprav(physics_engine)
        self._battle_update_storona(dx, X_D_ZONE)
        self.fizika.update(physics_engine, dx, dy)
        self.update_sposob_list(physics_engine)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._update_harakteristiki()
        self._update_hp()
        self.kvadrat_radius.update()

        for sposob in self.igrok.five_sposobs:
            if sposob.action and sposob.sposob != sposobs.VOD_MARIONETKA and sposob not in self.__action_list:
                self.action(sposob.sposob)
                self.__action_list.append(sposob)

        for action in self.__action_list:
            if not action.action:
                self.__action_list.remove(action)

        if self.igrok.block.block:
            self.block.block = True
        else:
            self.block.block = False

        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.draw_sposob_list()
        if self.voda_udars:
            self.voda_udars.draw()
        self.texture = self.idle_texture[self.storona]

    def uprav(self, physics_engine: arcade.PymunkPhysicsEngine):
        self.walk = self.igrok.walk
        self.beg = self.igrok.beg
        self._update_beg()
        if self.walk:
            physics_engine.set_friction(self, 0)
            if self.igrok.fizika.dx > X_D_ZONE:
                physics_engine.apply_force(self, (7000, 0))
            elif self.igrok.fizika.dx < -X_D_ZONE:
                physics_engine.apply_force(self, (-7000, 0))
        elif self.beg:
            physics_engine.set_friction(self, 0)
            if self.igrok.fizika.dx > X_D_ZONE:
                physics_engine.apply_force(self, (10000, 0))
            elif self.igrok.fizika.dx < -X_D_ZONE:
                physics_engine.apply_force(self, (-10000, 0))
        if not self.walk and not self.beg or abs(self.igrok.fizika.dx) < X_D_ZONE:
            physics_engine.set_friction(self, 1)


class Vrag(Mob):
    def __init__(self, igrok, name, walls_list):
        super().__init__(name, arcade.SpriteList(), walls_list)
        self.igrok = igrok
        self.sprite_list.append(self.igrok)

        self.ataka = False

        self.not_ii = False

        self.__s_ii = 0

    def ii(self):
        self.update_radius_list()
        self._update_hp()
        self.__s_ii += 1
        if self.__s_ii > 3 and not self.stan_for_sposob and not self.kast_scena:
            self.__s_ii = 0
            if self.center_y > self.igrok.center_y:
                self.center_y += 1
                if arcade.check_for_collision(self.igrok, self):
                    if self.igrok.center_x >= self.center_x:
                        self.force_x = -10000
                    else:
                        self.force_x = 10000
                    self.center_y -= 1
                    return
                self.center_y -= 1
            if self.radius_vid.check_collision(self.igrok) and not self.oglush and not self.not_ii:
                if self.igrok.center_x < self.radius_vid.center_x:
                    if (abs(self.igrok.right - self.left) <= self.d_zone
                            or (abs(self.igrok.block.right - self.left) <= self.d_zone and self.igrok.block.block)):
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                        self.storona = 1
                    else:
                        self.force_x = -15000
                        self.go = True

                        if (self.kvadrat_radius.check_collision(sprite_list=self.sprite_list) and
                                self.fizika.is_on_ground and abs(self.fizika.dx) < X_D_ZONE):
                            for wall in self.walls_list:
                                if self.kvadrat_radius.check_collision(wall):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0
                elif self.igrok.center_x > self.radius_vid.center_x:
                    if (abs(self.right - self.igrok.left) <= self.d_zone
                            or (abs(self.igrok.block.left - self.right) <= self.d_zone and self.igrok.block.block)):
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                        self.storona = 0
                    else:
                        self.force_x = 15000
                        self.go = True

                        if (self.kvadrat_radius.check_collision(sprite_list=self.sprite_list) and
                                self.fizika.is_on_ground and abs(self.fizika.dx) < X_D_ZONE):
                            for wall in self.walls_list:
                                if self.kvadrat_radius.check_collision(wall):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0
                else:
                    self.force_x = 0

                # for drug in self.drug_list:
                #     if (drug.center_x > self.center_x and abs(self.right - drug.left) <= self.d_zone and not drug.go
                #             and self.igrok.center_x > self.center_x):
                #         self.go = False
                #         self.force_x = 0.
                #         break
                #     elif (drug.center_x < self.center_x and abs(self.left - drug.right) <= self.d_zone and not drug.go
                #           and self.igrok.center_x < self.center_x):
                #         self.go = False
                #         self.force_x = 0.
                #         break
            else:
                self.go = False
                self.force_x, self.force_y = 0., 0.

            self.walk = self.go

    def apply_force_x(self, force_x):
        if self.igrok.center_x < self.radius_vid.center_x:
            self.force_x = -force_x
        elif self.igrok.center_x > self.radius_vid.center_x:
            self.force_x = force_x

    def return_force(self, xy: str):
        if not self.fizika.is_on_ground:
            self.force_y = 0
        if xy == 'x':
            return self.force_x
        if xy == 'y':
            return self.force_y
