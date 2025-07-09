import os
import sys
import csv

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import arcade
import views.play_views
import arcade.gui
from arcade.gui import UIOnClickEvent
from arcade.gui.widgets import buttons, layout, text
from interaction_sprites import simples
from interaction_sprites.simples import individ_simples
from interaction_sprites.battles import mobs
import sposobs
from pyglet.math import Vec2
import open_files
from my_gui import ui

MASS_ROCK = 50
CENTER_X_ROCK = 14000

BACKGROUND_COLOR = (0, 135, 206, 235)

NUMBERS = (1, 2, 3, 4, 5, 3.1, 3.2)
SPEAKERS_DIALOG = ('0', '1', '2', '3')
NAMES = ('hp', 'mana', 'stamina', 'voda')

TEXT_OBUCH_LIST = []
open_files.read_file('files/TEXTS/texts_obuch.txt', TEXT_OBUCH_LIST)

PISMO_1 = ('\tПривет, Эрдэнэ, моя дорогая жена!\n\n\tТы наверное до сих пор злишься из-за того, что я отправился на военную '
           'миссию, тем самым нарушив своё обещание. Перед отъездом я тебе уже объяснял, почему на эту миссию я должен '
           'был отправиться, хоть и как адмирал не должен был. Повторяться не хочу, да и не об этом пишу тебе это '
           'письмо. К твоему день рождению я точно успеваю, но не к приезду детей и внуков. И про подарок для тебя я '
           'не забыл, ведь я подготовил его ещё до отъезда. Поэтому не будет как в прошлый раз. Всё пройдёт так, как '
           'ты любишь: сначала отметим день рождение в кругу семьи, а потом поздним вечером будем отмечать праздник с '
           'гостями. Я конечно буду спаринговаться с нашими детьми и между ними тоже устрою спарринг. Много времени '
           'это не займёт, сильно гонять их не хочу. Я ещё думаю, как будем отмечать нашу тридцатилетнюю годовщину '
           'свадьбы. Говорят на юго-западе Врапы какая-то банда продвигается к столице. Из-за них сенат скорей всего '
           'решит усилить границы, а это будет значить, что дома буду появляться ещё реже. Надеюсь этого не случиться, '
           'и мы сможем спокойно отметить нашу годовщину.\n\nС любовью, твой дорогой муж, Оюун Окинус.') # open_files
PISMO_2 = ('    Здравствуйте, Ашиль Эбба.\n\n\tЯ со всей радостью приглашаю Вас на празднование дня рождения моей жены, '
           'Эрдэны Окинус. Празднование начнётся в 9 вечера в моём имении. Будет пышное празднование с выступлениями '
           'моих внуков. Приходите, не пожалеете.\n\nС уважением, адмирал флота Оюун Окинус.') # open_files
DOKLAD = ('Адмиралтейству Боековского флота Врапы от Адмирала боековского флота Врапы Оюуна Окинуса.\n\n\tЯ, адмирал '
          'флота Оюун Окинус, докладываю о успешно проводящихся боевых учениях с четвёртой ротой береговой части '
          'боековского флота Врапы. Один день мы потратили на дорогу до реки Разлома, всё остальное время уходит на '
          'учения. Четвёртая рота показывает отличные результаты, а капитан Синхелм Хротгар лишний раз доказал, что '
          'мы не зря его повысили до звания капитана.\n\tБоевые учение проводяться следующим образом: на берегу реки'
          ' стоял флаг, который охранял я. Задача роты: захватить флаг и отнести его в свой штаб, который находится '
          'в полукилометре от берега. Рота действует, как настоящей боевой миссии, поэтому они используют все свои '
          'силы, в том числе и огнестрел. За 4 дней максимальный их рекорд рекорд составил 457 метров, что на 23 метра'
          ' лучше, чем в прошлые боевые учения. Возможно они ещё улучшат свой результат.\n\tБоевые учения будут '
          'проводиться ещё 6 дней, после ещё один день потратиться на дорогу обратно. Полный отчёт по проведённым '
          'боевым учениям я напишу после возвращения в город Понкайобург.\n\nАдмирал флота О. Окинус') # open_files
SECRET_DOP = ('\tНа момент написания дополнения, мы уже почти добрались до города Аарон. К вечеру уже будем в городе.'
              ' По моему плану, мы сначала отцепляем город, затем в него с шести сторон входят 5 небольших отрядов и я.'
              ' Нашей задачей будет загнать бандитов в центр города, окружить их там и предложить им сдаться. Если они'
              ' откажутся, то отряды отцепляют центр, а я буду ловить их. Моё мастерство владении стихией позволит мне'
              ' ловить бандитов с минимальным для них урона. Нам неизвестно точное количество бандитов, но я '
              'предполагаю, что их будет несколько десятков. Поймать всех бандитов в городе я планирую к полуночи.'
              ' Далее на следующий день мы выдвигаемся обратно в Понкайобург, через тюрьму Верхний Разлом, чтобы там'
              ' передать всех бандитов под стражу. Из-за этого путь обратно займёт на два дня больше. на данный момент'
              ' эта секретная миссия идёт по плану. Отправьте гонца обратно на случай, если случится какой-нибудь '
              'форс-мажор, так как в таком случае мне может понадобиться помощь или консультация.') # open_files

DEREVO = 'derevo'


class PrologViev(views.play_views.LevelView):
    def __init__(self, position_slovar, new_game):
        super().__init__(position_slovar, new_game)
        self.window.background_color = BACKGROUND_COLOR

        self.igrok.kast_scena = True
        self.sinhelm = individ_simples.Sinhelm()
        self.rock = mobs.Rock(self.walls_list)
        with open('files/bosses.csv', newline='') as file_bosses:
            reader = csv.reader(file_bosses, delimiter=';')
            for row in reader:
                if self.rock.name == row[0]:
                    self.rock.hp = int(row[1])
        self.bratislav = individ_simples.AdnotBratislav() if self.rock.hp > 0 else None

        self.kamera_dvizh = True # if NEW_GAME else True

        self.dialog.create_dialog_slovar(NUMBERS, SPEAKERS_DIALOG, 'Prolog')

        file_kast_scena = open(r'files/kast_scena.txt')
        self.kast_scena = False if file_kast_scena.readline().replace('\n', '') == self.window.FALSE_STR else True
        self.list_kast_scen = [False, False, False, False, False, False]
        self.s_kast_scena = int(file_kast_scena.readline())
        file_kast_scena.close()
        self.s_ks = 0

        self.perexod = False
        self.perexod_sprite = arcade.Sprite()

        self.manager_buttons = arcade.gui.UIManager()
        self.gird_button = None
        self.manager_text = arcade.gui.UIManager()
        self.text_layout_text = None
        self.text_list = [PISMO_1, PISMO_2, DOKLAD, SECRET_DOP]
        self.read = False
        self.vibor = False
        self.vit = False
        self.manager_obuch = arcade.gui.UIManager()
        self.text_label = None
        self.text_obuch_list = TEXT_OBUCH_LIST
        with open('files/states.txt') as file_state:
            for i in file_state.readline().split():
                if i == self.window.TRUE_STR:
                    self.state_list.append(True)
                else:
                    self.state_list.append(False)
            obuch = file_state.readline()
            fight = file_state.readline()
            udar = file_state.readline()
            self.obuch = False if obuch.replace('\n', '') == self.window.FALSE_STR else True
            self.fight = False if fight.replace('\n', '') == self.window.FALSE_STR else True
            self.udar = False if udar.replace('\n', '') == self.window.FALSE_STR else True

        self.s_state = 0
        self.manager_konec = arcade.gui.UIManager()
        self.text_konec = None

        self.alpha = -120
        self.alpha_bg = 255
        self.s_prolog = 0
        if self.new_game:
            self.prolog = True
        else:
            self.prolog = False

    def setup(self):
        v_box = arcade.gui.UIBoxLayout(space_between=50)

        gird = layout.UIGridLayout(column_count=2, row_count=1, horizontal_spacing=30, vertical_spacing=30)
        vit_button = buttons.UIFlatButton(text='Выйти из игры', width=self.window.width * 25 / 96,
                                          height=self.window.height * 5 / 54, style=ui.BUTTONS_STYLE)
        gird.add(vit_button, 0, 0)
        new_game_button = buttons.UIFlatButton(text='Начать новую игру', width=self.window.width * 25 / 96,
                                               height=self.window.height * 5 / 54, style=ui.BUTTONS_STYLE)
        gird.add(new_game_button, 1, 0)
        v_box.add(gird)

        @new_game_button.event('on_click')
        def on_click_new_game(event):
            self.reset()

        @vit_button.event('on_click')
        def on_click_vit(event):
            self.window.close()

        ui_anchor_layout = layout.UIAnchorLayout()
        ui_anchor_layout.add(v_box, anchor_x='center_x', anchor_y='center_y', align_y=-self.window.height * 1 / 20)
        self.manager_konec.add(ui_anchor_layout)

        with open('files/states.txt') as file_states:
            text_obuch = file_states.readlines()[-1]
        self.text_label = text.UILabel(width=self.window.width * 0.3125, height=self.window.height * 4 / 9,
                                       font_size=20, font_name=ui.FONT_NAME, bold=True, align='center', multiline=True,
                                       text=text_obuch)
        ui_anchor_layout = layout.UIAnchorLayout()
        ui_anchor_layout.add(self.text_label, anchor_x='right', anchor_y='top', align_y=-self.window.height * 1 / 12,
                             align_x=-self.window.width * 0.0625)
        self.manager_obuch.add(ui_anchor_layout)

        ui_anchor_layout = layout.UIAnchorLayout()

        nazad_button = buttons.UIFlatButton(text='Назад', width=self.window.width * 0.15625,
                                            height=self.window.height * 2 / 27, style=ui.BUTTONS_STYLE)
        ui_anchor_layout.add(nazad_button, anchor_x='center_x', anchor_y='bottom', align_y=self.window.height * 1 / 30)
        self.text_layout_text = text.UILabel(font_name=ui.FONT_NAME, font_size=14, text_color=arcade.csscolor.BLACK,
                                             multiline=True, width=self.window.width * 0.39375,
                                             height=self.window.height * 0.77)
        ui_anchor_layout.add(self.text_layout_text, anchor_x='center_x', anchor_y='top',
                             align_x=self.window.width * 0.00625, align_y=-self.window.height * 5 / 90)
        self.manager_text.add(ui_anchor_layout)

        @nazad_button.event('on_click')
        def on_click_nazad(event):
            self.read = False
            self.vibor = True
            self.manager_text.disable()
            self.manager_buttons.enable()

        self.manager_buttons.enable()
        # Дать возможность прочитать не только письмо, но и доклады, отчёты и секретные документы
        self.gird_button = layout.UIGridLayout(column_count=2, row_count=2, horizontal_spacing=30, vertical_spacing=30)
        ui_anchor_layout = layout.UIAnchorLayout()

        viti_button = buttons.UIFlatButton(text='Выйти из палатки', width=self.window.width * 5 / 24,
                                           height=self.window.height * 2 / 27, style=ui.BUTTONS_STYLE)
        buttons_text = ['Письмо жене', 'Письмо гостю', 'Доклад', 'Секретное дополнение']

        class MyButton(buttons.UIFlatButton):
            def __init__(a, i, x: float = 0, y: float = 0, width: float = 100, height: float = 50, text="",
                         multiline=True, size_hint=None, size_hint_min=None, size_hint_max=None, style=None, **kwargs):
                super().__init__(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    size_hint=size_hint,
                    size_hint_min=size_hint_min,
                    size_hint_max=size_hint_max,
                    style=style or a.DEFAULT_STYLE,
                    text=text,
                    multiline=multiline,
                    **kwargs
                )
                a.i = i

            def on_click(a, event: UIOnClickEvent):
                self.read = True
                self.vibor = False
                self.text_layout_text.text = self.text_list[a.i]
                self.manager_buttons.disable()
                self.manager_text.enable()

        i = 0
        row_num = 0
        col_num = 0
        for button_text in buttons_text:
            button = MyButton(i, text=button_text, width=self.window.width * 49 / 384,
                              height=self.window.height * 347 / 1080, style=ui.BUTTONS_STYLE)
            self.gird_button.add(button, col_num=col_num, row_num=row_num)
            if i < 1:
                row_num = 0
            else:
                if row_num == 0:
                    col_num = -1
                row_num = 1

            i += 1
            col_num += 1

        def on_click_viti(event):
            self.read = False
            self.vibor = False
            self.igrok.animations.read = False
            self.vit = True
            self.move_sprite(self.igrok, 0.2 / 60, (views.play_views.IGROK_MOVE_GROUND, 0), 0.6)
            self.manager_buttons.disable()

        viti_button.on_click = on_click_viti

        ui_anchor_layout.add(viti_button, anchor_x='center_x', anchor_y='center_y',
                             align_y=self.window.height * 13 / 36)
        ui_anchor_layout.add(self.gird_button, anchor_x='center_x', anchor_y='center_y',
                             align_y=-self.window.height * 1 / 15)
        self.manager_buttons.add(ui_anchor_layout)

        self.dialog.manager_dialog.enable()

        if self.s_kast_scena == 0:
            self.kamera.zoom = 0.65
        else:
            self.kamera.zoom = 0.9

        self.perexod_sprite.texture = arcade.load_texture('resources/perehod.png')
        self.perexod_sprite.scale = 100
        self.perexod_sprite.position = CENTER_X_ROCK - 18000, 800

        self.rock.position = (CENTER_X_ROCK, -150) if self.s_kast_scena < 5 else self.position_slovar[self.rock.name]
        with open('files/bosses.csv', newline='') as file_bosses:
            reader = csv.reader(file_bosses, delimiter=';')
            for row in reader:
                if self.rock.name == row[0]:
                    self.rock.hp = int(row[1])

        if self.s_kast_scena == 0:
            gonec = individ_simples.Gonec()
            gonec.position = 125, 192
            self.interaction_list.append(gonec)
        if self.rock.hp > 0:
            # self.bratislav = pers.AdnotBratislav(arcade.SpriteList())
            self.bratislav.scale = 1
            self.bratislav.position = (4000, 192) if self.s_kast_scena < 4 else self.position_slovar[self.bratislav.name]

        derevo = simples.ToggleSprite(DEREVO, 'resources/Pers_animations/Derevo.png',
                                      'resources/Pers_animations/Derevo.png')
        derevo.position = CENTER_X_ROCK - 4000, 384
        self.interaction_list.append(derevo)

        voin1 = arcade.Sprite('resources/Pers_animations/base/male_adventurer/maleAdventurer_idle.png',
                              0.8, 3500,
                              179.2)
        self.background_list.append(voin1)
        voin2 = arcade.Sprite('resources/Pers_animations/base/male_adventurer/maleAdventurer_idle.png',
                              1.01, 4500,
                              192.64)
        self.background_list.append(voin2)
        voin3 = arcade.Sprite('resources/Pers_animations/base/male_adventurer/maleAdventurer_idle.png',
                              0.9, 4200, 192)
        self.background_list.append(voin3)

        self.sinhelm.position = (1500, 192) if (2 >= self.s_kast_scena or self.s_kast_scena == 6) \
            else self.position_slovar[self.sinhelm.name]

        self.create_walls(CENTER_X_ROCK + 150, 17000, 128, 0, 1, 1, 'resources/waterTop_low.png')
        self.create_walls(-1000, CENTER_X_ROCK + 150, 128, -128, 1, 128, 'resources/grassmid.png')

        self.update_igrok_pos(self.position_slovar[self.igrok.name])
        self.igrok.fight = False

        # colors_mana = {0: (138, 43, 255, 255), 1: (0, 0, 255, 255), 2: (0, 0, 150, 255), 3: (0, 0, 100, 255),
        #                4: (0, 0, 50, 255)}
        # line_mana = line.Line(self.igrok.max_mana, self.window.width * 0.0125, self.window.width * 0.10625,
        #                            self.window.height * 0.9, self.kamera, 15, colors_mana)
        # line_mana.name = NAMES[1]
        # self.line_list.append(line_mana)
        # colors_stamina = {0: (255, 255, 255, 255), 1: (230, 230, 230, 255), 2: (200, 200, 200, 255),
        #                   3: (150, 150, 150, 255), 4: (100, 100, 100, 255)}
        # line_stamina = line.Line(self.igrok.max_stamina, self.window.width * 0.0125, self.window.width * 0.10625,
        #                               self.window.height * 79/90, self.kamera, 15, colors_stamina)
        # line_stamina.name = NAMES[2]
        # self.line_list.append(line_stamina)

        self.filling_vrag_lists()

        # def begin_handler(sprite_a, sprite_b, arbiter, space, data):
        #     physics_object_a = self.fizika.sprites[sprite_a]
        #     physics_object_b = self.fizika.sprites[sprite_b]
        #     if physics_object_a.shape.collision_type == physics_object_b.shape.collision_type == 0:
        #         return False
        #     else:
        #         return True
        #
        # self.fizika.add_collision_handler(IGROK_CT, IGROK_CT, begin_handler)

        super().setup()

        self.fizika.add_sprite_list(self.walls_list, friction=self.WALL_FRICTION,
                                    body_type=self.fizika.STATIC, collision_type="default")

        self.fizika.add_sprite(self.rock, 1, 1, body_type=self.fizika.STATIC,
                               max_horizontal_velocity=300, max_vertical_velocity=2000,
                               moment_of_inertia=self.fizika.MOMENT_INF)

        if self.s_kast_scena > 2:
            self.sinhelm.not_fizik = False
            self.fizika.add_sprite(self.sinhelm, views.play_views.MASS_IGROK, views.play_views.FRICTION_IGROK,
                                   max_vertical_velocity=views.play_views.IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=views.play_views.IG_MAX_HORIZANTAL_SPEED,
                                   moment_of_inertia=self.fizika.MOMENT_INF, damping=0.9)
            if self.s_kast_scena < 5:
                self.dialog.speakers_slovar = {0: self.igrok, 2: self.sinhelm, 3: self.bratislav}
        if self.s_kast_scena < 2:
            self.dialog.speakers_slovar = {0: self.igrok, 1: self.interaction_list[0], 2: self.sinhelm,
                                           3: self.bratislav}
        elif self.s_kast_scena == 2:
            self.dialog.speakers_slovar = {0: self.igrok, 2: self.sinhelm, 3: self.bratislav}
        elif self.s_kast_scena == 5:
            self.sinhelm.storona = 0
            if self.rock.hp > 0:
                self.dialog.speakers_slovar = {0: self.igrok, 2: self.sinhelm, 3: self.bratislav}
                self.kamera_koef_x = 2
                self.bratislav.change_x = -5
                if not self.state_list[4]:
                    self.text_label.text = self.text_obuch_list[3]
                    self.igrok.stan_for_sposob = True
            else:
                self.sinhelm.pymunk.max_horizontal_velocity = 700
                self.sinhelm.olen_beg = True
                self.dialog.speakers_slovar = {0: self.igrok, 2: self.sinhelm}
            self.fizika.remove_sprite(self.rock)
            self.fizika.add_sprite(self.rock, MASS_ROCK, 1, max_vertical_velocity=5000, max_horizontal_velocity=300,
                                   moment_of_inertia=self.fizika.MOMENT_INF, damping=0.9)
        elif self.s_kast_scena == 6:
            self.sinhelm.storona = 0
            self.text_label.text = self.text_obuch_list[12]
            self.igrok.fight = False
            self.fizika.step()
        elif self.s_kast_scena == 7:
            self.kamera_dvizh = False
            self.alpha = 255
            self.s_prolog = 120

        self.igrok.sprite_list.append(self.rock)
        self.center_kamera_za_igrok()
        if self.new_game:
            self.kamera_dvizh = False

    def reset(self):
        pass

    def on_draw(self):
        self.clear()

        arcade.draw_rectangle_filled(-500, 200, 1000, 650, arcade.color.GOLD)

        self.sprite_list_draw()
        if self.bratislav is not None:
            self.bratislav.draw()
            self.bratislav.update_animation()
        self.igrok.draw(pixelated=True)
        self.igrok.update_animation()
        self.sinhelm.draw()
        if self.sinhelm.not_fizik:
            self.sinhelm.update_animation()
        self.smert_list2.draw()

        self.rock.draw()
        self.rock.update_animation()
        self.walls_list.draw()

        self.lcd_draw()

        if self.list_kast_scen[0]:
            if self.vibor:
                arcade.draw_rectangle_filled(-500, self.window.height * 0.27, self.window.width * 0.1875, self.window.height * 7/18,
                                             (0, 0, 0, 125))
                self.manager_buttons.draw()
            if self.read:
                width = self.window.width * 0.21875
                arcade.draw_rectangle_filled(-500, self.window.height * 5/18, width, width * 99/70, arcade.color.WHITE)
                self.manager_text.draw()

        if self.obuch:
            self.manager_obuch.enable()
            self.manager_obuch.draw()
        else:
            self.manager_obuch.disable()

        if self.s_kast_scena == 7:
            self.window.set_mouse_visible()
            self.manager_konec.enable()
            texture = arcade.load_texture('nuzhno/Aaron.jpg', width=self.window.width, height=self.window.height)
            arcade.draw_scaled_texture_rectangle(self.x + texture.width / 1.9, self.window.height * 25/54, texture)

            if self.alpha < 255:
                self.alpha += 2

            alpha = self.alpha
            if alpha < 0:
                alpha = 0
            elif alpha > 255:
                alpha = 255

            text_konec = arcade.Text('Глава первая: город Аарон', (self.ekran_center[0] + self.window.width *
                                                                   self.kamera.zoom / 2) - self.window.width * 35/96,
                                     (self.ekran_center[1] + self.window.height * self.kamera.zoom / 2) +
                                     self.window.height * 25/108,
                                     font_size=self.window.height * 1/12, font_name=ui.FONT_NAME,
                                     color=(255, 255, 255, alpha), align='center', width=self.window.width * 25/48,
                                     multiline=True, bold=True)
            text_konec.draw()
            if self.alpha >= 255:
                self.s_prolog += 1
                if self.s_prolog >= 120:
                    self.manager_konec.draw()

        if self.perexod:
            self.perexod_sprite.update_animation()

        self.zoom()
        self.kamera.use()

        if self.s_kast_scena == 0:
            if self.prolog:
                if self.s_prolog == 0:
                    self.alpha += 2
            else:
                self.alpha -= 2
            if self.prolog and self.alpha >= 255:
                self.s_prolog += 1
                if self.s_prolog >= 90:
                    self.prolog = False
            elif not self.prolog and self.alpha <= -90:
                self.alpha_bg -= 3
                if self.alpha_bg <= 120:
                    self.igrok.animations.wasu = True
            #self.center_kamera_za_igrok()
            if self.alpha_bg < 0:
                self.list_kast_scen[0] = True
                self.alpha_bg = 0
                self.s_kast_scena += 1
                self.alpha = -240
            arcade.draw_rectangle_filled(self.igrok.center_x + self.window.width / 2,
                                         self.igrok.center_y + self.window.height / 2, self.window.width * 2,
                                         self.window.height * 2, (0, 0, 0, self.alpha_bg))
            alpha = self.alpha
            if alpha < 0:
                alpha = 0
            elif alpha > 255:
                alpha = 255

            text_prolog = arcade.Text('Пролог', (self.ekran_center[0] + self.window.width * self.kamera.zoom / 2.6),
                                      (self.ekran_center[1] + self.window.height * self.kamera.zoom / 2) - 30, font_size=60,
                                      font_name=ui.FONT_NAME, color=(255, 255, 255, alpha), align='center', width=30)
            text_prolog.draw()

    def on_update(self, delta_time: float):
        self.walk_update()

        if self.s_kast_scena == 6:
            self.double_click_right()
            self.double_click_left()

        if self.rock.hp < self.rock.max_hp:
            if not self.state_list[5]:
                self.obuch = False
                self.udar = True
            self.state_list[5] = True

        self.kast_scena_1()
        self.kast_scena_2()
        self.kast_scena_3()
        self.kast_scena_4()
        self.kast_scena_5()
        self.kast_scena_6()

        if self.perexod:
            self.perexod_sprite.change_x = 50
            self.perexod_sprite.update()

        if self.list_kast_scen[1]:
            self.state_list[0] = self.state_list[1] = self.state_list[2] = self.state_list[3] = True
            self.obuch = False

        self.update_kast_scena()

        if self.kamera_dvizh:
            self.center_kamera_za_igrok()

        self.update_inter_back()

        self.lines_and_circles_update({NAMES[0]: self.igrok.hp, NAMES[3]: self.igrok.v})

        if self.igrok.smert:
            self.window.close()

        if not self.kast_scena:
            self.update_vrag_list()
            self.update_move_igrok(-94, CENTER_X_ROCK + 500)
            if (not self.igrok.stan_for_sposob and not self.igrok.toggle and self.igrok.center_x <= CENTER_X_ROCK - 980
                    and self.s_kast_scena == 5 and self.rock.hp > 0):
                self.fizika.set_friction(self.igrok, 1)

        if self.igrok.center_x >= CENTER_X_ROCK + 300:
            self.fizika.set_position(self.igrok, (CENTER_X_ROCK + 300, self.igrok.center_y))
        if self.igrok.center_x <= -94 and self.s_kast_scena > 1:
            self.fizika.set_position(self.igrok, (-94, self.igrok.center_y))
        elif self.igrok.center_x <= CENTER_X_ROCK - 980 and self.s_kast_scena == 5 and self.rock.hp > 0:
            self.fizika.set_position(self.igrok, (CENTER_X_ROCK - 980, self.igrok.center_y))

        if self.s_kast_scena == 5 and not self.list_kast_scen[4] and self.rock.hp <= 0:
            if self.bratislav is not None:
                self.bratislav = None
            self.kamera_dvizh = True
            self.obuch = False
            self.fight = False
            if self.dialog.s_dialog == 0:
                self.dialog.s_dialog += 1
                self.dialog.dialog = True
                self.dialog.skip = True
                self.dialog.speakers_list.append(self.igrok)
                self.dialog.speakers_list.append(self.sinhelm)
            if self.dialog.s_dialog == 2:
                self.dialog.skip = False
                self.dialog.dialog = False
            self.dialog.update(5)

            if self.sinhelm.center_x < 0:
                if self.sinhelm.not_fizik:
                    self.fizika.add_sprite(self.sinhelm, views.play_views.MASS_IGROK, views.play_views.FRICTION_IGROK,
                                           max_vertical_velocity=views.play_views.IG_MAX_VERTICAL_SPEED,
                                           max_horizontal_velocity=views.play_views.IG_MAX_HORIZANTAL_SPEED,
                                           moment_of_inertia=self.fizika.MOMENT_INF, damping=0.9)
                    self.sinhelm.not_fizik = False
                self.fizika.set_position(self.sinhelm, (CENTER_X_ROCK - 11000, 2500))
                self.sinhelm.pymunk.max_horizontal_velocity = 700
                self.sinhelm.olen_beg = True
            if abs(self.sinhelm.center_x - self.igrok.center_x) <= 7500:
                self.list_kast_scen[4] = True
        elif not self.list_kast_scen[3] and self.s_kast_scena == 4:
            if self.igrok.center_x <= CENTER_X_ROCK - 800:
                if self.pravo and self.bratislav.center_x < self.igrok.center_x:
                    if 100 >= abs(self.bratislav.center_x - self.igrok.center_x) >= 50:
                        self.bratislav.change_x = 4
                    elif abs(self.bratislav.center_x - self.igrok.center_x) > 100:
                        self.bratislav.change_x = 5.5
                    else:
                        self.bratislav.change_x = 0
                else:
                    self.bratislav.change_x = 0
                if self.s_interaction == 1:
                    if not self.dialog.dialog:
                        self.dialog.s = 3.1
                        self.dialog.dialog_slovar[self.dialog.s] = self.dialog.DIALOG_SLOVAR[self.dialog.s].copy()
                        self.dialog.dialog = self.dialog.skip = True
                        self.dialog.clear_text()
                        self.dialog.s_dialog = 1
                        if len(self.dialog.speakers_list) == 0:
                            self.dialog.speakers_list.append(self.igrok)
                            self.dialog.speakers_list.append(self.bratislav)
                    self.dialog.update(3.1)
                    if self.dialog.s_dialog == 8:
                        self.dialog.dialog = self.dialog.skip = False
                        self.dialog.clear_text()
                        self.s_interaction = 0
                        self.dialog.s_dialog = 0
                else:
                    if CENTER_X_ROCK - 4000 <= self.igrok.center_x:
                        if not self.dialog.dialog and len(self.dialog.dialog_slovar[3.2][0]) != 102:
                            self.s_ks = 0
                        self.s_ks += 1
                        if self.s_ks >= 1800:
                            if not self.dialog.dialog:
                                if len(self.dialog.speakers_list) == 0:
                                    self.dialog.speakers_list.append(self.igrok)
                                    self.dialog.speakers_list.append(self.bratislav)
                                self.dialog.s_dialog = 1
                                self.dialog.clear_text()
                            self.dialog.dialog = True
                            self.dialog.skip = True
                            self.dialog.update(3.2)
                            if self.dialog.s_dialog == 24:
                                self.dialog.dialog = self.dialog.skip = False
                                self.dialog.s_dialog = 0
                                self.dialog.clear_text()
                                self.s_ks = 0
                        if self.s_interaction == 1:
                            self.s_ks = 0
                            self.dialog.clear_text()
            elif self.igrok.center_x > CENTER_X_ROCK - 800:
                self.igrok.pymunk.max_horizontal_velocity = views.play_views.IG_MAX_HORIZANTAL_SPEED
                self.bratislav.change_x = 0
                self.list_kast_scen[3] = True
        elif self.s_kast_scena == 3 and not self.list_kast_scen[1]:
            if self.sinhelm.center_x < -120:
                self.fizika.set_friction(self.sinhelm, 1)
            else:
                self.fizika.apply_force(self.sinhelm, (-8000, 0))

        self.igrok.on_update()
        if self.state_list[4]:
            if self.state_list[5] and self.udar:
                if self.igrok.udar.action and self.igrok.udar.s == 1:
                    self.s_state += 1
                if self.s_state >= 6:
                    self.s_state = 0
                    self.udar = False
                    self.text_label.text = self.text_obuch_list[5]
                    self.obuch = True
            if not self.state_list[6] and self.state_list[5] and not self.udar:
                if self.igrok.udar.action and self.igrok.udar.s == 1:
                    self.s_state += 1
                if self.s_state >= 6:
                    self.s_state = 0
                    self.state_list[6] = True
                    self.text_label.text = self.text_obuch_list[6]
        else:
            if self.igrok.udar.action and self.igrok.udar.s == 1:
                self.s_state += 1
            if self.s_state >= 4:
                self.s_state = 0
                self.state_list[4] = True
                self.text_label.text = self.text_obuch_list[4]
                self.igrok.stan_for_sposob = False

        self.fizika.step()
        if self.bratislav is not None:
            self.bratislav.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.F:
            self.fight = True
            self.udar = False
            for i in range(len(self.state_list)):
                self.state_list[i] = True

        if symbol == arcade.key.E:
            for interaction in self.interaction_list:
                if arcade.check_for_collision(interaction, self.igrok):
                    if interaction.name == DEREVO:
                        self.s_interaction = 1

        if symbol == arcade.key.KEY_0:
            self.rock.hp -= 10000

        self.press_escape(symbol)

        if symbol == (arcade.key.ENTER or arcade.key.NUM_ENTER):
            self.dialog.skip_func()

            if not self.igrok.block.block and self.fight and not self.kast_scena and self.state_list[10]:
                self.igrok.action(self.igrok.five_sposobs[1].sposob)
                if not self.state_list[11]:
                    self.state_list[11] = True
                    self.text_label.text = self.text_obuch_list[11]

        if symbol == arcade.key.K:
            self.kast_scena = not self.kast_scena

        if symbol == arcade.key.T:
            x = 0
            y = 0
            for sprite in self.zhivie_vrag_list:
                x = sprite.center_x
                y = sprite.center_y
            x += 100
            y += 100
            self.fizika.set_position(self.igrok, (x, y))

        if not self.kast_scena:
            if self.fight:
                if symbol == arcade.key.NUM_DECIMAL:
                    self.igrok.prityag_voda()

                if symbol == arcade.key.NUM_6:
                    self.igrok.action(sposobs.KARAKATICA)

                if symbol == arcade.key.Q:
                    self.igrok.block.block = True

                if symbol == arcade.key.SPACE:
                    if self.state_list[5] and not self.udar:
                        self.igrok.action(sposobs.VODA_UDARS)
                    self.press_sposob(symbol, arcade.key.SPACE, sposobs.UDAR)

                if symbol == arcade.key.NUM_0 and self.state_list[8]:
                    if not self.igrok.block.block:
                        self.igrok.action(self.igrok.five_sposobs[4].sposob)
                        if not self.state_list[9]:
                            self.state_list[9] = True
                            self.text_label.text = self.text_obuch_list[9]

                if symbol == arcade.key.NUM_1 and self.state_list[6]:
                    if not self.igrok.block.block:
                        self.igrok.action(self.igrok.five_sposobs[0].sposob)
                        if not self.state_list[7]:
                            self.state_list[7] = True
                            self.text_label.text = self.text_obuch_list[7]

                if symbol == arcade.key.NUM_2 and self.state_list[7]:
                    if not self.igrok.block.block:
                        self.igrok.action(self.igrok.five_sposobs[3].sposob)
                        if not self.state_list[8]:
                            self.state_list[8] = True
                            self.text_label.text = self.text_obuch_list[8]

                if symbol == arcade.key.NUM_3 and self.state_list[9]:
                    if not self.igrok.block.block:
                        self.igrok.action(self.igrok.five_sposobs[2].sposob)
                        if not self.state_list[10]:
                            self.state_list[10] = True
                            self.text_label.text = self.text_obuch_list[10]

            self.press_wad(symbol)
            if symbol == arcade.key.D or symbol == arcade.key.RIGHT and not self.state_list[0]:
                if self.s_kast_scena == 6:
                    self.s_right += 1
                    if ((self.igrok.fizika.is_on_ground or self.igrok.toggle) and not self.igrok.block.block
                            and self.s_right >= 2):
                        self.s_r = 0
                        self.s_right = 0
                        self.igrok.fight = False
                        self.igrok.action(sposobs.REKA, True)

                if self.s_kast_scena < 3 and not self.state_list[2]:
                    self.state_list[0] = True
                    if self.state_list[0] and self.state_list[1]:
                        self.text_label.text = self.text_obuch_list[1]
            elif symbol == arcade.key.A or symbol == arcade.key.LEFT and not self.state_list[0]:
                if self.s_kast_scena == 6:
                    self.s_left += 1
                    if ((self.igrok.fizika.is_on_ground or self.igrok.toggle) and not self.igrok.block.block
                            and self.s_left >= 2):
                        self.s_l = 0
                        self.s_left = 0
                        self.igrok.fight = False
                        self.igrok.action(sposobs.REKA, True)
                        self.obuch = False
                        self.state_list[12] = True

                if self.s_kast_scena < 3 and not self.state_list[2]:
                    self.state_list[1] = True
                    if self.state_list[0] and self.state_list[1]:
                        self.text_label.text = self.text_obuch_list[1]

            if symbol == arcade.key.W or symbol == arcade.key.UP and not self.state_list[2]:
                if self.igrok.fizika.is_on_ground and not self.igrok.stan_for_sposob and not self.igrok.fight: # self.igrok.is_on_ground and
                    if not self.state_list[2]:
                        s = 0
                        for state in self.state_list:
                            if state:
                                s += 1
                        if self.s_kast_scena < 3 and s == 2:
                            self.state_list[2] = True
                            self.text_label.text = self.text_obuch_list[2]

            self.press_lshift(symbol)
            if symbol == arcade.key.LSHIFT and not self.state_list[3]:
                if self.obuch and self.state_list[2] and not self.state_list[3]:
                    self.state_list[3] = True
                    self.obuch = False
                    self.text_label.text = self.text_obuch_list[3]

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.NUM_5:
            self.igrok.block.block = False

        self.release_lshift(_symbol)

        self.release_ad(_symbol)
        if (_symbol == arcade.key.D or _symbol == arcade.key.RIGHT) and self.igrok.toggle and not self.igrok.block.block:
            self.igrok.action(sposobs.REKA, True)
        elif (_symbol == arcade.key.A or _symbol == arcade.key.LEFT) and self.igrok.toggle and not self.igrok.block.block:
            self.igrok.action(sposobs.REKA, True)

    def kast_scena_6(self):
        if self.s_kast_scena == 6 and self.igrok.center_x <= CENTER_X_ROCK - 4500:
            self.list_kast_scen[5] = True
            self.kast_scena = True
            if self.save:
                self.save = False
                open_files.write_csv_file(r'files/positions.csv', [
                    [self.igrok.name, CENTER_X_ROCK - 4000, self.igrok.center_y, self.igrok.storona],
                    [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                    [self.rock.name, self.rock.position[0], self.rock.position[1], 0]
                ], self.window.FIELDNAMES_POSITION)
                open_files.write_file(r'files/kast_scena.txt', [False, self.s_kast_scena])
                open_files.write_file(r'files/states.txt', [self.state_list, self.obuch, self.fight, self.udar,
                                                           self.text_label.text])
        if self.s_kast_scena == 6 and self.list_kast_scen[5]:
            self.igrok.action(sposobs.REKA)
            self.igrok.techenie.hod(-15, self.walls_list)
            self.perexod = True
            if self.igrok.center_x < self.perexod_sprite.left + 3000:
                self.s_kast_scena += 1
                self.list_kast_scen[5] = False
                self.kast_scena = False
                self.igrok.action(sposobs.REKA, True)
                self.kamera_dvizh = False
                open_files.write_csv_file(r'files/positions.csv', [
                    [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                    [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                    [self.rock.name, self.rock.position[0], self.rock.position[1], 0]
                ], self.window.FIELDNAMES_POSITION)
                open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])

    def kast_scena_5(self):
        if self.s_kast_scena == 5 and self.list_kast_scen[4]:
            if self.save:
                self.save = False
                self.igrok.storona = -1
                self.kast_scena = True
                self.fizika.set_friction(self.igrok, 1)
                self.timer_for_s_zoom = 150
                self.zoom_minus = True
                self.kamera_dvizh_x = 0.9 / self.timer_for_s_zoom
                if self.dialog.s_dialog == 1:
                    self.dialog.dialog = self.dialog.skip = False
                    self.dialog.s_dialog += 1
                    self.dialog.clear_text()

                open_files.write_csv_file(r'files/positions.csv', [
                    [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                    [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                    [self.rock.name, self.rock.position[0], self.rock.position[1], 0]
                ], self.window.FIELDNAMES_POSITION)
                open_files.write_csv_file(r'files/bosses.csv', [
                    [self.rock.name, self.rock.hp]
                ], self.window.FIELDNAMES_BOSS)
                open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                open_files.write_file(r'files/states.txt', [self.state_list, self.obuch, self.fight, self.udar,
                                                           self.text_label.text])
            if self.zoom_minus and self.dialog.s_dialog < 4:
                if self.kamera.zoom >= 2:
                    self.s_zoom = 0
                    self.zoom_minus = False
                    self.kamera.zoom = 2
                if self.kamera_koef_x > 1.1:
                    self.kamera_koef_x -= self.kamera_dvizh_x
                else:
                    self.kamera_koef_x = 1.1
                if self.kamera_otnos_x < 1600:
                    self.kamera_otnos_x += 1600 / 150
                else:
                    self.kamera_otnos_x = 1600
                if self.kamera_otnos_y < 950:
                    self.kamera_otnos_y += 950 / 150
                else:
                    self.kamera_otnos_y = 950
            if self.dialog.s_dialog != 21:
                if 4200 < abs(self.sinhelm.center_x - self.igrok.center_x) <= 4800:
                    self.kamera.zoom = 0.5
                    self.kamera_koef_x = 2
                    self.kamera_koef_y = 2
                    self.kamera.position = Vec2(self.igrok.center_x - self.kamera.viewport_width * self.kamera.zoom
                                                / self.kamera_koef_x, 0)
                    self.igrok.animations.gotov = True
                elif 4000 < abs(self.sinhelm.center_x - self.igrok.center_x) <= 4200:
                    self.kamera.zoom = 2
                    self.kamera_koef_x = 1.1
                    self.kamera_koef_y = 4
                    self.kamera.position = Vec2((self.igrok.center_x - self.kamera.viewport_width * self.kamera.zoom
                                                 / self.kamera_koef_x) - self.kamera_otnos_x, self.igrok.center_y -
                                                (self.kamera.viewport_height / self.kamera_koef_y) * self.kamera.zoom +
                                                self.kamera_otnos_y)
                elif 2000 < abs(self.sinhelm.center_x - self.igrok.center_x) <= 4000:
                    if not self.zoom_plus:
                        self.zoom_plus = True
                        self.v_zoom = 1 / 900
                        self.timer_for_s_zoom = 900
                        self.kamera_dvizh_x = 0.9 / 900
                    if self.zoom_plus:
                        if self.kamera_koef_x < 2:
                            self.kamera_koef_x += self.kamera_dvizh_x
                        else:
                            self.kamera_koef_x = 2
                        if self.kamera_otnos_x > 0:
                            self.kamera_otnos_x -= 1600 / 600
                        else:
                            self.kamera_otnos_x = 0
                        if self.kamera_otnos_y > 0:
                            self.kamera_otnos_y -= 950 / 600
                        else:
                            self.kamera_otnos_y = 0

            if 250 < abs(self.sinhelm.center_x - self.igrok.center_x) <= 2000 and self.dialog.s_dialog < 7:
                self.sinhelm.olen_beg = False
                if abs(self.sinhelm.center_x - self.igrok.center_x) <= 1500:
                    self.igrok.animations.gotov = False
                if 2000 > self.sinhelm.center_y > 292:
                    if self.sinhelm.center_y > 1500:
                        force_y = 300
                    elif self.sinhelm.center_y > 1000:
                        force_y = 800
                    else:
                        force_y = 1300
                    if abs(self.sinhelm.center_x - self.igrok.center_x) > 400:
                        force_x = 10000
                        self.sinhelm.pymunk.max_horizontal_velocity = 1000
                    else:
                        force_x = -10
                        self.sinhelm.pymunk.max_horizontal_velocity = 300
                    self.fizika.apply_force(self.sinhelm, (force_x, force_y))
                elif 210 < self.sinhelm.center_y < 292:
                    self.fizika.apply_force(self.sinhelm, (0, 11000))
                elif self.sinhelm.center_y <= 210:
                    self.sinhelm.pymunk.max_horizontal_velocity = 300
                    if not self.sinhelm.animations.landing and not self.sinhelm.is_on_ground:
                        self.sinhelm.animations.landing = True
                if not self.sinhelm.animations.landing and self.sinhelm.is_on_ground:
                    self.fizika.apply_force(self.sinhelm, (8000, 0))
                if self.zoom_plus:
                    if 2250 > self.sinhelm.center_y:
                        self.v_zoom = 1 / 150
                        self.kamera_dvizh_x = 0.9 / 150
                        if self.kamera.zoom <= 0.9:
                            self.zoom_plus = False
                            self.kamera.zoom = 0.9
                            self.s_zoom = 0
                        if self.kamera_koef_x < 2:
                            self.kamera_koef_x += self.kamera_dvizh_x
                        else:
                            self.kamera_koef_x = 2
                        if self.kamera_otnos_x > 0:
                            self.kamera_otnos_x -= 1600 / 150
                        else:
                            self.kamera_otnos_x = 0
                        if self.kamera_otnos_y > 0:
                            self.kamera_otnos_y -= 950 / 100
                        else:
                            self.kamera_otnos_y = 0
                    else:
                        if self.kamera_koef_x < 2:
                            self.kamera_koef_x += self.kamera_dvizh_x
                        else:
                            self.kamera_koef_x = 2
                        if self.kamera_otnos_x > 0:
                            self.kamera_otnos_x -= 1600 / 600
                        else:
                            self.kamera_otnos_x = 0
                        if self.kamera_otnos_y > 0:
                            self.kamera_otnos_y -= 950 / 600
                        else:
                            self.kamera_otnos_y = 0
            elif (abs(self.sinhelm.center_x - self.igrok.center_x) <= 250 and self.dialog.s_dialog < 7
                  and self.sinhelm.is_on_ground):
                if not self.dialog.dialog:
                    if self.dialog.s_dialog == 1:
                        self.dialog.clear_text()
                    self.dialog.dialog = self.dialog.skip = True
                if self.kamera.zoom <= 0.9:
                    self.zoom_plus = False
                    self.kamera.zoom = 0.9
                    self.s_zoom = 0
                self.fizika.set_friction(self.sinhelm, 1)
                self.s_ks = 0
            elif self.dialog.s_dialog == 8:
                if abs(self.sinhelm.center_x - self.igrok.center_x) <= 120:
                    self.fizika.set_friction(self.igrok, 1)
                    self.dialog.skip = True
                else:
                    self.igrok.pymunk.max_horizontal_velocity = 100
                    self.move_sprite(self.igrok, 0.2 / 60, (-5000, 0), 0.6)
            elif self.dialog.s_dialog == 9:
                if len(self.dialog.dialog_slovar[5][self.dialog.s_dialog - 1]) == 0:
                    self.dialog.skip = True
                    self.fizika.set_friction(self.igrok, 1)
                    self.sinhelm.storona = 0
                else:
                    self.dialog.skip = False
                    if abs(self.sinhelm.center_x - self.igrok.center_x) <= 120:
                        self.dialog.skip = True
                        self.fizika.set_friction(self.igrok, 1)
                    else:
                        self.igrok.pymunk.max_horizontal_velocity = 100
                        self.move_sprite(self.igrok, 0.2 / 60, (-5000, 0), 0.6)
            elif self.dialog.s_dialog == 15:
                self.dialog.skip = False
                if len(self.dialog.dialog_slovar[5][self.dialog.s_dialog - 1]) == 0:
                    self.s_ks += 1
                    if self.s_ks >= 60:
                        self.s_ks = 0
                        self.dialog.s_dialog += 1
                        self.dialog.dialog = self.dialog.skip = True
                        self.dialog.clear_text()
            elif self.dialog.s_dialog == 18:
                self.dialog.dialog = self.dialog.skip = False
                self.kamera_otnos_y = 0
                self.s_ks += 1
                if self.s_ks >= 30:
                    self.s_ks = 0
                    self.dialog.dialog = self.dialog.skip = True
                    self.dialog.s_dialog += 1
            elif self.dialog.s_dialog == 23:
                if not self.zoom_minus and self.kamera.zoom < 0.9:
                    self.zoom_minus = True
                    self.v_zoom = 0.3 / 60
                    self.timer_for_s_zoom = 60
                self.dialog.dialog = False
                if not self.sinhelm.animations.podgotovka:
                    self.fizika.apply_force(self.sinhelm, (-8000, 0))
                if abs(self.sinhelm.center_x - self.igrok.center_x) >= 350:
                    self.sinhelm.animations.podgotovka = True
                    self.fizika.set_friction(self.sinhelm, 1)
                    self.s_ks = 0
                    if self.sinhelm.animations.s_podgotovka >= 60:
                        self.dialog.dialog = self.dialog.skip = True
                        self.dialog.s_dialog += 1
                        self.dialog.clear_text()
                else:
                    self.dialog.skip = False
            elif self.dialog.s_dialog == 24:
                self.sinhelm.animations.s_podgotovka = 0
                self.sinhelm.animations.podgotovka = False
            elif self.dialog.s_dialog == 25:
                self.sinhelm.storona = 0
            elif (self.dialog.s_dialog == 26 and self.sinhelm.center_y < 300
                  and abs(self.sinhelm.center_x - self.igrok.center_x) <= 500):
                self.dialog.skip = self.dialog.dialog = False
                self.s_ks += 1
                if self.s_ks >= 90 and self.sinhelm.storona == 0:
                    self.s_ks = 0
                    self.sinhelm.storona = 1
                    self.sinhelm.animations.podgotovka = True
                if not self.sinhelm.animations.podgotovka and self.sinhelm.is_on_ground and self.sinhelm.storona == 1:
                    self.sinhelm.pymunk.max_horizontal_velocity = 700
                    self.fizika.apply_force(self.sinhelm, (-50000, 100000))
            elif self.dialog.s_dialog == 26 and self.sinhelm.center_y > 300:
                self.s_ks += 1
                if self.s_ks >= 120:
                    self.save = True
                    self.sinhelm.olen_beg = True
                    self.igrok.pymunk.max_horizontal_velocity = views.play_views.IG_MAX_HORIZANTAL_SPEED
                    self.s_kast_scena += 1
                    self.list_kast_scen[4] = False
                    self.kast_scena = False
                    self.dialog.s_dialog = 0
                    self.s_ks = 0
                    self.dialog.speakers_list.remove(self.igrok)
                    self.dialog.speakers_list.remove(self.sinhelm)
                    self.obuch = True
                    self.text_label.text = self.text_obuch_list[12]
                    open_files.write_csv_file(r'files/positions.csv', [
                        [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                        [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                        [self.rock.name, self.rock.position[0], self.rock.position[1], 0]
                    ], self.window.FIELDNAMES_POSITION)
                    open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                    open_files.write_file(r'files/states.txt', [self.state_list, self.obuch, self.fight,
                                                                self.udar, self.text_label.text])

            self.dialog.update(5)

    def kast_scena_4(self):
        if self.s_kast_scena == 4 and self.list_kast_scen[3]:
            self.fizika.set_friction(self.igrok, 1)
            self.kast_scena = True
            if self.save:
                self.save = False
                if len(self.dialog.speakers_list) == 0:
                    self.dialog.speakers_list.append(self.igrok)
                    self.dialog.speakers_list.append(self.bratislav)
                open_files.write_csv_file(r'files/positions.csv', [
                    [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                    [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                    [self.bratislav.name, self.bratislav.center_x, self.bratislav.center_y, self.bratislav.storona]
                ], self.window.FIELDNAMES_POSITION)
                open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                self.dialog.s_dialog = 1
                self.dialog.clear_text()
                self.kamera_koef_x = 5
                self.dialog.dialog = self.dialog.skip = True
                self.s_ks = 0
            if self.dialog.s_dialog == 3:
                self.dialog.dialog = self.dialog.skip = False
                if (abs(self.bratislav.center_x - self.igrok.center_x) < 150
                        or self.bratislav.center_x < self.igrok.center_x):
                    self.bratislav.change_x = 3
                    self.s_ks = 0
                else:
                    self.bratislav.change_x = 0
                    self.s_ks += 1
                    if self.s_ks >= 30:
                        self.s_ks = 0
                        self.bratislav.storona = 1
                        self.dialog.s_dialog += 1
                        self.dialog.dialog = self.dialog.skip = True
            elif self.dialog.s_dialog == 19:
                self.dialog.dialog = self.dialog.skip = False
                if (abs(self.bratislav.center_x - self.igrok.center_x) < 300
                        or self.bratislav.center_x < self.igrok.center_x):
                    self.bratislav.change_x = 3
                elif (abs(self.bratislav.center_x - self.igrok.center_x) >= 300
                      and self.bratislav.center_x >= self.igrok.center_x):
                    if self.bratislav.change_x > 0:
                        self.bratislav.animations.priziv = True
                    self.bratislav.change_x = 0
                    if not self.bratislav.animations.priziv and self.bratislav.change_x == 0:
                        self.dialog.s_dialog += 1
                        self.dialog.dialog = self.dialog.skip = True
                        self.bratislav.storona = 1
                        self.dialog.clear_text()
                if self.bratislav.rock:
                    self.rock.center_y += 10
                    # self.fizika.set_position(self.rock, (self.rock.center_x, self.rock.center_y + 10))
                if self.rock.bottom >= 110 and self.bratislav.rock:
                    self.bratislav.rock = False
                    self.fizika.remove_sprite(self.rock)
                    self.fizika.add_sprite(self.rock, MASS_ROCK, 1, max_vertical_velocity=5000, max_horizontal_velocity=300,
                                           moment_of_inertia=self.fizika.MOMENT_INF, damping=0.9)
            elif self.dialog.s_dialog == 21:
                self.igrok.animations.chest = True
            elif self.dialog.s_dialog == 22:
                self.bratislav.animations.chest = True
            elif self.dialog.s_dialog >= 23:
                self.save = True
                self.kamera_koef_x = 2
                self.igrok.animations.chest = False
                self.bratislav.animations.chest = False
                self.bratislav.change_x = -5
                self.dialog.s_dialog = 0
                self.dialog.dialog = self.dialog.skip = False
                self.kast_scena = False
                self.list_kast_scen[3] = False
                self.s_kast_scena += 1
                self.fight = True
                self.dialog.speakers_list.remove(self.igrok)
                self.dialog.speakers_list.remove(self.bratislav)
                self.obuch = True
                self.text_label.text = self.text_obuch_list[3]
                self.igrok.stan_for_sposob = True
                open_files.write_csv_file(r'files/positions.csv', [
                    [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                    [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                    [self.bratislav.name, self.bratislav.center_x, self.bratislav.center_y, self.bratislav.storona],
                    [self.rock.name, self.rock.position[0], self.rock.position[1], 0]
                ], self.window.FIELDNAMES_POSITION)
                open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                open_files.write_file(r'files/states.txt', [self.state_list, self.obuch, self.fight, self.udar,
                                      self.text_label.text])
            self.dialog.update(4)

    def kast_scena_3(self):
        if self.s_kast_scena == 3:
            if 175 < abs(self.bratislav.center_x - self.igrok.center_x) <= 300:
                if self.save:
                    self.kast_scena = True
                    self.save = False
                    open_files.write_csv_file(r'files/positions.csv', [[self.igrok.name, self.igrok.center_x,
                                              self.igrok.center_y, self.igrok.storona], [self.sinhelm.name,
                                              self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona]],
                                              self.window.FIELDNAMES_POSITION)
                    open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                    self.dialog.s_dialog += 1
                    self.dialog.dialog = True
                    self.dialog.skip = True
                    self.dialog.speakers_list.append(self.igrok)
                    self.dialog.speakers_list.append(self.bratislav)
                self.list_kast_scen[2] = True
                self.move_sprite(self.igrok, 0.2 / 60, (3000, 0), 0.6)
            elif abs(self.bratislav.center_x - self.igrok.center_x) <= 175 and self.dialog.s_dialog <= 10:
                self.fizika.set_friction(self.igrok, 1)
            elif self.dialog.s_dialog >= 13:
                self.save = True
                self.list_kast_scen[2] = False
                self.kast_scena = False
                self.s_kast_scena += 1
                self.dialog.dialog = self.dialog.skip = False
                self.dialog.s_dialog = 0
                self.dialog.speakers_list.remove(self.igrok)
                self.dialog.speakers_list.remove(self.bratislav)
                open_files.write_csv_file(r'files/positions.csv', [
                    [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                    [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona],
                    [self.bratislav.name, self.bratislav.center_x, self.bratislav.center_y, self.bratislav.storona]
                ], self.window.FIELDNAMES_POSITION)
                open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
            self.dialog.update(3)

    def kast_scena_2(self):
        if self.s_kast_scena == 2:
            if self.sinhelm.center_x >= self.igrok.center_x:
                self.sinhelm.storona = 1
                if (200 >= abs(self.sinhelm.center_x - self.igrok.center_x) > 175 and not self.list_kast_scen[0]
                        and self.dialog.s_dialog < 12):
                    self.list_kast_scen[1] = True
                    self.kast_scena = True
                    if self.save:
                        self.save = False
                        self.dialog.speakers_list.append(self.igrok)
                        self.dialog.speakers_list.append(self.sinhelm)
                        open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                        open_files.write_csv_file(r'files/positions.csv', [[self.igrok.name,
                                                                            self.igrok.center_x, self.igrok.center_y,
                                                                            self.igrok.storona]], self.window.FIELDNAMES_POSITION)
                        open_files.write_file(r'files/states.txt', [self.state_list, self.obuch, self.fight,
                                                                    self.udar, self.text_label.text])
                    self.move_sprite(self.igrok, 0.2 / 60, (3000, 0), 0.6)
                    if not self.dialog.dialog and self.dialog.s_dialog == 0:
                        self.dialog.clear_text()
                        self.dialog.s_dialog += 1
                    self.dialog.dialog = True
                    self.dialog.skip = True
                if self.list_kast_scen[1] and 175 >= abs(self.sinhelm.center_x - self.igrok.center_x):
                    self.fizika.set_friction(self.igrok, 1)
                    if self.dialog.s_dialog == 8 and 90 >= len(self.dialog.dialog_slovar[2][self.dialog.s_dialog - 1]) >= 45:
                        self.sinhelm.animations.ukaz = True
                        self.sinhelm.storona = 0
                    elif self.dialog.s_dialog >= 12:
                        self.dialog.s_dialog = 12
                        self.dialog.skip = False
                        self.dialog.dialog = False
                        self.kast_scena = False
            else:
                self.sinhelm.storona = 0
                if self.dialog.s_dialog == 12:
                    self.sinhelm.sulky = True
                    #self.move_sprite(self.igrok, 0.2 / 60, (3000, 0), 0.6)
                    if abs(self.sinhelm.center_x - self.igrok.center_x) >= 400:
                        self.dialog.s_dialog += 1
                        self.dialog.clear_text()
                        self.dialog.dialog = self.dialog.skip = True
                        self.fizika.add_sprite(self.sinhelm, views.play_views.MASS_IGROK, views.play_views.FRICTION_IGROK,
                                               max_vertical_velocity=views.play_views.IG_MAX_VERTICAL_SPEED,
                                               max_horizontal_velocity=views.play_views.IG_MAX_HORIZANTAL_SPEED,
                                               moment_of_inertia=self.fizika.MOMENT_INF, damping=0.9)
                        self.levo = False
                        self.pravo = False
                        self.kast_scena = True
                elif self.dialog.s_dialog == 13 and len(self.dialog.dialog_slovar[2][self.dialog.s_dialog - 1]) == 0:
                    self.igrok.sulky = True
                    self.dialog.skip = True
                elif self.dialog.s_dialog == 15:
                    self.igrok.storona = -1
                elif self.dialog.s_dialog == 16:
                    self.s_ks += 1
                    self.dialog.skip = False
                    self.dialog.dialog = False
                    if self.s_ks >= 30 and not self.dialog.dialog:
                        self.move_sprite(self.igrok, 0.2 / 60, (-3000, 0), 0.6)
                    if abs(self.sinhelm.center_x - self.igrok.center_x) <= 150:
                        self.dialog.dialog = True
                        self.dialog.skip = True
                        self.fizika.set_friction(self.igrok, 1)
                        self.dialog.s_dialog += 1
                        self.dialog.clear_text()
                elif self.dialog.s_dialog == 19:
                    self.dialog.skip = self.dialog.dialog = False
                    self.s_ks += 1
                    if self.s_ks >= 30:
                        self.dialog.skip = self.dialog.dialog = True
                        self.dialog.s_dialog += 1
                elif self.dialog.s_dialog == 24:
                    self.sinhelm.sulky = False
                    self.igrok.sulky = False
                    self.sinhelm.not_fizik = False
                    self.dialog.dialog = False
                    self.dialog.skip = False
                    self.kast_scena = False
                    self.dialog.speakers_list.remove(self.igrok)
                    self.dialog.speakers_list.remove(self.sinhelm)
                    self.s_ks = 0
                    self.dialog.s_dialog = 0
                    self.list_kast_scen[1] = False
                    self.s_kast_scena += 1
                    self.save = True
                    open_files.write_csv_file(r'files/positions.csv', [
                        [self.igrok.name, self.igrok.center_x, self.igrok.center_y, self.igrok.storona],
                        [self.sinhelm.name, self.sinhelm.center_x, self.sinhelm.center_y, self.sinhelm.storona]
                    ], self.window.FIELDNAMES_POSITION)
                    open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
            self.dialog.update(2)

    def kast_scena_1(self):
        if self.list_kast_scen[0] and self.s_kast_scena == 1:
            self.kast_scena = True
            self.kamera_dvizh = False
            if self.igrok.center_x < 0:
                if len(self.dialog.speakers_list) == 0:
                    self.dialog.speakers_list.append(self.igrok)
                    self.dialog.speakers_list.append(self.interaction_list[0])
                if not self.vit:
                    if self.igrok.animations.wasu:
                        self.window.set_mouse_visible(False)
                        self.center_kamera_za_igrok()
                        self.igrok.animations.write_and_stand_up_animation()
                    else:
                        self.window.set_mouse_visible()
                        if not self.vibor and not self.read:
                            self.vibor = True
                            self.igrok.animations.read = True
                else:
                    self.window.set_mouse_visible(False)
                    self.move_sprite(self.igrok, 0.2 / 60, (views.play_views.IGROK_MOVE_GROUND, 0), 0.6)

            ekran_center_y = self.igrok.center_y - self.kamera.viewport_height / 4
            if self.igrok.center_x >= 0 and self.dialog.s_dialog == 0 and not self.dialog.dialog:
                self.kamera.position = Vec2(-200, ekran_center_y)
                self.x, self.y = self.kamera.position
                self.kamera.zoom = 0.9
                self.dialog.dialog = True
                self.dialog.skip = True
                self.dialog.s_dialog += 1

            if 0 < self.dialog.s_dialog < 3 and self.interaction_list[0].center_x < 500:
                self.fizika.set_friction(self.igrok, 1)
                self.kamera.move_to((-200, ekran_center_y), 0)
            if self.interaction_list[0].center_x >= 500:
                if self.interaction_list[0].change_x > 0:
                    self.interaction_list[0].animations.anim = True
                self.interaction_list[0].change_x = 0
                if self.interaction_list[0].animations.anim:
                    self.interaction_list[0].animations.animation_1()
                else:
                    self.dialog.s_dialog = 0
                    self.kamera_dvizh = True
                    self.interaction_list.remove(self.interaction_list[0])
                    self.list_kast_scen[0] = False
                    self.kast_scena = False
                    self.s_kast_scena += 1
                    self.obuch = True
                    self.new_game = False
                    open_files.write_file(r'files/NEW_GAME.txt', [self.new_game])
                    open_files.write_file(r'files/kast_scena.txt', [self.kast_scena, self.s_kast_scena])
                    open_files.write_csv_file(r'files/positions.csv', [[self.igrok.name, self.igrok.center_x,
                                                                        self.igrok.center_y, self.igrok.storona]],
                                              self.window.FIELDNAMES_POSITION)
                    open_files.write_file(r'files/states.txt', [self.state_list, self.obuch, self.fight,
                                                                self.udar, self.text_label.text])
                    self.dialog.clear_text()
            else:
                if self.dialog.s_dialog == 3:
                    if self.dialog.dialog:
                        self.dialog.speakers_list.remove(self.igrok)
                        self.dialog.speakers_list.remove(self.interaction_list[0])
                    self.dialog.dialog = False
                    self.dialog.skip = False
                if not self.dialog.dialog and self.dialog.s_dialog > 2:
                    self.interaction_list[0].change_x = 8

            self.dialog.update(1)

    def dop_func(self, ekran_center_x: float, ekran_center_y: float):
        if ekran_center_x >= CENTER_X_ROCK - 1100:
            ekran_center_x = CENTER_X_ROCK - 1100
        if ekran_center_x <= CENTER_X_ROCK - 1100 and self.rock.hp > 0 and self.s_kast_scena == 5:
            ekran_center_x = CENTER_X_ROCK - 1100
        elif ekran_center_x < -200 and self.s_kast_scena > 1:
            ekran_center_x = -200

        ekran_center_y = -64

        return ekran_center_x, ekran_center_y
