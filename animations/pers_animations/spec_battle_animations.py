import instruments
from instruments import PNG
from interaction_sprites import battles
import animations
from interaction_sprites.battles import mobs
from animations.pers_animations import WALK, IDLE, BEG, SBIV
from animations import pers_animations
import arcade


class OyuunAnimations(pers_animations.BattleAnimations):
    def __init__(self, pers: battles.VodaPers):
        super().__init__(pers)
        main_patch = 'resources/Pers_animations/battle/Oyuun/'
        #self.idle_texture = arcade.load_texture_pair(f'{main_patch}_idle.png')
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle/0.png')
        self.slovar_animation[IDLE][1] = 7
        self.slovar_animation[IDLE][2] = 0.05
        self.slovar_animation[IDLE][3].load_textures(8, f'{main_patch}idle/', PNG)
        self.slovar_animation[BEG][1] = 7
        self.slovar_animation[BEG][3].load_textures(8, f'{main_patch}beg/', PNG)
        self.sprite.texture = self.idle_texture[0]
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}jump_fall/jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}jump_fall/j.png')
        self.block_texture = arcade.load_texture_pair(f'{main_patch}jump_fall/oyuun_fall.png')
        self.udar_texture = arcade.load_texture_pair(f'{main_patch}master/udar0.png')

        self.slovar_animation[WALK][1] = 7
        self.slovar_animation[WALK][3].load_textures(8, f'{main_patch}walk/', PNG)
        self.dialog_textures.load_textures(3, f'{main_patch}oyuun_dialog', PNG)

        self.sprite: battles.VodaPers
        udar_main_patch = f'{main_patch}master/udar'
        self.sprite.udar.idle_udar_texture_list.load_textures(2, udar_main_patch, PNG)
        self.sprite.udar.jump_udar_texture_list.load_textures(2, udar_main_patch + '_W', PNG)
        self.sprite.udar.jump_dvizh_udar_texture_list.load_textures(2, udar_main_patch + '_WAD', PNG)
        self.sprite.udar.move_udar_texture_list.load_textures(2, udar_main_patch + '_move', PNG)

        self.razminka = False
        self.razminka_textures = instruments.TextureList()
        self.s_razminka_texture = 0
        self.razminka_textures.load_textures(12, f'{main_patch}Razminka/razminka', PNG)

        self.concentration = False
        self.concentration_textures = instruments.TextureList()
        self.s_concentration_texture = 0
        self.concentration_textures.load_textures(15, f'{main_patch}Concentration/concentration', PNG)

        self.wasu = False
        self.s_wasu = 0
        self.max_s_wasu = 340

        self.chest = False
        self.read = False
        self.gotov = False

    def razminka_animation(self):
        self.s_razminka_texture += 0.08
        if self.s_razminka_texture > 12:
            self.s_razminka_texture = 0
            self.razminka = False
            return
        self._update_texture_and_hitbox(self.razminka_textures[int(self.s_razminka_texture)])

    def concentration_animation(self):
        self.s_concentration_texture += 0.05
        if self.s_concentration_texture > 15:
            self.s_concentration_texture = 0
            self.concentration = False
            #self.action(sposobs.VODA_UDARS)
            return
        self._update_texture_and_hitbox(self.concentration_textures[int(self.s_concentration_texture)])

    def write_and_stand_up_animation(self):
        self.s_wasu += 1
        if self.s_wasu >= self.max_s_wasu:
            self.wasu = False
            self.s_wasu = 0

    def chest_animation(self):
        if self.chest:
            self._update_texture_and_hitbox(self.jump_texture[self.sprite.storona])
            self.tipo_return = True

    def read_animation(self):
        if self.read:
            self._update_texture_and_hitbox(self.slovar_animation[WALK][3][2][self.sprite.storona])
            self.tipo_return = True

    def gotov_animation(self):
        if self.gotov:
            self._update_texture_and_hitbox(self.fall_texture[self.sprite.storona])
            self.tipo_return = True

    def ispit(self):
        self._update_texture_and_hitbox(self.idle_texture[self.sprite.storona])


class BetaOyuunAnimations(pers_animations.BattleAnimations):
    def __init__(self, pers):
        super().__init__(pers)
        main_patch = 'nuzhno/Oyuun/maleAdventurer'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}_idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}_jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}_fall.png')
        self.block_texture = arcade.load_texture_pair('nuzhno/Oyuun/maleAdventurer_jump.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/Oyuun/master/udar0.png')

        self.slovar_animation[WALK][1] = 7
        self.slovar_animation[WALK][3].load_textures(8, f'{main_patch}_walk', PNG)
        self.dialog_textures.load_textures(3, f'{main_patch}_dialog', PNG)

        self.sprite.texture = self.idle_texture[0]


class BalvanchikAnimations(pers_animations.BattleAnimations):
    def __init__(self, pers: mobs.Vrag):
        super().__init__(pers)
        main_patch = self.main_patch + 'male_adventurer/maleAdventurer_'

        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')
        self.sprite.texture = self.idle_texture[0]

        self.slovar_animation[WALK][1] = 7
        self.slovar_animation[WALK][3].load_textures(8, f'{main_patch}walk', PNG)

        self.slovar_animation[BEG][1] = 3
        self.slovar_animation[BEG][3].load_textures(4, f'{main_patch}beg', PNG)

        self.slovar_animation[SBIV][1] = 1
        texture = arcade.load_texture_pair(f'{main_patch}sbiv.png')
        self.slovar_animation[SBIV][3].append(texture)
        texture = arcade.load_texture_pair(f'{main_patch}sbiv.png')
        self.slovar_animation[SBIV][3].append(texture)

        self.jump_texture = arcade.load_texture_pair(f'{main_patch}jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}fall.png')

        self.udar_texture = arcade.load_texture_pair(f'{main_patch}udar.png')


