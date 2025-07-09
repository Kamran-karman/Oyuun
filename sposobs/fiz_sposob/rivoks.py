import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import hit_box_and_radius
import sposobs
from sposobs import fiz_sposob, dvizh


class Rivoks(dvizh.DvizhPers):
    def __init__(self, pers, sprite_list, timer_for_s_dvizh=0, vel=(0, 0), igrok=False):
        super().__init__(pers, sprite_list, vel, timer_for_s_dvizh, igrok)
        self.klass = sposobs.RIVOKS

        self.radius_stop = hit_box_and_radius.KvadratRadius()

        self.levo = 0
        self.pravo = 0

    def timer_kd(self):
        if self.action:
            self.update_storona()
            self.pers.stan_for_sposob = True
            self.s_kd += 1
            if self.s_kd >= self.timer_for_s_kd:
                self.action = False
                self.pers.stan_for_sposob = False
                self.dvizh_pers_func()

    def updadte_stop(self):
        self.radius_stop.position = self.pers.position

        if not self.igrok:
            if not self.pers.s_kast_scena:
                if self.pers.radius_vid.check_collision(self.pers.igrok):
                    if self.pers.igrok.center_x > self.pers.radius_vid.center_x:
                        if self.levo <= abs(self.pers.igrok.left - self.pers.right) <= self.pravo:
                            if self.s_kd < self.timer_for_s_kd:
                                self.action = True
                        else:
                            if self.s_kd < self.timer_for_s_kd - self.timer_for_s_kd / 5:
                                self.action = False
                                self.s_kd = 0
                                self.pers.stan_for_sposob = False
                    elif self.pers.igrok.center_x < self.pers.radius_vid.center_x:
                        if self.levo <= abs(self.pers.igrok.right - self.pers.left) <= self.pravo:
                            if self.s_kd < self.timer_for_s_kd:
                                self.action = True
                        else:
                            if self.s_kd < self.timer_for_s_kd - 30:
                                self.action = False
                                self.s_kd = 0
                                self.pers.stan_for_sposob = False

                for drug in self.pers.v_drug_list:
                    if drug != self.pers and not drug.smert:
                        if (self.radius_stop.check_collision(drug.kvadrat_radius) and
                                abs(self.radius_stop.center_x - self.pers.igrok.center_x) >
                                abs(drug.center_x - self.pers.igrok.center_x)):
                            self.stop_dvizh = True
                            self.s_kd = 0

                if self.radius_stop.check_collision(self.pers.igrok) and self.dvizh:
                    self.stop_dvizh = True
                    self.s_kd = 0
        else:
            if self.radius_stop.check_collision(sprite_list=self.pers.sprite_list):
                self.stop_dvizh = True
                self.action = False
                self.s_kd = 0
                self.pers.stan_for_sposob = False


class Rivok(fiz_sposob.FizSposobFight, Rivoks):
    def __init__(self, pers, sprite_list, vel, timer_for_s=30, timer_for_s_kd=60, timer_for_s_dvizh=60,
                 igrok=False):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.dvizh_vel = vel
        self.igrok = igrok
        self.sposob = sposobs.RIVOK

        self.dvizh_force = (10000, 0)

        self.levo = 400
        self.pravo = 800

        self.timer_for_s = timer_for_s
        self.timer_for_s_kd = timer_for_s_kd
        self.timer_for_s_dvizh = timer_for_s_dvizh

        self.minus_stamina = 3

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if not self.pers.smert and not self.pers.oglush:

            self.radius_stop.position = self.pers.position

            self.timer_kd()

            if self.dvizh:
                if self.s_dvizh == 1:
                    self.func_stamina()
                    if not self.stamina:
                        self.s_kd = 0
                        self.pers.stan_for_sposob = False
                        self.stop_dvizh = True
                        self.s_dvizh += self.timer_for_s_dvizh
                        return
                    else:
                        self.pers.stamina -= self.minus_stamina
                if self.s_dvizh >= self.timer_for_s_dvizh:
                    self.s_kd = 0
            elif not self.dvizh and self.s_kd >= self.timer_for_s_kd:
                self.s_kd = 0

            self.updadte_stop()
        elif self.pers.smert or self.pers.oglush:
            if self.dvizh:
                self.stop_dvizh = True
            self.action = False
            self.s_kd = 0

        self.update_dvizh_pers()
