from interaction_sprites import battles
from sposobs import dvizh
from interaction_sprites import simples
from animations.pers_animations import spec_base_animations, spec_plus_animations
import arcade


class Gonec(simples.SimpleSprite):
    def __init__(self):
        super().__init__('Gonec')
        self.animations = spec_base_animations.GonecAnimations(self)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_base_animations()


class AdnotBratislav(simples.SimpleSprite):
    def __init__(self):
        super().__init__('Bratislav')
        self.rock = False
        self.animations = spec_base_animations.BratislavAnimations(self)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.animations.tipo_return = False

        self.animations.chest_animation()
        if self.animations.tipo_return:
            return

        self.animations.priziv_animation()
        if self.animations.tipo_return:
            return

        self.update_base_animations()

class RinTeo(simples.SimpleSprite):
    def __init__(self):
        super().__init__("Rin")
        self.animations = spec_base_animations.RinTeoAnimations(self)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_base_animations()


class Sinhelm(simples.SimpleSprite):
    def __init__(self):
        super().__init__('Sinhelm')
        self.olen_beg = False

        self.force_list = [50000, 60000, 10000, 10000]
        self.visota = 2250
        self.s = 0
        self.dvizh = dvizh.DvizhPers(self, arcade.SpriteList())

        self.not_fizik = True
        self.is_on_ground = True

        self.animations = spec_plus_animations.SinhekmAnimations(self)

        self.storona = 1

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.animations.tipo_return = False
        self._update_storona(dx, battles.X_D_ZONE)

        self.dvizh.update_storona_pers()
        self.is_on_ground = physics_engine.is_on_ground(self)

        if self.olen_beg:
            if self.center_y <= self.visota and self.s == 0:
                self.s = 1
                physics_engine.apply_force(self, (self.force_list[0] * self.dvizh.storona, self.force_list[1]))
            elif self.center_y <= self.visota and self.s == 1:
                physics_engine.apply_force(self, (self.force_list[2] * self.dvizh.storona, self.force_list[3]))
            elif self.center_y > self.visota:
                self.s = 0

        self.animations.landing_animations()
        if self.animations.tipo_return:
            return
        self.animations.podgotovka_animations()
        if self.animations.tipo_return:
            return

        self.animations.jump_and_fall_animation(dy, self.is_on_ground, battles.Y_D_ZONE)
        if self.animations.tipo_return:
            return
        self.animations.base_animations(dx, battles.X_D_ZONE)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.animations.tipo_return = False
        self.animations.ukaz_animation()
        if self.animations.tipo_return:
            return

        self.animations.base_animations(self.change_x)


