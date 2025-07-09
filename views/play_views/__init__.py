import csv
import math
import os
import random

import arcade
import pymunk

import instruments
import texts
from interaction_sprites import battles

from interaction_sprites.battles import igrok
from my_gui import line, circles
from views import menu_views


GRAVITY = (0, -1500)
DAMPING = 0.9
IGROK_MOVE_GROUND = 6000
MASS_IGROK = 1
FRICTION_IGROK = 0.6
IG_MAX_VERTICAL_SPEED = 10000
IG_MAX_HORIZANTAL_SPEED = 300
IG_BEG_SPEED = IG_MAX_HORIZANTAL_SPEED * 3
IGROK_JUMP_FORCE = 40000

CIRCLES_RADIUS = 50

HOD_SPEED = 16


def sprite_list_on_draw(sprite_list: arcade.SpriteList):
    for sprite in sprite_list:
        sprite.draw(pixelated=True)
        sprite.update_animation()


class LevelView(arcade.View):
    VRAG_CT = 'vrag'
    VOD_MARIONETKA_CT = 'vod_marionetka'
    IGROK_CT = 'igrok'
    WALL_FRICTION = 0.9

    def __init__(self, position_slovar, new_game):
        super().__init__()
        self.show = False

        self.position_slovar = position_slovar
        self.new_game = new_game

        self.window.set_mouse_visible(False)

        self.walls_list = arcade.SpriteList()

        self.drug_list = arcade.SpriteList()
        self.vrag_list = arcade.SpriteList()
        self.zhivie_vrag_list = arcade.SpriteList()
        self.v_drug_list = arcade.SpriteList()
        self.smert_list1 = arcade.SpriteList()
        self.smert_list2 = arcade.SpriteList()

        self.igrok = igrok.Oyuun(self.vrag_list, self.walls_list)

        self.fizika = arcade.PymunkPhysicsEngine(GRAVITY, DAMPING)
        def begin_handler_vrags(sprite_a, sprite_b, arbiter, space, data):
            physics_object_a = self.fizika.sprites[sprite_a]
            physics_object_b = self.fizika.sprites[sprite_b]
            if physics_object_a.shape.collision_type == physics_object_b.shape.collision_type == 0:
                return False
            else:
                return True

        def begin_handler_vod_mari(sprite_a, sprite_b, arbiter, space, data):
            physics_object_a = self.fizika.sprites[sprite_a]
            physics_object_b = self.fizika.sprites[sprite_b]
            if physics_object_a.shape.collision_type == physics_object_b.shape.collision_type == 1:
                return False
            else:
                return True

        def begin_handler_vod_mari_and_oyuun(sprite_a, sprite_b, arbiter, space, data):
            physics_object_a = self.fizika.sprites[sprite_a]
            physics_object_b = self.fizika.sprites[sprite_b]
            if physics_object_a.shape.collision_type == 2 and physics_object_b.shape.collision_type == 1:
                return False
            else:
                return True

        self.fizika.add_collision_handler(self.VRAG_CT, self.VRAG_CT, begin_handler_vrags)
        self.fizika.add_collision_handler(self.VOD_MARIONETKA_CT, self.VOD_MARIONETKA_CT, begin_handler_vod_mari)
        self.fizika.add_collision_handler(self.IGROK_CT, self.VOD_MARIONETKA_CT, begin_handler_vod_mari_and_oyuun)

        self.kamera = arcade.Camera()
        self.kamera_koef_x = 2
        self.kamera_koef_y = 5
        self.kamera_dvizh = True
        self.kamera_dvizh_x = 0
        self.kamera_dvizh_y = 0
        self.kamera_otnos_x = 0
        self.kamera_otnos_y = 0
        self.ekran_center = (0, 0)
        self.zoom_minus = False
        self.zoom_plus = False
        self.s_zoom = 0
        self.timer_for_s_zoom = 180
        self.v_zoom = 1 / 150

        self.dialog = texts.Dialogs({}, self.window, self.kamera)

        self.x = 0
        self.y = 0

        self.line_list = line.LineList()
        line_hp = line.Line(self.igrok.max_hp, self.window.width * 0.0125, self.window.width * 0.175,
                            self.window.height * 17 / 18, self.kamera)
        line_hp.name = 'hp'
        self.line_list.append(line_hp)
        colors_v = {0: (0, 200, 255, 255), 1: (0, 200, 255, 255), 2: (0, 200, 255, 255), 3: (0, 200, 255, 255),
                    4: (0, 200, 255, 255)}
        line_v = line.Line(self.igrok.v_max, self.window.width * 0.0125, self.window.width * 0.10625,
                           self.window.height * 23 / 30, self.kamera, 40, colors_v)
        line_v.name = 'voda'
        self.line_list.append(line_v)

        self.circles = circles.Circles(CIRCLES_RADIUS)
        circles_texture = instruments.TextureList()
        circles_texture.load_textures(5, 'resources/sposob', instruments.PNG, False)
        self.circles.create_circles(self.igrok.five_sposobs, self.window.width * 0.2625, self.window.height * 1 / 12,
                                    self.window.width * 0.09375, circles_texture)

        self.levo = False
        self.pravo = False

        self.kast_scena = False
        self.list_kast_scen: list[bool::] = []
        self.s_kast_scena: int = 0
        self.s_ks = 0

        self.fight = False
        self.state_list = []

        self.s_interaction = 0
        self.interaction_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        self.prover_vrag_y = 0
        self.s_voln = 0

        self.s_right = 0
        self.s_left = 0
        self.s_r = 0
        self.s_l = 0
        self.timer_for_s = 20

        self.save = True

        self.stop_x = 0

    def setup(self):
        self.fizika.add_sprite(self.igrok, MASS_IGROK, FRICTION_IGROK, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                               max_horizontal_velocity=IG_MAX_HORIZANTAL_SPEED, moment_of_inertia=self.fizika.MOMENT_INF,
                               damping=0.9, collision_type=self.IGROK_CT)

    def dop_func(self, ekran_center_x: float, ekran_center_y: float):
        return (ekran_center_x, ekran_center_y)

    def center_kamera_za_igrok(self):
        if 1 < self.kamera.zoom <= 2:
            ekran_center_x = ((self.igrok.center_x - self.kamera.viewport_width * self.kamera.zoom / self.kamera_koef_x)
                              - self.kamera_otnos_x)
            ekran_center_y = (self.igrok.center_y - (self.kamera.viewport_height / self.kamera_koef_y) *
                              self.kamera.zoom + self.kamera_otnos_y)
        else:
            ekran_center_x = self.igrok.center_x - self.kamera.viewport_width * self.kamera.zoom / self.kamera_koef_x
            ekran_center_y = (self.igrok.center_y - self.kamera.viewport_height * self.kamera.zoom / self.kamera_koef_y
                              - (self.kamera.viewport_width - self.kamera.viewport_width * self.kamera.zoom) / self.kamera_koef_y )

        if self.kamera_dvizh:
            self.kamera.move_to(self.dop_func(ekran_center_x, ekran_center_y), 0.1)
            self.x, self.y = self.kamera.position

        self.ekran_center = self.dop_func(ekran_center_x, ekran_center_y)

    def zoom(self):
        if self.zoom_minus and not self.zoom_plus:
            self.s_zoom += 1
            # if self.s_zoom > self.timer_for_s_zoom:
            if self.kamera.zoom >= 2:
                self.s_zoom = 0
                self.zoom_minus = False
                self.kamera.zoom = 2
            if self.s_zoom > self.timer_for_s_zoom:
                self.s_zoom = 0
                self.zoom_minus = False
            else:
                self.kamera.zoom += self.v_zoom
        if self.zoom_plus and not self.zoom_minus:
            self.s_zoom += 1
            if self.s_zoom > self.timer_for_s_zoom:
                self.s_zoom = 0
                self.zoom_plus = False
            else:
                self.kamera.zoom -= self.v_zoom

    def filling_vrag_lists(self):
        for vrag in self.vrag_list:
            self.zhivie_vrag_list.append(vrag)
            for drug in self.vrag_list:
                if vrag != drug:
                    vrag.append_drug(drug)

        self.igrok.sprite_list = self.vrag_list

        for vrag in self.zhivie_vrag_list:
            self.fizika.add_sprite(vrag, 1, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=300,
                                   moment_of_inertia=self.fizika.MOMENT_INF, damping=0.9, collision_type=self.VRAG_CT)

    def create_walls(self, start_x: int, end_x: int, interval_x: int, start_y: int, end_y: int, interval_y: int,
                     wall_texture: int or str | bytes | os.PathLike[str] | os.PathLike[bytes]):
        for x in range(start_x, end_x, interval_x):
            for y in range(start_y, end_y, interval_y):
                wall = arcade.Sprite(wall_texture)
                wall.position = x, y
                self.walls_list.append(wall)

    def update_igrok_pos(self, pos):
        self.igrok.position = pos

        with open('files/positions.csv', newline='') as file_position:
            reader = csv.DictReader(file_position, delimiter=';')
            for row in reader:
                if row['pers'] == self.igrok.name:
                    self.igrok.storona = int(row['storona'])

    def sprite_list_draw(self):
        sprite_list_on_draw(self.background_list)
        sprite_list_on_draw(self.interaction_list)
        self.smert_list1.draw()
        sprite_list_on_draw(self.zhivie_vrag_list)

    def lcd_draw(self):
        """
        Lines, circles and dialog draw
        """
        if self.fight and not self.kast_scena:
            self.line_list.draw()
            self.circles.draw(self.x, self.y)

        self.dialog.draw(self.x, self.y)

    def walk_update(self):
        if self.levo or self.pravo:
            self.igrok.walk = True if abs(self.igrok.fizika.dy) < battles.Y_D_ZONE and not self.igrok.fizika.in_air \
                else False

    def update_inter_back(self):
        for interaction in self.interaction_list:
            interaction.update()
        for background in self.background_list:
            background.update()

    def lines_and_circles_update(self, znach_slovar: dict):
        if self.fight:
            self.line_list.update(self.x, self.y, znach_slovar)
            self.circles.update()

    def update_vrag_list(self):
        for vrag in self.zhivie_vrag_list:
            if vrag.smert:
                if random.randint(0, 1) == 1:
                    self.smert_list1.append(vrag)
                else:
                    self.smert_list2.append(vrag)
                self.zhivie_vrag_list.remove(vrag)
                self.v_drug_list.remove(vrag)
                self.fizika.remove_sprite(vrag)
                vrag.smert_func()
            else:
                vrag.on_update()
                x = vrag.return_force('x')
                y = vrag.return_force('y')

                if y > 0:
                    self.prover_vrag_y += 1
                if self.prover_vrag_y > 2 and not vrag.is_on_ground:
                    y = 0

                force = (x, y)
                friction = 0.7
                if vrag.dvizh:
                    force = (vrag.new_force[0] + x, vrag.new_force[1] + y)
                    self.move_sprite(vrag, 0.2 / 60, force, friction)
                else:
                    vrag.vel_x = vrag.pymunk.max_horizontal_velocity
                    if abs(x) > 0:
                        self.move_sprite(vrag, 0.2 / 60, force, friction)
                    elif y > 0:
                        self.move_sprite(vrag, 0.2 / 60, force, friction)
                    else:
                        self.fizika.set_friction(vrag, 1)

                if y == 0 and self.prover_vrag_y >= 2:
                    self.prover_vrag_y = 0

    def update_move_igrok(self, gran_levo, gran_pravo):
        if not self.igrok.stan_for_sposob:
            friction = FRICTION_IGROK
            if not self.igrok.toggle:
                if self.pravo and not self.levo:
                    if self.igrok.center_x >= gran_pravo:
                        self.fizika.set_friction(self.igrok, 1)
                    else:
                        if not self.igrok.fight:
                            self.move_sprite(self.igrok, 0.2 / 60, (IGROK_MOVE_GROUND, 0), friction)
                    self.igrok.storona = 0
                elif not self.pravo and self.levo:
                    if self.igrok.center_x <= gran_levo:
                        self.fizika.set_friction(self.igrok, 1)
                    else:
                        if not self.igrok.fight:
                            self.move_sprite(self.igrok, 0.2 / 60, (-IGROK_MOVE_GROUND, 0), friction)
                    self.igrok.storona = 1
                else:
                    # self.igrok.fight = True
                    self.fizika.set_friction(self.igrok, 1)
            else:
                #print(1)
                # self.igrok.fight = False
                if self.pravo and not self.levo:
                    self.igrok.techenie.hod(HOD_SPEED, self.walls_list)
                elif not self.pravo and self.levo:
                    self.igrok.techenie.hod(-HOD_SPEED, self.walls_list)
                else:
                    self.igrok.techenie.hod(0, self.walls_list)

    def press_escape(self, symbol: int):
        if symbol == arcade.key.ESCAPE:
            self.igrok.beg = False
            self.igrok.pymunk.max_horizontal_velocity = IG_MAX_HORIZANTAL_SPEED
            self.levo = self.pravo = False
            self.window.background_color = arcade.csscolor.GRAY
            self.window.set_mouse_visible()
            self.window.pause_view.settings_manager.new_values(menu_views.Value_Zvuk_Effekt, menu_views.Value_Music,
                                                               menu_views.Complexity)
            self.show = False
            self.window.pause_view.show = True
            self.window.show_view(self.window.pause_view)

    def press_wad(self, symbol: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.pravo = True
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.levo = True

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            if (self.igrok.fizika.is_on_ground and not self.igrok.stan_for_sposob and not self.igrok.fight
                    and not self.igrok.toggle):  # self.igrok.is_on_ground and
                self.igrok.walk = False
                if not self.igrok.dvizh:
                    force = (0, IGROK_JUMP_FORCE)
                else:
                    force = (0, IGROK_JUMP_FORCE + self.igrok.new_force[1])
                self.fizika.apply_force(self.igrok, force)

    def press_lshift(self, symbol: int):
        if symbol == arcade.key.LSHIFT:
            self.igrok.walk = False
            self.igrok.beg = True
            self.igrok.pymunk.max_horizontal_velocity = IG_BEG_SPEED

    def press_sposob(self, symbol: int, key: int, sposob: int):
        if symbol == key:
            self.igrok.action(sposob)

    def release_lshift(self, _symbol: int):
        if _symbol == arcade.key.LSHIFT:
            self.igrok.beg = False
            self.igrok.pymunk.max_horizontal_velocity = IG_MAX_HORIZANTAL_SPEED

    def release_ad(self, _symbol: int):
        if _symbol == arcade.key.D or _symbol == arcade.key.RIGHT:
            self.igrok.walk = self.pravo = False
        elif _symbol == arcade.key.A or _symbol == arcade.key.LEFT:
            self.igrok.walk = self.levo = False

    def polukrug(self, sprite, vektor):
        angle_rad = math.radians(45)
        force_x = math.cos(angle_rad) * 70000 * vektor
        force_y = math.sin(angle_rad) * 70000
        self.fizika.apply_force(sprite, (force_x, force_y))

    def volna(self, kol_vo: int, personazh, start, end, const, tip=0, hp=-1, xy=True):
        vrag_list = arcade.SpriteList()

        prom = abs(abs(start) - abs(end)) // kol_vo
        for i in range(start, end, prom):
            vrag = personazh(self.igrok, arcade.SpriteList(), self.v_drug_list, self.walls_list, tip)
            if xy:
                vrag.position = i, const
            else:
                vrag.position = const, i
            if hp > -1:
                vrag.hp = vrag.max_hp = hp
            vrag_list.append(vrag)

        for vrag in vrag_list:
            self.vrag_list.append(vrag)
            self.zhivie_vrag_list.append(vrag)
            self.v_drug_list.append(vrag)
            self.fizika.add_sprite(vrag, 1, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=300,
                                   moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)

        for vrag in self.vrag_list:
            vrag.v_drug_list = self.v_drug_list
            vrag.fizika = self.fizika

        self.igrok.sprite_list = self.vrag_list

    def double_click_right(self):
        if self.s_right == 1:
            self.s_r += 1
        if self.s_r >= self.timer_for_s:
            self.s_r = 0
            self.s_right = 0

    def double_click_left(self):
        if self.s_left == 1:
            self.s_l += 1
        if self.s_l >= self.timer_for_s:
            self.s_l = 0
            self.s_left = 0

    def move_sprite(self, sprite, minus_stamina, force, friction):
        force, friction = sprite.oglush_force(force, friction, 2)
        # force, friction = sprite.slabweak_func(force, friction)
        self.fizika.apply_force(sprite, force)
        self.fizika.set_friction(sprite, friction)
        # sprite.stamina -= minus_stamina

    def update_kast_scena(self):
        if self.kast_scena and not self.igrok.kast_scena:
            self.igrok.kast_scena = True
            for vrag in self.vrag_list:
                vrag.kast_scena = True
        elif not self.kast_scena and self.igrok.kast_scena:
            self.igrok.kast_scena = False
            for vrag in self.vrag_list:
                vrag.kast_scena = False

    def izmen_poly(self, sprite):
        physics_object = self.fizika.sprites[sprite]
        poly = sprite.hit_box.points
        scaled_poly = [[x * sprite.scale for x in z] for z in poly]
        shape = pymunk.Poly(physics_object.body, scaled_poly, radius=0)
        shape.friction = physics_object.shape.friction
        shape.elasticity = physics_object.shape.elasticity
        shape.collision_type = physics_object.shape.collision_type
        new_physics_object = arcade.PymunkPhysicsObject(physics_object.body, shape)
        self.fizika.sprites[sprite] = new_physics_object
        self.fizika.space.remove(physics_object.shape)
        self.fizika.space.add(shape)
