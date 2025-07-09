import os
import sys
import arcade.gui
from views import menu_views
from views.play_views import prolog, glava_1
import open_files

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

W = 1600
H = 900

RESET = False

FALSE_STR = 'False'
TRUE_STR = 'True'
NEW_GAME = True
POSITION_SLOVAR = {}

with open(r'files/NEW_GAME.txt', 'r') as file_NEW_GAME:
    state = file_NEW_GAME.read()
    open_files.read_csv_file('files/positions.csv', POSITION_SLOVAR)
    if state == FALSE_STR:
        NEW_GAME = False
file_NEW_GAME.close()

with open(r'files/settings.txt') as file_setting:
    menu_views.Complexity = menu_views.COMPLEXITY_TUPLE[1] if NEW_GAME else file_setting.readline()

    menu_views.Value_Zvuk_Effekt = 100 if NEW_GAME else float(file_setting.readline())
    menu_views.Value_Music = 100 if NEW_GAME else float(file_setting.readline())


GRAVITY = (0, -1500)
DAMPING = 0.9

# s = 1
# file = open('files/DIALOGS/dialog5.txt', encoding='utf-8')
# dialog = file.readlines()
# file.close()
# for i in TEXT_OBUCH_LIST:
#     print(s, i)
#     s += 1


class MyWindow(arcade.Window):
    FIELDNAMES_POSITION = ['pers', 'center_x', 'center_y', 'storona']
    FIELDNAMES_BOSS = ['pers', 'hp']
    FALSE_STR = 'False'
    TRUE_STR = 'True'

    def __init__(self, width, height, position_slovar, new_game):
        super().__init__(width, height, fullscreen=True, vsync=True)

        self.prolog_view = prolog.PrologViev(position_slovar, new_game)
        self.glava_1_view = glava_1.GlavaFirstView(position_slovar, new_game)
        self.glava_2_view = None
        self.glava_3_view = None

        self.pause_view = menu_views.PauseViev(self.prolog_view, self.FIELDNAMES_POSITION, self.FIELDNAMES_BOSS)
        self.main_menu_view = menu_views.MainMenuViev(self.prolog_view)
        #self.show_view(self.main_menu_view)
        self.glava_1_view.setup()

    def on_update(self, delta_time: float):
        # if self.main_menu_view.show:
        #     self.show_view(self.main_menu_view)
        # elif self.pause_view.show:
        #     self.show_view(self.pause_view)
        # elif self.prolog_view.show:
        #     self.show_view(self.prolog_view)
        if self.glava_1_view.show:
            self.show_view(self.glava_1_view)


window = MyWindow(W, H, POSITION_SLOVAR, NEW_GAME)
# 1920, 1080

arcade.run()
