# -*- coding: latin-1 -*-
import random as rdm
import numpy as np

NBR_X = 50
NBR_Y = 50
TAILLE_CELLULE = 10


class Simulation:

    def __init__(self):
        self.tour = 0
        self.sain = NBR_X * NBR_Y
        self.malade = 0
        self.mort = 0
        self.guerie = 0
        self.vaccin = 0
        self.r0 = 0.0

        self.etat = np.zeros((NBR_Y, NBR_X), dtype=np.int_)
        self.masque = np.zeros((NBR_Y, NBR_X), dtype=np.bool_)
        self.temps = np.zeros((NBR_Y, NBR_X), dtype=np.int_)

    def propagation(self, infec_value, leta_value, infec_mode, infec_min, infec_max, guer_mode, guer_min, guer_max, masque_value, voyage_value,
                    conf_mode, conf_force, conf_respect, vacc_value, vacc_mode, vacc_comm, masq_mode, masq_comm):
        """Calcul le tour n+1 de la matrice état"""
        matrice_memoire = self.etat.copy()
        nouveau_malade, voyage = 0, 0
        for y in range(NBR_Y):
            for x in range(NBR_X):
                if matrice_memoire[y][x] == 0:
                    if self.infecte(x, y, infec_value, masque_value, conf_mode, conf_force, conf_respect) >= rdm.randint(1, 100):
                        self.etat[y][x], self.temps[y][x] = 1, rdm.randint(infec_min, infec_max)
                        nouveau_malade += 1
                    elif vacc_mode and vacc_comm >= rdm.randint(1, 5000):
                        self.etat[y][x] = 4

                elif matrice_memoire[y][x] == 4:
                    coeff = (100 - vacc_value) / 100
                    if int(self.infecte(x, y, infec_value, masque_value, conf_mode, conf_force, conf_respect) * coeff) >= rdm.randint(1, 100):
                        self.etat[y][x], self.temps[y][x] = 1, rdm.randint(infec_min, infec_max)
                        nouveau_malade += 1

                elif matrice_memoire[y][x] == 1:
                    if voyage_value >= rdm.randint(1, 100):
                        voyage += 1
                    if infec_mode:  # si infini
                        if leta_value >= rdm.randint(1, 5000):
                            self.etat[y][x], self.masque[y][x] = 3, False
                    elif self.temps[y][x] == 0:
                        if leta_value >= rdm.randint(1, 100):
                            self.etat[y][x], self.masque[y][x] = 3, False
                        else:
                            self.temps[y][x] = rdm.randint(guer_min, guer_max)
                            if self.temps[y][x] == 0:
                                self.etat[y][x] = 0
                            else:
                                self.etat[y][x] = 2
                    else:
                        self.temps[y][x] -= 1

                elif matrice_memoire[y][x] == 2 and not guer_mode:
                    if self.temps[y][x] == 0:
                        self.etat[y][x] = 0
                    else:
                        self.temps[y][x] -= 1

                if masq_mode and not self.masque[y][x] and masq_comm >= rdm.randint(1, 100*(101-masq_comm)):
                    self.masque[y][x] = True

        if self.malade == 0 or infec_mode:
            self.r0 = 0.0
        else:
            self.r0 = (nouveau_malade / self.malade) * ((infec_min + infec_max) / 2)

        for k in range(voyage):
            y, x = rdm.randint(0, NBR_Y - 1), rdm.randint(0, NBR_X - 1)
            if self.etat[y][x] == 0 and infec_value // 5 >= rdm.randint(1, 100):
                self.etat[y][x], self.temps[y][x] = 1, rdm.randint(infec_min, infec_max)

    def infecte(self, x, y, infec_value, masque_value, conf_mode, conf_force, conf_respect):
        nb_malade, nb_masque = 0, 0
        """calcul la propabilité pour un individu donné d'etre infecté au prochain tour"""
        for i, j in ((x + i, y + j) for i, j in [(0, -1), (1, 0), (0, 1), (-1, 0)] if (0 <= x + i < NBR_X and 0 <= y + j < NBR_Y)):
            if self.etat[j][i] == 1:
                nb_malade += 15
                if self.masque[j][i] == 1:
                    nb_masque += 15
        if not conf_mode or conf_respect < rdm.randint(1, 100):  # s'il n'y a pas de confinement ou que ce n'est pas recpectee
            for i, j in ((i + x, j + y) for i, j in [(-1, -1), (1, -1), (1, 1), (-1, 1)] if (0 <= x + i < NBR_X and 0 <= y + j < NBR_Y)):
                if self.etat[j][i] == 1:
                    nb_malade += 10
                    if self.masque[j][i] == 1:
                        nb_masque += 10
        return int(((nb_malade - (nb_masque * masque_value // 100)) * infec_value // 100) * (conf_force / 100))

    def temps_init(self, infec_min, infec_max, guer_min, guer_max, ):
        """Lorsqu'on lance la simulation calcul le temps d'infection ou de guerison"""
        for y in range(NBR_Y):
            for x in range(NBR_X):
                if self.etat[y][x] == 1:
                    self.temps[y][x] = rdm.randint(infec_min, infec_max)
                elif self.etat[y][x] == 2:
                    self.temps[y][x] = rdm.randint(guer_min, guer_max)
