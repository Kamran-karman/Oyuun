from interaction_sprites import simples
import animations
from instruments import PNG
from animations.pers_animations import WALK, BEG
import sposobs
import arcade


class SinhekmAnimations(animations.pers_animations.AnimationsPlus):
    def __init__(self, sprite: simples.SimpleSprite):
        super().__init__(sprite)
        self.landing = False
        self.s_landing = 0
        self.timer_for_s_landing = 30
        self.podgotovka = False
        self.s_podgotovka = 0
        self.timer_for_s_podgotovka = 120
        self.ukaz = False
        self.s_ukaz = 0

        main_patch = 'resources/Pers_animations/plus/Sinhelm/sinhelm_'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')
        self.ukaz_texture = arcade.load_texture_pair(f'{main_patch}ukaz.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}fall.png')
        self.landing_texture = arcade.load_texture_pair(f'{main_patch}landing.png')
        self.podgotovka_texture = arcade.load_texture_pair(f'{main_patch}podgotovka.png')
        self.sprite.texture = self.idle_texture[self.sprite.storona]

        self.slovar_animation[WALK][3].load_textures(8, f'{main_patch}walk', PNG)
        self.slovar_animation[WALK][1] = 7
        self.slovar_animation[WALK][2] = 0.2
        self.dialog_textures.load_textures(3, f'{main_patch}dialog', PNG)

    def landing_animations(self):
        # if not self.landing and not self.sprite.is_on_ground:
        #     self.landing = True

        if self.landing:
            if self.s_landing <= self.timer_for_s_landing:
                self.tipo_return = True
                self._update_texture_and_hitbox(self.landing_texture[self.sprite.storona])
                self.s_landing += 1
            else:
                self.landing = False
                self.s_landing = 0

    def ukaz_animation(self):
        if self.ukaz:
            self.tipo_return = True
            self.s_ukaz += 1
            if self.s_ukaz >= 15:
                self.ukaz = False
                self.s_ukaz = 0
            self._update_texture_and_hitbox(self.ukaz_texture[self.sprite.storona])

    def podgotovka_animations(self):
        if self.podgotovka:
            if self.s_podgotovka <= self.timer_for_s_podgotovka:
                self.s_podgotovka += 1
                self._update_texture_and_hitbox(self.podgotovka_texture[self.sprite.storona])
                self.tipo_return = True
            else:
                self.podgotovka = False
                self.s_podgotovka = 0


class FirstAnimations(animations.pers_animations.AnimationsPlus):
    def __init__(self, sprite):
        super().__init__(sprite)

        main_patch = self.main_patch + 'First/maleAdventurer_'

        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')
        self.sprite.texture = self.idle_texture[0]

        self.slovar_animation[WALK][1] = 7
        self.slovar_animation[WALK][3].load_textures(8, f'{main_patch}walk', PNG)

        self.slovar_animation[BEG][1] = 3
        self.slovar_animation[BEG][3].load_textures(4, f'{main_patch}beg', PNG)

        self.jump_texture = arcade.load_texture_pair(f'{main_patch}jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}fall.png')

        self.poiman_texture = arcade.load_texture_pair(f"{main_patch}poiman.png")
        self.poiman = False

        self.poiman_udaren_texture = arcade.load_texture_pair(f"{main_patch}udaren.png")
        self.poiman_udar = False
        self.s_pu = 0
        self.timer_for_s_pu = 60

        self.ataka_texture = arcade.load_texture_pair(f"{main_patch}ataka.png")
        self.ataka = False
        self.s_ataka = 0
        self.timer_for_s_ataka = 30

    def poiman_animation(self):
        if self.poiman:
            self.sprite.texture = self.poiman_texture[self.sprite.storona]
            self.tipo_return = True

    def poiman_udaren_animation(self):
        if self.poiman_udar:
            self.s_pu += 1
            if self.s_pu >= self.timer_for_s_pu:
                self.s_pu = 0
                self.poiman_udar = False
                return
            self.sprite.texture = self.poiman_udaren_texture[self.sprite.storona]
            self.tipo_return = True
            self.poiman = False

    def ataka_animations(self):
        if self.ataka:
            self.s_ataka += 1
            if self.s_ataka >= self.timer_for_s_ataka:
                self.s_ataka = 0
                self.ataka = False

            self.sprite.texture = self.ataka_texture[1]
            self.tipo_return = True
