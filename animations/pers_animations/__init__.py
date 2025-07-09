import arcade
import interaction_sprites
from interaction_sprites import battles
import instruments
import animations

WALK = 'walk'
IDLE = 'idle'
BEG = 'beg'
SBIV = 'sbiv'
VSTAT = 'vstat'


class ToggleAnimation:
    def __init__(self, sprite: interaction_sprites.InteractionSprite, texture_enable: arcade.Texture,
                 texture_disable: arcade.Texture):
        self.main_patch = 'resources/Pers_animations/'

        self.sprite = sprite
        self.texture_pair = (texture_enable, texture_disable)
        self.sprite.texture = self.texture_pair[0]

    def animation(self, action):
        if action:
            self.sprite.texture = self.texture_pair[0]
        else:
            self.sprite.texture = self.texture_pair[1]


class BaseAnimations(animations.Animations):
    def __init__(self, sprite: interaction_sprites.DvizhInteractionSprite):
        super().__init__(sprite)
        self.main_patch = 'resources/Pers_animations/base/'

        self.dialog_textures = instruments.TextureList()
        self.idle_texture = None
        self.tipo_return = False

        self.slovar_animation.update({WALK: [0, 0, 0, instruments.TextureList()],
                                      IDLE: [0, 0, 0, instruments.TextureList()]})

    def idle_animation(self, speed_x, x_d_zone=0):
        if abs(speed_x) <= x_d_zone:
            self.slovar_animation[WALK][0] = 0
            if len(self.slovar_animation[IDLE][3]) == 0:
                self._update_texture_and_hitbox(self.idle_texture[self.sprite.storona])
            else:
                self.slovar_animation[IDLE][0] += self.slovar_animation[IDLE][2]
                if self.slovar_animation[IDLE][0] > self.slovar_animation[IDLE][1]:
                    self.slovar_animation[IDLE][0] = 0
                self._update_texture_and_hitbox(
                    self.slovar_animation[IDLE][3][int(self.slovar_animation[IDLE][0])][self.sprite.storona])
            self.tipo_return = True

    def walk_animation(self, speed_x, x_d_zone: float = 0, odometr=False):
        if abs(speed_x) > x_d_zone:
            if odometr:
                self.sprite: battles.BattleSprite
                self.sprite.fizika.x_odometr = 0
                self.slovar_animation[WALK][2] = 1 / 4
            self.slovar_animation[WALK][0] += self.slovar_animation[WALK][2]
            if self.slovar_animation[WALK][0] > self.slovar_animation[WALK][1]:
                self.slovar_animation[WALK][0] = 0
            self._update_texture_and_hitbox(self.slovar_animation[WALK][3][int(self.slovar_animation[WALK][0])]
                                            [self.sprite.storona])


class AnimationsPlus(BaseAnimations):
    def __init__(self, sprite: interaction_sprites.DvizhInteractionSprite):
        super().__init__(sprite)
        self.jump_texture = None
        self.fall_texture = None

        self.main_patch = 'resources/Pers_animations/plus/'

        self.in_air = False

        self.slovar_animation.update({BEG: [0, 0, 0, instruments.TextureList()]})

    def jump_and_fall_animation(self, speed_y, is_on_ground, y_d_zone=0):
        if not is_on_ground:
            if speed_y > y_d_zone:
                self.slovar_animation[WALK][0] = 0
                self._update_texture_and_hitbox(self.jump_texture[self.sprite.storona])
                self.tipo_return = True
            elif speed_y < -y_d_zone:
                self.slovar_animation[WALK][0] = 0
                self._update_texture_and_hitbox(self.fall_texture[self.sprite.storona])
                self.tipo_return = True
            self.tipo_return = True

    def base_animations(self, speed_x, x_d_zone=0, x_odometr=0, max_x_odometr: float = 0):
        self.idle_animation(speed_x, x_d_zone)
        if self.tipo_return:
            return
        self.sprite: battles.BattlePers
        if max_x_odometr == 0:
            self.walk_animation(speed_x, x_d_zone)
        else:
            self.walk_animation(x_odometr, max_x_odometr, True)

    def beg_animatioon(self, speed_x, x_d_zone: float = 0, odometr=False):
        if abs(speed_x) > x_d_zone and self.sprite.beg:
            self.tipo_return = True
            if odometr:
                self.sprite: battles.BattleSprite
                self.sprite.fizika.x_odometr = 0
                self.slovar_animation[BEG][2] = 1 / 4
            self.slovar_animation[BEG][0] += self.slovar_animation[BEG][2]
            if self.slovar_animation[BEG][0] > self.slovar_animation[BEG][1]:
                self.slovar_animation[BEG][0] = 0
            self._update_texture_and_hitbox(self.slovar_animation[BEG][3][int(self.slovar_animation[BEG][0])]
                                            [self.sprite.storona])


class BattleAnimations(AnimationsPlus):
    def __init__(self, sprite: battles.BattlePers):
        super().__init__(sprite)
        self.udar_texture = None
        self.block_texture = None
        self.udaren_texture = None

        self.main_patch = 'resources/Pers_animations/battle/'

        self.slovar_animation.update({SBIV: [0, 0, 0, instruments.TextureList()],
                                      VSTAT: [0, 0, 0, instruments.TextureList()]})

        self.vstat = False

    def plus_animations(self, speed_x, speed_y, can_jump, x_d_zone, y_d_zone, x_odometr=0, max_x_odometr: float = 0):
        self.tipo_return = False
        if not self.sprite.walk:
            y_d_zone /= 1000
            self.sprite: battles.BattlePers
        self.jump_and_fall_animation(speed_y, can_jump, y_d_zone)
        if self.tipo_return:
            return
        if max_x_odometr == 0:
            self.beg_animatioon(speed_x, x_d_zone)
        else:
            self.beg_animatioon(x_odometr, max_x_odometr, True)
        if self.tipo_return:
            return
        self.base_animations(speed_x, x_d_zone, x_odometr, max_x_odometr)

    def udar_animations(self):
        self.sprite: battles.BattlePers
        if self.sprite.udar.action:
            self._update_texture_and_hitbox(self.udar_texture[self.sprite.storona])
            self.tipo_return = True

    def udaren_animation(self):
        self.sprite: battles.BattlePers
        if self.sprite.udaren:
            self._update_texture_and_hitbox(self.udaren_texture[self.sprite.storona])
            self.tipo_return = True

    def block_animation(self):
        self.sprite: battles.BattlePers
        if self.sprite.block.block and self.sprite.udar.main_block:
            self._update_texture_and_hitbox(self.block_texture[self.sprite.storona])
            self.tipo_return = True

    def sbiv_animation(self):
        self.sprite: battles.BattlePers
        if self.sprite.sbiv:
            if not self.sprite.oglush:
                self.sprite.sbiv = False
                self.sprite.fizika.update_poly = True
                return
            self.tipo_return = True
            self.slovar_animation[SBIV][0] += self.slovar_animation[SBIV][2]
            if self.slovar_animation[SBIV][0] >= self.slovar_animation[SBIV][1]:
                self.slovar_animation[SBIV][0] = 0  # self.slovar_animation[SBIV][1]
            self._update_texture_and_hitbox(self.slovar_animation[SBIV][3][int(self.slovar_animation[SBIV][0])]
                                            [self.sprite.storona])

    def vstat_animation(self):
        if self.vstat:
            self.slovar_animation[VSTAT][0] += self.slovar_animation[VSTAT][2]
            self._update_texture_and_hitbox(self.slovar_animation[VSTAT][3][int(self.slovar_animation[VSTAT][0])]
                                            [self.sprite.storona])
            self.tipo_return = True
            if self.slovar_animation[VSTAT][0] >= self.slovar_animation[VSTAT][1]:
                self.vstat = False
                self.slovar_animation[VSTAT][0] = 0

    def smert_animation(self):
        self.sprite: battles.BattlePers
        if self.sprite.smert:
            pass

