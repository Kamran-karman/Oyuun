import arcade
import arcade.gui
from pyglet.math import Vec2

import open_files
import instruments
from interaction_sprites import simples
from interaction_sprites.simples import individ_simples
from interaction_sprites.battles.mobs import vrags
import views.play_views
from views.play_views import IGROK_MOVE_GROUND, FRICTION_IGROK, IG_MAX_HORIZANTAL_SPEED, IG_MAX_VERTICAL_SPEED, \
    MASS_IGROK, HOD_SPEED

BACKGROUND_COLOR = (254, 192, 81, 255)

NUMBERS = (1, 2, 3)
SPEAKERS_DIALOG = ('0', '1', '2', '3', '4')

NACH_X = 200


class GlavaFirstView(views.play_views.LevelView):
    def __init__(self, position_slovar, new_game):
        super().__init__(position_slovar, new_game)
        self.show = True

        self.window.set_mouse_visible(False)

        # self.igrok.kast_scena = True
        self.sinhelm = individ_simples.Sinhelm()
        self.interaction_list.append(individ_simples.RinTeo())
        self.bratislav = individ_simples.AdnotBratislav()

        self.vrag_napad = vrags.First(self.igrok, "First", self.walls_list)
        self.dom = arcade.Sprite('resources/dom.png', center_x=NACH_X + 5000, center_y=650)

        self.kast_scena = False
        self.list_kast_scen = [True, False, False]
        self.s_kast_scena = 1
        self.s_ks = 0

        self.kamera_dvizh = False

        self.point_x = 0

        self.kamera_mod = False

    def setup(self):
        self.update_igrok_pos((NACH_X, 163))
        self.center_kamera_za_igrok()
        self.igrok.storona = 1
        self.sinhelm.position = NACH_X - 200, 128
        self.sinhelm.storona = 0
        self.interaction_list[0].position = NACH_X + 2200, 128
        self.interaction_list[0].storona = 1
        self.dialog.create_dialog_slovar(NUMBERS, SPEAKERS_DIALOG, "GlavaFirst")

        self.vrag_napad.position = NACH_X + 4400, 650
        self.vrag_napad.storona = 1
        self.vrag_list.append(self.vrag_napad)

        self.filling_vrag_lists()

        if self.s_kast_scena == 1:
            self.kamera.zoom = 0.65
        else:
            self.kamera.zoom = 0.9

        self.window.background_color = BACKGROUND_COLOR
        self.dialog.manager_dialog.enable()

        self.create_walls(NACH_X - 2000, NACH_X + 10000, 128, 0, 1, 1, 'resources/grassmid.png')
        self.create_walls(NACH_X + 10000, NACH_X + 10001, 1, 0, 385, 128, 'resources/grassmid.png')
        stena = arcade.Sprite("resources/stena.png", center_x=NACH_X + 2650)
        stena.center_y = 64 + stena.height / 2
        self.walls_list.append(stena)
        self.walls_list.append(self.dom)
        krilco = arcade.Sprite('resources/krilco.png', center_x=self.dom.center_x - self.dom.width/2 - 207, center_y=650)
        krilco.center_y = 64 + krilco.height / 2
        self.walls_list.append(krilco)
        krilco.hit_box._points = (
            (-krilco.width/2, -krilco.height/2), (krilco.width/2, -krilco.height/2),
            (krilco.width/2, 518 - krilco.height/2), (-krilco.width/2, 408 - krilco.height/2)
        )
        self.fizika.add_sprite_list(self.walls_list, body_type=self.fizika.STATIC, friction=self.WALL_FRICTION,
                                    collision_type="wall")

    def on_draw(self):
        self.clear()

        self.sprite_list_draw()
        self.drug_list.draw()
        self.drug_list.update_animation()
        self.igrok.draw(pixelated=True)
        if self.s_kast_scena == 1 and self.dialog.dialog:
            self.igrok.animations.idle_animation(0)
        elif self.s_kast_scena == 3:
            self.vrag_napad.draw()
            self.vrag_napad.update_animation()
        self.igrok.update_animation()
        self.sinhelm.draw()
        if self.sinhelm.not_fizik:
            self.sinhelm.update_animation()
        self.smert_list2.draw()
        self.vrag_list.draw()

        self.walls_list.draw()

        self.lcd_draw()

        # arcade.draw_rectangle_filled(2900, 200, 300, 600, arcade.color.BRONZE)

        self.zoom()
        self.kamera.use()

    def on_update(self, delta_time: float):
        self.walk_update()
        # if self.fight and not self.kast_scena:
        self.double_click_left()
        self.double_click_right()

        self.kast_scena_1()
        self.kast_scena_2()

        self.update_kast_scena()

        if self.kamera_dvizh:
            self.center_kamera_za_igrok()

        self.update_inter_back()

        self.lines_and_circles_update({'hp': self.igrok.hp, 'voda': self.igrok.v})

        self.update_vrag_list()
        if not self.kast_scena:
            self.update_move_igrok(NACH_X - 1340, 10000)

        if self.s_kast_scena == 1:
            self.sinhelm.update()
        elif self.s_kast_scena == 2:
            self.vrag_napad.kast_scena = True
            if not self.kast_scena: # and self.igrok.techenie.right > self.dom.left:
                self.fizika.apply_force(self.vrag_napad, (IGROK_MOVE_GROUND, 0))
            if self.igrok.techenie.right > self.dom.right:
                self.list_kast_scen[1] = True
        elif self.s_kast_scena == 3:
            self.vrag_napad.on_update()
            if self.igrok.center_x < NACH_X + 2350:
                self.list_kast_scen[2] = True


        if self.igrok.smert:
            self.window.close()

        self.igrok.on_update()

        self.fizika.step()

    def on_key_press(self, symbol: int, modifiers: int):
        # self.press_escape(symbol)
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

        if symbol == arcade.key.KEY_1:
            self.kast_scena = self.list_kast_scen[0] = self.dialog.dialog = self.dialog.skip = False
            self.kamera_dvizh = self.fight = self.save = self.vrag_napad.beg = True
            self.s_kast_scena = 2
            super().setup()
            self.kamera.zoom = 0.9
            self.fizika.set_position(self.igrok, (2900, 163))
            self.fizika.set_position(self.vrag_napad, (6500, 150))
            self.dialog.clear_text()
            self.dialog.s_dialog = 0

        if symbol == arcade.key.K:
            self.kamera.zoom = 2
            self.kamera_dvizh = self.kamera_mod = True

        if symbol == arcade.key.RIGHT and self.kamera_mod:
            self.kamera.move((self.kamera.position[0] + 100, self.kamera.position[1] + 100))

        if symbol == arcade.key.LEFT and self.kamera_mod:
            self.kamera.move((self.kamera.position[0] - 100, self.kamera.position[1] - 100))

        if symbol == (arcade.key.ENTER or arcade.key.NUM_ENTER):
            self.dialog.skip_func()

        if not self.kast_scena:
            self.press_wad(symbol)
            self.press_lshift(symbol)

            if self.fight:
                self.press_sposob(symbol, arcade.key.NUM_2, self.igrok.five_sposobs[3].sposob)

            if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
                self.s_right += 1
                if ((self.igrok.fizika.is_on_ground or self.igrok.toggle) and not self.igrok.block.block
                        and self.s_right >= 2):
                    self.s_r = 0
                    self.s_right = 0
                    self.igrok.fight = False
                    self.igrok.action(self.igrok.techenie.sposob, True)
            elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
                self.s_left += 1
                if ((self.igrok.fizika.is_on_ground or self.igrok.toggle) and not self.igrok.block.block
                        and self.s_left >= 2):
                    self.s_l = 0
                    self.s_left = 0
                    self.igrok.fight = False
                    self.igrok.action(self.igrok.techenie.sposob, True)

                # if (symbol == arcade.key.W or symbol == arcade.key.UP) and self.igrok.toggle:
                #     self.igrok.techenie.vverh_func(self.walls_list, 60)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.release_lshift(_symbol)

        self.release_ad(_symbol)
        # if self.fight and not self.kast_scena:
        if (_symbol == arcade.key.D or _symbol == arcade.key.RIGHT) and self.igrok.toggle:
            self.igrok.action(self.igrok.techenie.sposob, True)
        elif (_symbol == arcade.key.A or _symbol == arcade.key.LEFT) and self.igrok.toggle:
            self.igrok.action(self.igrok.techenie.sposob, True)

    def kast_scena_1(self):
        if self.s_kast_scena == 1 and self.list_kast_scen[0]:
            if self.save:
                self.save = False

                open_files.write_csv_file(r'files/positions.csv', [
                    [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                    [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                    [self.vrag_napad.name, self.vrag_napad.center_x, self.vrag_napad.center_y, self.vrag_napad.storona]
                ], self.window.FIELDNAMES_POSITION)
                open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                open_files.write_file(r'files/states.txt', [self.fight])

            if self.igrok.center_x < self.interaction_list[0].center_x:
                if self.kamera.zoom == 0.65:
                    self.kamera_dvizh = False
                    if not self.kast_scena:
                        ek_x = NACH_X - 700
                        self.kamera.goal_position = Vec2(ek_x, -100)
                        self.x, self.y = self.kamera.goal_position
                        self.kamera.move((ek_x, -100))
                    self.kast_scena = True
                    if len(self.dialog.speakers_list) == 0:
                        self.dialog.speakers_list.append(self.igrok)
                        self.dialog.speakers_list.append(self.sinhelm)
                        self.dialog.dialog = self.dialog.skip = True
                        self.dialog.s_dialog += 1
                    if self.dialog.s_dialog == 17:
                        self.s_ks += 1
                        if self.s_ks > 60:
                            self.s_ks = 0
                            self.dialog.s_dialog += 1
                        # self.dialog.speakers_list.remove(self.sinhelm)
                        # он типа тут должен заменить Синхелма на кучера, но нету кучера
                    elif self.dialog.s_dialog == 18 and self.dialog.dialog:
                        self.dialog.dialog = self.dialog.skip = False
                        self.sinhelm.change_x = 20
                        self.sinhelm.change_y = 10
                    if self.sinhelm.change_x == 20 and self.sinhelm.center_x > 600:
                        super().setup()
                        self.sinhelm.change_x = self.sinhelm.change_y = 0
                        self.sinhelm.position = NACH_X + 1000, 128
                        self.move_sprite(self.igrok, 1/60, (-IGROK_MOVE_GROUND, 0), FRICTION_IGROK)
                    if self.dialog.s_dialog == 18 and self.sinhelm.change_x == 0:
                        if self.igrok.center_x > -400:
                            self.move_sprite(self.igrok, 1/60, (-IGROK_MOVE_GROUND, 0), FRICTION_IGROK)
                        else:
                            self.fizika.set_friction(self.igrok, 1)
                            self.kamera.zoom = 1.25
                            self.center_kamera_za_igrok()
                            ek_x = NACH_X - 1500
                            self.kamera.position = Vec2(ek_x, self.ekran_center[1])
                            self.kamera.move((ek_x, self.ekran_center[1]))
                            self.x, self.y = self.kamera.position
                            self.dialog.s_dialog = 0
                            self.dialog.speakers_list.remove(self.igrok)
                            self.dialog.speakers_list.remove(self.sinhelm)
                    self.dialog.update(1)
                elif self.kamera.zoom == 1.25:
                    self.kamera.move_to((NACH_X + 1300, self.ekran_center[1]), 0.0043)
                    if abs(self.igrok.center_x - self.sinhelm.center_x) >= 1850:
                        self.move_sprite(self.igrok, 1 / 60, (IGROK_MOVE_GROUND, 0), FRICTION_IGROK)
                    self.sinhelm.change_x = 8
                    if abs(self.sinhelm.center_x - self.interaction_list[0].center_x) < 500:
                        self.sinhelm.change_y = 30
                    if abs(self.igrok.center_x - self.interaction_list[0].center_x) < 1200:
                        self.zoom_plus = True
                        self.timer_for_s_zoom = 195
                        self.v_zoom = 7/3900
                elif self.kamera.zoom < 1.25 and self.zoom_plus:
                    self.move_sprite(self.igrok, 1 / 60, (IGROK_MOVE_GROUND, 0), FRICTION_IGROK)
                elif self.kamera.zoom < 1.25 and not self.zoom_plus and not self.dialog.dialog and self.dialog.s_dialog == 0:
                    self.kamera.zoom = 0.9
                    # self.kamera_dvizh = True
                    if abs(self.igrok.center_x - self.interaction_list[0].center_x) < 250:
                        self.kamera_dvizh = True
                        self.fizika.set_friction(self.igrok, 1)
                        self.dialog.dialog = self.dialog.skip = True
                        self.dialog.s_dialog += 1 # --
                        self.dialog.speakers_list.append(self.igrok)
                        self.dialog.speakers_list.append(self.sinhelm)
                elif self.kamera.zoom == 0.9 and self.dialog.s_dialog > 0:
                    if self.dialog.s_dialog == 13:
                        self.dialog.dialog = self.dialog.skip = False
                        self.move_sprite(self.igrok, 1/60, (IGROK_MOVE_GROUND, 0), FRICTION_IGROK)
                    self.dialog.update(2)
            else:
                if self.dialog.s_dialog == 13:
                    self.kamera_koef_x += 1/60
                    self.kamera_koef_y -= 1/120
                    if self.igrok.center_x < NACH_X + 2630:
                        self.move_sprite(self.igrok, 1 / 60, (IGROK_MOVE_GROUND, 0), FRICTION_IGROK)
                        if self.igrok.center_x > NACH_X + 2300:
                            self.igrok.action(self.igrok.tayfun.sposob)
                            if NACH_X + 2304 > self.igrok.center_x > NACH_X + 2300:
                                self.fizika.apply_force(self.igrok, (0, 10000))
                    else:
                        self.fizika.set_friction(self.igrok, 1)
                        self.dialog.s_dialog += 1
                        self.dialog.dialog = self.dialog.skip = True
                elif 16 > self.dialog.s_dialog > 13:
                    if self.kamera_koef_x < 10:
                        self.kamera_koef_x += 1/25
                    else:
                        self.kamera_koef_x = 10

                    if self.kamera_koef_y > 1.8:
                        self.kamera_koef_y -= 1/30
                    else:
                        self.kamera_koef_y = 1.8
                elif self.dialog.s_dialog == 16:
                    if self.kamera_dvizh:
                        self.kamera_koef_x = 10
                        self.kamera_koef_y = 1.8
                        self.dialog.skip = False
                        s = self.vrag_napad.center_x - self.igrok.center_x - 400
                        t = (s / self.vrag_napad.fire_ball.change) + self.vrag_napad.fire_ball.timer_for_s_kast
                        n = t / 2 - 3
                        if (not self.vrag_napad.fire_ball.action and len(self.dialog.dialog_slovar[2][self.dialog.s_dialog - 1]) <= n
                                and self.dialog.dialog):
                            self.vrag_napad.action(self.vrag_napad.fire_ball.sposob)
                        if abs(self.igrok.center_x - self.vrag_napad.fire_ball.center_x) < 400:
                            self.igrok.block.block = True
                            self.dialog.dialog = False
                            self.dialog.clear_text()
                            self.fizika.set_position(self.vrag_napad, (NACH_X + 6300, 200))
                        if not self.dialog.dialog and not self.vrag_napad.fire_ball.action:
                            self.kamera_dvizh = False
                    else:
                        if self.igrok.block.block:
                            self.fizika.set_friction(self.igrok, 1)
                            self.kamera.move_to((4000, self.y), 0.1)
                            self.s_ks += 1
                            if self.s_ks >= 70:
                                self.igrok.block.block = False
                                self.s_ks = 0
                                self.kamera_dvizh = True
                                self.kamera_koef_x = 2
                                self.kamera_koef_y = 5
                                self.dialog.s_dialog += 1
                                self.move_sprite(self.igrok, 1/60, (10000, 0), FRICTION_IGROK)
                                self.dialog.dialog = True
                                self.igrok.storona = 0
                elif self.dialog.s_dialog == 17:
                    self.igrok.storona = 0
                    if not self.igrok.fizika.is_on_ground or self.igrok.left < self.dom.right:
                        self.move_sprite(self.igrok, 1 / 60, (10000, 0), FRICTION_IGROK)
                    else:
                        self.vrag_napad.beg = self.vrag_napad.kast_scena = self.kamera_dvizh = self.fight = True
                        self.save = True
                        self.dialog.dialog = False
                        self.dialog.s_dialog = 0
                        self.kast_scena = self.list_kast_scen[0] = False
                        self.s_kast_scena += 1

                        open_files.write_csv_file(r'files/positions.csv', [
                            [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                            [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                            [self.vrag_napad.name, self.vrag_napad.center_x, self.vrag_napad.center_y, self.vrag_napad.storona]
                        ], self.window.FIELDNAMES_POSITION)
                        open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                        open_files.write_file(r'files/states.txt', [self.fight])

                self.dialog.update(2)

    def kast_scena_2(self):
        if self.s_kast_scena == 2 and self.list_kast_scen[1]:
            self.kast_scena = True
            if self.save:
                self.save = False
                self.zoom_minus = True
                self.timer_for_s_zoom = 60
                self.v_zoom = 1/240
                self.kamera_dvizh = False
                # self.kamera_koef_x = 4
                # self.kamera_koef_y = 2
                self.point_x = self.dom.right

                open_files.write_csv_file(r'files/positions.csv', [
                    [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                    [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                    [self.vrag_napad.name, self.vrag_napad.center_x, self.vrag_napad.center_y, self.vrag_napad.storona]
                ], self.window.FIELDNAMES_POSITION)
                open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                open_files.write_file(r'files/states.txt', [self.fight])

            if not self.kamera_dvizh:
                if self.igrok.center_x < self.dom.right + self.window.width / 2:
                    if abs(self.igrok.center_x - self.vrag_napad.center_x) > 800:
                        self.kamera.move_to((self.point_x, 0), 0.02)
                    else:
                        self.kamera.move_to((self.point_x, 0), 0.06)
                else:
                    if abs(self.igrok.center_x - self.vrag_napad.center_x) > 415:
                        self.point_x += HOD_SPEED - 2

                    self.kamera.move_to((self.point_x, 0), 0.09)

                if not self.vrag_napad.animations.ataka and self.igrok.toggle:
                    if abs(self.igrok.center_x - self.vrag_napad.center_x) > 415:
                        self.fizika.apply_force(self.vrag_napad, (IGROK_MOVE_GROUND, 0))
                        self.igrok.action(self.igrok.techenie.sposob)
                        self.igrok.techenie.hod(HOD_SPEED, self.walls_list)
                    else:
                        if abs(self.igrok.center_x - self.vrag_napad.center_x) > 400:
                            self.igrok.techenie.hod(HOD_SPEED, self.walls_list)
                        else:
                            self.igrok.techenie.hod(0, self.walls_list)
                            self.vrag_napad.animations.ataka = True
                        self.fizika.set_friction(self.vrag_napad, 1)
                else:
                    if self.igrok.toggle:
                        self.igrok.action(self.igrok.techenie.sposob, True)

                if not self.vrag_napad.animations.ataka and not self.igrok.toggle:
                    self.vrag_napad.animations.poiman = True
                    self.vrag_napad.storona = 1
                    self.dialog.dialog = self.dialog.skip = True
                    self.dialog.s_dialog += 1
                    self.dialog.speakers_list.append(self.igrok)
                    self.dialog.speakers_list.append(self.sinhelm)
                    self.zoom_plus = self.kamera_dvizh = True
            else:
                if abs(self.igrok.center_x - self.vrag_napad.center_x) > 170:
                    self.move_sprite(self.igrok, 1/60, (IGROK_MOVE_GROUND, 0), FRICTION_IGROK)
                if self.dialog.s_dialog == 4:
                    self.dialog.dialog = self.dialog.skip = False
                    if not self.vrag_napad.animations.poiman_udar:
                        if self.s_ks == 0:
                            self.s_ks += 1
                            if not self.igrok.udar.action:
                                self.igrok.action(self.igrok.udar.sposob)
                        elif self.s_ks == 1 and not self.igrok.udar.action:
                            self.vrag_napad.animations.poiman_udar = True
                        elif self.s_ks == 2:
                            self.s_ks = 0
                            self.dialog.s_dialog += 1
                            self.dialog.dialog = self.dialog.skip = True
                    else:
                        self.s_ks = 2
                elif self.dialog.s_dialog >= 6:
                    self.dialog.s_dialog = 6
                    self.dialog.dialog = self.dialog.skip = False
                    self.fizika.remove_sprite(self.vrag_napad)
                    self.vrag_napad.poiman = True
                    self.vrag_napad.animations.poiman = True
                    self.kast_scena = self.list_kast_scen[1] = False
                    self.s_kast_scena += 1
                    self.save = True
                    self.fight = False
                    self.zhivie_vrag_list.remove(self.vrag_napad)
                    self.vrag_list.remove(self.vrag_napad)

                    open_files.write_csv_file(r'files/positions.csv', [
                        [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                        [self.vrag_napad.name, self.vrag_napad.center_x, self.vrag_napad.center_y,
                         self.vrag_napad.storona]
                    ], self.window.FIELDNAMES_POSITION)
                    open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                    open_files.write_file(r'files/states.txt', [self.fight])

                self.dialog.update(3)

    def kast_scena_3(self):
        if self.s_kast_scena == 3 and self.list_kast_scen[2]:
            self.kast_scena = True

    def dop_func(self, ekran_center_x: float, ekran_center_y: float):
        if ekran_center_x < NACH_X - 1500:
            return NACH_X - 1500, ekran_center_y
        elif 3 > self.s_kast_scena >= 1 and ekran_center_x < 2692:
            if self.s_kast_scena == 1:
                if (self.igrok.center_x >= self.interaction_list[0].center_x
                        and self.dialog.s_dialog >= 16 and self.kamera_dvizh):
                    return NACH_X + 2492, ekran_center_y
                else:
                    return ekran_center_x, ekran_center_y
            else:
                return NACH_X + 2492, ekran_center_y
        else:
            return ekran_center_x, ekran_center_y

