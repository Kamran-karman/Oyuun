import arcade
from arcade import gui
from arcade.gui.widgets import text, layout

import open_files

TIMER_FOR_S_TEXT_LIST = (2, 6, 12)
PAUSE_KONEC_STR = '.!?'
PAUSE_NACH_STR = ',;:–'
KOEF = 14/15

FONT_SIZE = 16
FONT_NAME = 'Comic Sans MS'
TEXT_COLOR = arcade.csscolor.BLACK
LABEL_WIDTH_KOEF = 0.625 * 11/12
LADEL_HEIGHT_KOEF = 2/14
ANCHOR_HEIGHT_KOEF = 1/18


class Dialogs:
    DIALOG_SLOVAR = {}

    def __init__(self, speakers_slovar: dict, window: arcade.Window, kamera: arcade.Camera):
        self.dialog = False
        self.s_dialog = 0
        self.skip = False
        self.skip1 = False
        self.skip2 = False

        self.__speakers_dialog: tuple[str::] = ()
        self.speakers_slovar = speakers_slovar
        self.speakers_list = []

        self._window = window
        self._kamera = kamera

        self.manager_dialog = gui.UIManager()
        self.dialog_label = text.UILabel(width=self._window.width * LABEL_WIDTH_KOEF, height=self._window.height * LADEL_HEIGHT_KOEF,
                                         font_size=FONT_SIZE, font_name=FONT_NAME, text_color=TEXT_COLOR, multiline=True)
        ui_anchor_layout = layout.UIAnchorLayout(y=self._window.height * ANCHOR_HEIGHT_KOEF)
        ui_anchor_layout.add(self.dialog_label, anchor_x='center_x', anchor_y='bottom')
        self.manager_dialog.add(ui_anchor_layout)

        self.dialog_slovar = {}
        self.s = 0

        self.__s_text = 0
        self.__timer_for_s_text_list = TIMER_FOR_S_TEXT_LIST
        self.__pause_konec_str = PAUSE_KONEC_STR
        self.__pause_nach_str = PAUSE_NACH_STR
        self.__pause0 = False
        self.__pause1 = False

    def create_dialog_slovar(self, number_list: tuple[float::], speakers_dialog: tuple[str::], level: str,
                             format: str = '.txt'):
        main_patch = f'files/DIALOGS/{level}/dialog'
        self.__speakers_dialog = speakers_dialog
        files_list = []
        for i in number_list:
            if i * 10 % 10 == 0:
                files_list.append(f'{main_patch}{i}{format}')
            else:
                files_list.append(f'{main_patch}_dop{i}{format}')
        s = 0
        for file in files_list:
            dialog = []
            open_files.read_file(file, dialog)
            self.dialog_slovar.update({number_list[s]: dialog})
            self.DIALOG_SLOVAR.update({number_list[s]: dialog.copy()})
            s += 1

    def update(self, s: float):
        self.s = s
        s_d = self.s_dialog
        if self.s_dialog >= len(self.dialog_slovar[s]):
            s_d = len(self.dialog_slovar[s])

        if self.dialog:
            self.__s_text += 1
            timer_fos_s_text = self.__timer_for_s_text_list[0]
            if self.__pause1:
                timer_fos_s_text = self.__timer_for_s_text_list[1]
            elif self.__pause0:
                timer_fos_s_text = self.__timer_for_s_text_list[2]
            if self.__s_text >= timer_fos_s_text:
                self.__s_text = 0
                self.__pause0 = self.__pause1 = False
                for i in self.dialog_slovar[s][s_d - 1]:
                    if (i in self.__speakers_dialog and len(self.dialog_slovar[s][s_d - 1]) ==
                            len(self.DIALOG_SLOVAR[s][s_d - 1])):
                        for q in self.speakers_slovar:
                            if q == int(self.__speakers_dialog[q]) == int(i):
                                self.speakers_slovar[q].speak = True
                                if self.speakers_slovar[q] == self.speakers_list[0]:
                                    self.speakers_list[0].speak = True
                                elif self.speakers_slovar[q] == self.speakers_list[0]:
                                    self.speakers_list[1].speak = True
                            else:
                                self.speakers_slovar[q].speak = False
                                if self.speakers_slovar[q] == self.speakers_list[0]:
                                    self.speakers_list[0].speak = False
                                elif self.speakers_slovar[q] == self.speakers_list[0]:
                                    self.speakers_list[1].speak = False
                    else:
                        if self.dialog_label.text == self.DIALOG_SLOVAR[s][s_d - 1][1::]:
                            break
                        self.dialog_label.text += i
                        if i in self.__pause_konec_str:
                            self.__pause0 = True
                        if i in self.__pause_nach_str:
                            self.__pause1 = True
                    self.dialog_slovar[s][s_d - 1] = self.dialog_slovar[s][s_d - 1].replace(i, '', 1)
                    if len(self.dialog_slovar[s][s_d - 1]) == 0:
                        self.__pause1 = self.__pause0 = False
                    break

    def draw(self, x: float, y: float):
        if self.dialog:
            def draw_rect(center_x, center_y, width, height, scale=1):
                # print(center_x, center_y) # 864.0 162.0
                color = arcade.csscolor.WHITE
                koef = KOEF
                radius = (width * (1 - koef)) / 2

                arcade.draw_rectangle_filled(x + center_x, y + center_y, width * koef, height, color)

                arcade.draw_circle_filled(x + center_x - width * koef / 2, (y + center_y - height / 2) + radius,
                                          radius, color)
                arcade.draw_circle_filled(x + center_x + width * koef / 2, (y + center_y - height / 2) + radius,
                                          radius, color)
                arcade.draw_circle_filled(x + center_x + width * koef / 2, (y + center_y + height / 2) - radius,
                                          radius, color)
                arcade.draw_circle_filled(x + center_x - width * koef / 2, (y + center_y + height / 2) - radius,
                                          radius, color)

                arcade.draw_rectangle_filled(x + center_x - width * koef / 2, y + center_y, width * (1 - koef),
                                             height - 2 * radius, color)
                arcade.draw_rectangle_filled(x + center_x + width * koef / 2, y + center_y, width * (1 - koef),
                                             height - 2 * radius, color)

                if self.speakers_list[0].speak:
                    index = 0
                    if self.speakers_list[0].sulky:
                        index = 1
                    arcade.draw_scaled_texture_rectangle(x + center_x - width * (13 / 15) / 2,
                                                         y + center_y + self._window.height * 7 / 180,
                                                         self.speakers_list[0].animations.dialog_textures[index][0],
                                                         scale)
                elif self.speakers_list[1].speak:
                    index = 0
                    if self.speakers_list[1].sulky:
                        index = 1
                    arcade.draw_scaled_texture_rectangle(x + center_x - width * (13 / 15) / 2,
                                                         y + center_y + self._window.height * 7 / 180,
                                                         self.speakers_list[1].animations.dialog_textures[index][0],
                                                         scale)

            if self._kamera.zoom == 0.65:
                draw_rect(self._window.width * 0.5 * self._kamera.zoom, self._window.height * self._kamera.zoom * 91/351,
                          self._window.width * 0.49 * self._kamera.zoom, self._window.height * self._kamera.zoom / 8)
            else:
                draw_rect(self._window.width * 0.5 * self._kamera.zoom, self._window.height * self._kamera.zoom / 6,
                          self._window.width * 0.625 * self._kamera.zoom, self._window.height * self._kamera.zoom / 6)  # 5/36
            self.manager_dialog.draw()

    def skip_func(self):
        if self.skip and self.dialog:
            if self.dialog_label.text == self.DIALOG_SLOVAR[self.s][self.s_dialog - 1][1::]:
                self.skip1 = False
                self.skip2 = True
            else:
                self.skip1 = True
                self.skip2 = False
            if self.skip1:
                self.dialog_label.text = self.DIALOG_SLOVAR[self.s][self.s_dialog - 1][1::]
                self.skip2 = True
                self.skip1 = False
            elif self.skip2:
                self.skip2 = False
                self.skip1 = True
                self.s_dialog += 1
                self.clear_text()

    def clear_text(self):
        self.dialog_label.text = ''
