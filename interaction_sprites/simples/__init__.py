from typing import Any

import arcade

import interaction_sprites
import animations.pers_animations


class ToggleSprite(interaction_sprites.InteractionSprite):
    def __init__(self, name: str, patch_texture_enable, patch_texture_disable):
        super().__init__()
        self.name = name
        texture_enable = arcade.load_texture(patch_texture_enable)
        texture_disable = arcade.load_texture(patch_texture_disable)
        self.animations = animations.pers_animations.ToggleAnimation(self, texture_enable, texture_disable)


class SimpleSprite(interaction_sprites.DvizhInteractionSprite, interaction_sprites.DialogSprite):
    def __init__(self, name: str):
        super().__init__()
        self.animations: animations.pers_animations.BaseAnimations or Any = None
        self.name = name

    def update_base_animations(self):
        self.animations.tipo_return = False
        self._update_storona(self.change_x)

        self.animations.idle_animation(self.change_x, self.change_y)
        if self.animations.tipo_return:
            return
        self.animations.walk_animation(self.change_x)




