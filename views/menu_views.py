import arcade
import arcade.gui
from arcade.gui.widgets import buttons, layout, text, slider
import open_files
from my_gui import ui

BACKGROUND_COLOR = (0, 135, 206, 235)

COMPLEXITY_TUPLE = ('Лёгкая', 'Средняя', 'Сложная')
Complexity = COMPLEXITY_TUPLE[1]
Value_Zvuk_Effekt = 100
Value_Music = 100


class MainMenuViev(arcade.View):
    def __init__(self, viev: arcade.View):
        super().__init__()
        self.viev = viev
        self.show = False

        self.window.background_color = arcade.csscolor.GRAY
        self.window.set_mouse_visible()

        self.manager = arcade.gui.UIManager()
        self.v_box = None

        self.settings = False
        self.settings_manager = ui.SettingManager(Value_Zvuk_Effekt, Value_Music, COMPLEXITY_TUPLE, Complexity)
        self.settings_v_box = None
        self.settings_v_box_buttons = None

    def on_show_view(self):
        self.manager.enable()
        self.v_box = layout.UIBoxLayout(space_between=20)

        nachat_button = buttons.UIFlatButton(text='Начать играть', width=400, height=80, style=ui.BUTTONS_STYLE)
        self.v_box.add(nachat_button)
        settings_button = buttons.UIFlatButton(text='Настройки', width=400, height=80, style=ui.BUTTONS_STYLE)
        self.v_box.add(settings_button)
        viti_button = buttons.UIFlatButton(text='Выйти из игры', width=400, height=80, style=ui.BUTTONS_STYLE)
        self.v_box.add(viti_button)

        ui_anchor_layuot = layout.UIAnchorLayout()
        ui_anchor_layuot.add(self.v_box, anchor_x='center_x', anchor_y='center_y')
        self.manager.add(ui_anchor_layuot)

        @nachat_button.event('on_click')
        def on_click_nachat(event):
            self.window.set_mouse_visible(False)
            arcade.set_background_color((0, 135, 206, 235))
            self.show = False
            self.viev.show = True
            self.viev.setup()
            self.window.show_view(self.viev)
            open_files.write_file(r'files/settings.txt', [Complexity.replace('\n', ''),
                                                          Value_Zvuk_Effekt, Value_Music])

        @settings_button.event('on_click')
        def on_click_setting(event):
            self.settings = self.settings_manager.active = True

        @viti_button.event('on_click')
        def on_click_viti(event):
            open_files.write_file(r'files/settings.txt', [Complexity.replace('\n', ''),
                                                          Value_Zvuk_Effekt, Value_Music])
            arcade.close_window()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        if self.settings:
            self.manager.disable()
            self.settings_manager.enable()
            self.settings_manager.draw()
            global Value_Zvuk_Effekt, Value_Music, Complexity
            self.settings, Value_Zvuk_Effekt, Value_Music, Complexity = self.settings_manager.return_values()
        else:
            self.settings_manager.disable()
            self.manager.enable()
            self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == (arcade.key.ENTER or arcade.key.NUM_ENTER):
            arcade.set_background_color((0, 135, 206, 235))
            self.window.show_view(self.viev)


class PauseViev(arcade.View):
    def __init__(self, viev: arcade.View, fieldnames_position: list[str], fieldnames_bosses: list[str]):
        super().__init__()
        self.viev = viev
        self.window.background_color = arcade.csscolor.GRAY
        self.show = False

        self.manager = arcade.gui.UIManager()
        self.v_box = None
        self.v_box_text = None

        self.settings_manager = ui.SettingManager(Value_Zvuk_Effekt, Value_Music, COMPLEXITY_TUPLE, Complexity)
        self.settings_v_box = None
        self.settings_v_box_buttons = None
        self.settings = False

        self.fieldnames_position = fieldnames_position
        self.fieldnames_bosses = fieldnames_bosses
        self.new_game = False

    def on_show_view(self):
        self.manager.enable()
        self.v_box = layout.UIBoxLayout(space_between=50)
        self.v_box_text = layout.UIBoxLayout()

        text_pause = text.UILabel(text='Пауза', font_size=40, font_name='Comic Sans MS', height=80, width=160, bold=True)
        self.v_box_text.add(text_pause)
        prodolzhit_button = buttons.UIFlatButton(text='Продолжить', width=400, height=80, style=ui.BUTTONS_STYLE)
        self.v_box.add(prodolzhit_button)
        settings_button = buttons.UIFlatButton(text='Настройки', width=400, height=80, style=ui.BUTTONS_STYLE)
        self.v_box.add(settings_button)
        viti_buttonn = buttons.UIFlatButton(text="Сохранить и выйти", width=400, height=80, style=ui.BUTTONS_STYLE)
        self.v_box.add(viti_buttonn)

        ui_anchor_layuot = layout.UIAnchorLayout()
        ui_anchor_layuot.add(self.v_box, anchor_x='center_x', anchor_y='center_y')
        ui_anchor_layuot.add(self.v_box_text, anchor_x='center_x', anchor_y='top', align_y=-40)
        self.manager.add(ui_anchor_layuot)

        @prodolzhit_button.event('on_click')
        def on_clock_prodolxzhit(event):
            self.show = False
            self.viev.show = True
            self.window.set_mouse_visible(False)
            self.window.background_color = BACKGROUND_COLOR
            self.window.show_view(self.viev)
            open_files.write_file(r'files/settings.txt', [Complexity.replace('\n', ''),
                                                          Value_Zvuk_Effekt, Value_Music])

        @settings_button.event('on_click')
        def on_click_settings(event):
            self.settings = self.settings_manager.active = True

        @viti_buttonn.event('on_click')
        def on_click_viti(event):
            if not self.viev.kast_scena:
                open_files.write_csv_file(r'files/positions.csv', [
                    [self.viev.igrok.name, self.viev.igrok.center_x, self.viev.igrok.center_y, self.viev.igrok.storona],
                    [self.viev.sinhelm.name, self.viev.sinhelm.center_x, self.viev.sinhelm.center_y, self.viev.sinhelm.storona],
                    [] if self.viev.bratislav is None else [self.viev.bratislav.name, self.viev.bratislav.center_x,
                                                        self.viev.bratislav.center_y,
                                                        self.viev.bratislav.storona],
                    [self.viev.rock.name, self.viev.rock.center_x, self.viev.rock.center_y, 0]
                ], self.fieldnames_position)
                open_files.write_csv_file(r'files/bosses.csv', [[self.viev.rock.name, self.viev.rock.hp]], self.fieldnames_bosses)
                open_files.write_file(r'files/kast_scena.txt', [False, self.viev.s_kast_scena])
                open_files.write_file(r'files/states.txt', [self.viev.state_list, self.viev.obuch, self.viev.fight,
                                                            self.viev.udar, self.viev.text_label.text])
                open_files.write_file(r'files/NEW_GAME.txt', [self.new_game])
                open_files.write_file(r'files/settings.txt', [Complexity.replace('\n', ''),
                                                              Value_Zvuk_Effekt, Value_Music])
            self.show = False
            self.window.main_menu_view.show = True
            self.window.show_view(self.window.main_menu_view)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        if not self.settings:
            self.settings_manager.disable()
            self.manager.enable()
            self.manager.draw()
        else:
            self.manager.disable()
            self.settings_manager.enable()
            self.settings_manager.draw()
            global Value_Zvuk_Effekt, Value_Music, Complexity
            self.settings, Value_Zvuk_Effekt, Value_Music, Complexity = self.settings_manager.return_values()
