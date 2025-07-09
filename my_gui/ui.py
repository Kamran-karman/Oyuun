from copy import deepcopy

import arcade
import arcade.gui
from arcade.gui import UIOnClickEvent
from arcade.gui.widgets import buttons, slider, layout, text, image

from interaction_sprites.battles.igrok import BetaOyuun, Oyuun
import instruments
from instruments import PNG
from my_gui.circles import Circles

BUTTONS_STYLE = {
            "normal": buttons.UIFlatButton.UIStyle(
                18, ('Comic Sans MS', 'Comic Sans MS'),
                bg=(255, 0, 0, 255)
            ),
            "hover": buttons.UIFlatButton.UIStyle(
                font_size=23,
                font_name=('Comic Sans MS', 'Comic Sans MS'),
                font_color=arcade.csscolor.WHITE,
                bg=(255, 0, 0, 255),
                border=arcade.csscolor.WHITE,
                border_width=2,
            ),
            "press": buttons.UIFlatButton.UIStyle(
                font_size=13,
                font_name=('Comic Sans MS', 'Comic Sans MS'),
                font_color=(255, 0, 0, 255),
                bg=arcade.color.WHITE,
                border=(255, 0, 0, 255),
                border_width=5,
            ),
            "disabled": buttons.UIFlatButton.UIStyle(
                font_size=20,
                font_name=('Comic Sans MS', 'Comic Sans MS'),
                font_color=arcade.color.WHITE,
                bg=(255, 0, 0, 255),
                border=arcade.color.WHITE,
                border_width=7,
            )
        }
MINI_BUTTONS_STYLE = {
            "normal": buttons.UIFlatButton.UIStyle(
                10, ('Comic Sans MS', 'Comic Sans MS'),
                bg=(255, 0, 0, 255)
            ),
            "hover": buttons.UIFlatButton.UIStyle(
                font_size=12,
                font_name=('Comic Sans MS', 'Comic Sans MS'),
                font_color=arcade.csscolor.WHITE,
                bg=(255, 0, 0, 255),
                border=arcade.csscolor.WHITE,
                border_width=2,
            ),
            "press": buttons.UIFlatButton.UIStyle(
                font_size=7,
                font_name=('Comic Sans MS', 'Comic Sans MS'),
                font_color=(255, 0, 0, 255),
                bg=arcade.color.WHITE,
                border=(255, 0, 0, 255),
                border_width=5,
            ),
            "disabled": buttons.UIFlatButton.UIStyle(
                font_size=12,
                font_name=("calibri", "arial"),
                font_color=arcade.color.WHITE,
                bg=arcade.color.GRAY,
                border=None,
                border_width=2,
            )
        }
SLIDERS_STYLE = {
    "normal": slider.UISliderStyle(
        bg=arcade.csscolor.RED,
        border=arcade.csscolor.BLACK,
        border_width=1,
        filled_bar=arcade.color.RED,
        unfilled_bar=(189, 195, 199, 255)
    ),
    "hover": slider.UISliderStyle(
        bg=arcade.csscolor.RED,
        border=arcade.csscolor.BLACK,
        border_width=2,
        filled_bar=arcade.csscolor.RED,
        unfilled_bar=arcade.csscolor.WHITE,
    ),
    "press": slider.UISliderStyle(
        bg=arcade.csscolor.RED,
        border=arcade.csscolor.BLACK,
        border_width=5,
        filled_bar=arcade.csscolor.RED,
        unfilled_bar=arcade.csscolor.WHITE,
    ),
    "disabled": slider.UISliderStyle(
        bg=arcade.csscolor.RED,
        border=arcade.csscolor.WHITE,
        border_width=1,
        filled_bar=(50, 50, 50, 255),
        unfilled_bar=arcade.csscolor.BLACK,
    )
}
FONT_NAME = 'Comic Sans MS'


class MyUIManager(arcade.gui.UIManager):
    def __init__(self):
        super().__init__()
        self.ui_anchor_layuot = self.add(layout.UIAnchorLayout())
        self.active = False


class SettingManager(MyUIManager):

    class Dropdown(arcade.gui.UIDropdown):
        def _update_options(self):
            self._layout.clear()

            active_style = deepcopy(BUTTONS_STYLE)
            active_style["normal"]["bg"] = arcade.csscolor.WHITE
            active_style['normal']['border'] = arcade.csscolor.RED
            active_style['normal']['font_color'] = arcade.csscolor.RED
            active_style['normal']['border_width'] = 2

            for option in self._options:
                if option is None:
                    self._layout.add(
                        arcade.gui.UIWidget(width=self.width, height=2).with_background(
                            color=arcade.color.WHITE
                        )
                    )
                    continue
                else:
                    button = self._layout.add(
                        buttons.UIFlatButton(
                            text=option,
                            width=self.width,
                            height=self.height,
                            style=active_style
                            if self.value == option
                            else BUTTONS_STYLE.copy(),
                        )
                    )
                button.on_click = self._on_option_click

        def new_style(self, style):
            self._default_button.style = style

    def __init__(self, value_zvuk_effekt: float, value_music: float, dropdown_options: tuple[str::], default: str):
        super().__init__()
        self.active = True

        self.zvuk_v_box = layout.UIBoxLayout(space_between=50, align='left')
        self.gameplay_v_box = layout.UIBoxLayout(space_between=50, align='left')

        dropdown_label = arcade.gui.UILabel(text='Сложность', font_name=FONT_NAME, font_size=30, align='left', bold=True)
        self.gameplay_v_box.add(dropdown_label)
        self.dropdown = self.Dropdown(default=default, options=dropdown_options, width=500, height=60)
        self.gameplay_v_box.add(self.dropdown)
        self.dropdown.new_style(BUTTONS_STYLE)

        zvuk_label = text.UILabel(text='Звук', font_name=FONT_NAME, font_size=30, align='left', bold=True)
        self.zvuk_v_box.add(zvuk_label)
        slider_zvuk_effect_label = text.UILabel(text='Звуковые эффекты', font_name=FONT_NAME, font_size=25, align='left')
        self.zvuk_v_box.add(slider_zvuk_effect_label)
        self.slider_zvuk_effect = slider.UISlider(value=value_zvuk_effekt, width=500, height=40,
                                                  style=SLIDERS_STYLE)
        self.zvuk_v_box.add(self.slider_zvuk_effect)
        slider_music_label = text.UILabel(text='Музыка', font_name=FONT_NAME, font_size=25, align='left')
        self.zvuk_v_box.add(slider_music_label)
        self.slider_music = slider.UISlider(value=value_music, width=500, height=40, style=SLIDERS_STYLE)
        self.zvuk_v_box.add(self.slider_music)

        vernutsya_button = buttons.UIFlatButton(text='Вернуться', width=150, height=50, style=MINI_BUTTONS_STYLE)
        text_layout = text.UILabel(text='Настройки', font_name='Comic Sans MS', font_size=50, width=337, height=150,
                                   bold=True)

        @vernutsya_button.event('on_click')
        def on_click_vernutsya(event):
            self.active = False

        self.ui_anchor_layuot.add(text_layout, anchor_x='center_x', anchor_y='top')
        self.ui_anchor_layuot.add(vernutsya_button, anchor_x='left', anchor_y='top')
        self.ui_anchor_layuot.add(self.zvuk_v_box, anchor_x='center_x', anchor_y='center_y',
                                  align_x=-self.window.width * 0.2)
        self.ui_anchor_layuot.add(self.gameplay_v_box, anchor_x='center_x', anchor_y='center_y',
                                  align_y=self.window.height * 0.141, align_x=self.window.width * 0.2)

    def return_values(self):
        return self.active, self.slider_zvuk_effect.value, self.slider_music.value, self.dropdown.value

    def new_values(self, value_zvuk_effekt: float, value_music: float, complexity: str):
        self.slider_zvuk_effect.value, self.slider_music.value, self.dropdown.value = (value_zvuk_effekt, value_music,
                                                                                       complexity)


class ViborSosob(MyUIManager):
    def __init__(self, igrok: BetaOyuun, row: int, col: int, default_texture_list: instruments.TextureList,
                 circles: Circles):
        super().__init__()
        self.igrpk = igrok

        self.update_rate = 1

        self.__s_active = 0
        self.__timer_for_s_active = 900

        self.kd = 0
        self.__s_kd = 0
        self.__timer_for_s_kd = 60

        self._nomer_sposob = 0

        self._v_box_five = layout.UIBoxLayout(space_between=10, align='right')
        s = 0
        for texture in default_texture_list:
            img = image.UIImage(texture=texture)
            self._v_box_five.add(img)
            s += 1

        self._gird_buts = layout.UIGridLayout(column_count=col, row_count=row, horizontal_spacing=15, vertical_spacing=15)
        active_buts = [0, 1, 2, 3, 4]

        class MyButton(buttons.UITextureButton):
            num = 0
            deactive = True
            radius = 25
            deactive_color = (0, 0, 0, 100)

            def on_click(self2, event: UIOnClickEvent):
                try:
                    def new_but_state(state):
                        for but1 in self._gird_buts.children:
                            if but1.num == active_buts[self._nomer_sposob]:
                                but1.deactive = state
                                break
                    new_but_state(True)
                    self.igrpk.five_sposobs[self._nomer_sposob] = self.igrpk.osn_sposobs[self2.num]
                    active_buts[self._nomer_sposob] = self2.num
                    self2.deactive = False
                    new_but_state(False)
                except:
                    return
                child_list = []
                for child in self._v_box_five.children:
                    child_list.append(child)
                self._v_box_five.clear()
                img = image.UIImage(texture=texture_but_list[self2.num])
                child_list[self._nomer_sposob] = img
                circles.set_sposob(self._nomer_sposob, self.igrpk.five_sposobs[self._nomer_sposob], texture_but_list[self2.num])
                for child in child_list:
                    self._v_box_five.add(child)

        button_list = []
        texture_but_list = instruments.TextureList()
        texture_but_list.load_textures(col * row, "resources/sposob", PNG, False)
        s = 0
        for texture in texture_but_list:
            but = MyButton(texture=texture)
            but.num = s
            if s in active_buts:
                but.deactive = False
            s += 1
            button_list.append(but)
        s = 0
        for r in range(row):
            for c in range(col):
                self._gird_buts.add(button_list[s], row_num=r, col_num=c)
                s += 1

        v_box = arcade.gui.UIBoxLayout(space_between=100, vertical=False)
        v_box.add(self._gird_buts)
        v_box.add(self._v_box_five)
        self.ui_anchor_layuot.add(v_box, anchor_x='center', anchor_y='center')
        # self.ui_anchor_layuot.add(self._gird_buts, anchor_x='center', anchor_y='center')
        # self.ui_anchor_layuot.add(self._v_box_five, anchor_x='center', anchor_y='center', align_x=self.window.width / 5)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.KEY_1:
                self._nomer_sposob = 0
            case arcade.key.NUM_1:
                self._nomer_sposob = 0
            case arcade.key.KEY_2:
                self._nomer_sposob = 1
            case arcade.key.NUM_2:
                self._nomer_sposob = 1
            case arcade.key.KEY_3:
                self._nomer_sposob = 2
            case arcade.key.NUM_3:
                self._nomer_sposob = 2
            case arcade.key.KEY_4:
                self._nomer_sposob = 3
            case arcade.key.NUM_4:
                self._nomer_sposob = 3
            case arcade.key.KEY_5:
                self._nomer_sposob = 4
            case arcade.key.NUM_5:
                self._nomer_sposob = 4

        if symbol == arcade.key.G:
            if not self.kd:
                self.active = not self.active

                if self.active:
                    self.window.set_update_rate(self.update_rate)
                else:
                    self.kd = True
                    self.window.set_update_rate(1/60)
                    self.__s_active = 0

    def enable(self) -> None:
        self.__s_active += 1
        if self.__s_active >= self.__timer_for_s_active:
            self.window.set_update_rate(1 / 60)
            self.active = False
            self.kd = True
            self.__s_active = 0

        if not self._enabled:
            self._enabled = True
            self.window.push_handlers(
                self.on_resize,
                self.on_update,
                self.on_mouse_drag,
                self.on_mouse_motion,
                self.on_mouse_press,
                self.on_mouse_release,
                self.on_mouse_scroll,
                self.on_key_release,
                self.on_text,
                self.on_text_motion,
                self.on_text_motion_select,
            )
        else:
            for child in self._gird_buts.children:
                if child.deactive:
                    arcade.draw_circle_filled(child.center_x, child.center_y, child.radius, child.deactive_color)

    def disable(self) -> None:
        if self.kd:
            self.__s_kd += 1
            if self.__s_kd >= self.__timer_for_s_kd:
                self.kd = False
                self.__s_kd = 0

        if self._enabled:
            self._enabled = False
            self.window.remove_handlers(
                self.on_resize,
                self.on_update,
                self.on_mouse_drag,
                self.on_mouse_motion,
                self.on_mouse_press,
                self.on_mouse_release,
                self.on_mouse_scroll,
                self.on_key_press,
                self.on_key_release,
                self.on_text,
                self.on_text_motion,
                self.on_text_motion_select,
            )


