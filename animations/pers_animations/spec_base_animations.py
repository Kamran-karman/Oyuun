import instruments
from instruments import PNG
from interaction_sprites import simples
from animations import pers_animations
from animations.pers_animations import WALK
import arcade


class GonecAnimations(pers_animations.BaseAnimations):
    def __init__(self, sprite: simples.SimpleSprite):
        super().__init__(sprite)
        main_patch = 'resources/Pers_animations/base/male_person/malePerson_'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')

        self.slovar_animation[WALK][3].load_textures(8, f'{main_patch}walk', PNG)
        self.slovar_animation[WALK][1] = 7
        self.slovar_animation[WALK][2] = 0.2
        self.sprite.texture = self.idle_texture[1]

        self.dialog_textures.load_textures(3, f'{main_patch}dialog', PNG)

        self.s = 0
        self.anim = False

    def animation_1(self):
        if self.anim:
            self.s += 1
            if self.s >= 60:
                self.s = 0
                self.anim = False


class RinTeoAnimations(pers_animations.BaseAnimations):
    def __init__(self, sprite: simples.SimpleSprite):
        super().__init__(sprite)
        self.main_patch = f"{self.main_patch}rin_teo/"

        self.idle_texture = arcade.load_texture_pair(f"{self.main_patch}idle.png")

        self.dialog_textures.load_textures(3, f"{self.main_patch}dialog", PNG)

        self.slovar_animation[WALK][3].load_textures(8, f'{self.main_patch}walk', PNG)
        self.slovar_animation[WALK][1] = 7
        self.slovar_animation[WALK][2] = 0.2


class BratislavAnimations(pers_animations.BaseAnimations):
    def __init__(self, sprite: simples.SimpleSprite):
        super().__init__(sprite)
        main_patch = f'{self.main_patch}male_person/malePerson_'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')

        self.dialog_textures.load_textures(3, f'{main_patch}dialog', PNG)
        self.slovar_animation[WALK][3].load_textures(8, f'{main_patch}walk', PNG)

        self.slovar_animation[WALK][1] = 7
        self.slovar_animation[WALK][2] = 0.2

        self.chest_texture = arcade.load_texture_pair(f'{main_patch}jump.png')

        self.priziv_list = instruments.TextureList()
        self.s_priziv_list = 0
        texture = arcade.load_texture_pair(f'{main_patch}walk3.png')
        self.priziv_list.append(texture)
        texture = arcade.load_texture_pair(f'{main_patch}anim_2.png')
        self.priziv_list.append(texture)

        self.chest = False
        self.priziv = False
        self.s_priziv = 0

    def priziv_animation(self):
        if self.priziv:
            self.s_priziv += 1
            if self.s_priziv >= 120 and self.s_priziv_list == 0:
                self.s_priziv_list += 1
                self.sprite.rock = True
            self._update_texture_and_hitbox(self.priziv_list[self.s_priziv_list][self.sprite.storona])
            if self.s_priziv == 210:
                self.priziv = False
                self.s_priziv = 0
                self.s_priziv_list = 0
            self.tipo_return = True

    def chest_animation(self):
        if self.chest:
            self._update_texture_and_hitbox(self.chest_texture[self.sprite.storona])
            self.tipo_return = True


class RockAnimations:
    def __init__(self, sprite):
        self.sprite = sprite
        
        self.sprite.texture = arcade.load_texture('resources/Pers_animations/base/Rock/rock.png')
        self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        self.tresk = False
        self.tresk_texture_list = instruments.TextureList()
        self.s_tresk = 0
        self.tresk_texture_list.load_textures(10, 'resources/Pers_animations/base/Rock/rock', PNG, False)
        
    def tresk_animation(self):
        if self.sprite.max_hp - 825 < self.sprite.hp <= self.sprite.max_hp - 450 and self.s_tresk == 0:
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        elif self.sprite.hp <= self.sprite.max_hp - 625 and self.s_tresk == 0:
            self.s_tresk += 1
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        elif self.sprite.hp <= self.sprite.max_hp - 2125 and self.s_tresk == 1:
            self.s_tresk += 1
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        elif self.sprite.hp <= self.sprite.max_hp - 2425 and self.s_tresk == 2:
            self.s_tresk += 1
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        elif self.sprite.hp <= self.sprite.max_hp - 2925 and self.s_tresk == 3:
            self.s_tresk += 1
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        elif self.sprite.hp <= self.sprite.max_hp - 3250 and self.s_tresk == 4:
            self.s_tresk += 1
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        elif self.sprite.hp <= self.sprite.max_hp - 3500 and self.s_tresk == 5:
            self.s_tresk += 1
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        elif self.sprite.hp <= self.sprite.max_hp - 4000 and self.s_tresk == 6:
            self.s_tresk += 1
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        elif self.sprite.hp <= self.sprite.max_hp - 4500 and self.s_tresk == 7:
            self.s_tresk += 1
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points
        elif self.sprite.hp <= self.sprite.max_hp - 4900 and self.s_tresk == 8:
            self.s_tresk += 1
            self.sprite.texture = self.tresk_texture_list[self.s_tresk]
            self.sprite.hit_box._points = self.sprite.texture.hit_box_points



