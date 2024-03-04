from virus import *
from tkinter import *
import matplotlib.pyplot as plt


class Interface(Tk):
    """Fenetre principale"""

    def __init__(self):
        Tk.__init__(self)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.title("PROPAGATOR")

        self.flag = False
        self.curseur_ligne_premier = ()
        self.curseur_ligne_deuxieme = ()
        self.graphe_x, self.graphe_sain, self.graphe_malade, self.graphe_guerie, self.graphe_mort, self.graphe_vaccin = [], [], [], [], [], []

        self.simulation = Simulation()

        mainframe = Frame(self, height=720, width=1000)
        mainframe.pack_propagate(0)
        mainframe.pack(pady=20)

        cadre1_gauche = Frame(mainframe, height=700, width=550)
        cadre1_gauche.propagate(0)
        cadre1_gauche.pack(side=LEFT)
        cadre1_droit = Frame(mainframe, height=700, width=500)
        cadre1_droit.propagate(0)
        cadre1_droit.pack(side=LEFT)

        cadre2_haut = Frame(cadre1_gauche, height=75, width=550)
        cadre2_haut.propagate(0)
        cadre2_haut.pack(side=TOP)
        cadre_scene = Frame(cadre1_gauche, borderwidth=5, bg='black')
        cadre_scene.pack(side=TOP)
        cadre2_bas = Frame(cadre1_gauche, height=75, width=550)
        cadre2_haut.propagate(0)
        cadre2_bas.pack(side=TOP, pady=20)

        cadre3_centre = Frame(cadre1_droit, height=580, width=400)
        cadre3_centre.propagate(0)
        cadre3_centre.pack(side=TOP)
        cadre3_bas = Frame(cadre1_droit, height=120, width=400)
        cadre3_bas.propagate(0)
        cadre3_bas.pack(side=TOP)

        cadre4_gauche = Frame(cadre3_centre, height=580, width=200)
        cadre4_gauche.propagate(0)
        cadre4_gauche.pack(side=LEFT)
        cadre4_droit = Frame(cadre3_centre, height=580, width=200)
        cadre4_droit.propagate(0)
        cadre4_droit.pack(side=LEFT)

        cadre5_case = LabelFrame(cadre4_gauche, text="Cases", height=230, width=190)
        cadre5_case.propagate(0)
        cadre5_case.pack(side=TOP)
        cadre5_masque = LabelFrame(cadre4_gauche, text="Masque", height=175, width=190)
        cadre5_masque.propagate(0)
        cadre5_masque.pack(side=TOP)
        cadre5_vaccin = LabelFrame(cadre4_gauche, text="Vaccin", height=175, width=190)
        cadre5_vaccin.propagate(0)
        cadre5_vaccin.pack(side=TOP)

        cadre6_propagation = LabelFrame(cadre4_droit, text="Propagation", height=325, width=190)
        cadre6_propagation.propagate(0)
        cadre6_propagation.pack(side=TOP)
        cadre6_confinement = LabelFrame(cadre4_droit, text="Confinement", height=255, width=190)
        cadre6_confinement.propagate(0)
        cadre6_confinement.pack(side=TOP)

        cadre7_graphe = LabelFrame(cadre3_bas, text="Graphe", height=120, width=390)
        cadre7_graphe.propagate(0)
        cadre7_graphe.pack()
        self.scene = Canvas(cadre_scene, height=NBR_Y * TAILLE_CELLULE - 1, width=NBR_X * TAILLE_CELLULE - 1, bd=0, bg='white', cursor="plus")
        self.scene.bind("<Button-1>", self.clique_souris)
        self.scene.bind("<B1-Motion>", self.clique_souris2)
        self.scene.bind("<Motion>", self.ligne)
        self.scene.pack(side=LEFT)

        self.flag_txt = StringVar(value="GO")
        Button(cadre2_haut, text="New", command=self.new, width=5).pack(side=LEFT, padx=30)
        Button(cadre2_haut, textvariable=self.flag_txt, command=self.start_stop, width=5).pack(side=LEFT, padx=5)
        self.vitesse = IntVar(value=100)
        Scale(cadre2_haut, variable=self.vitesse, from_=100, to=1800, label="Vitesse/tour (ms):", orient=HORIZONTAL, length=160, resolution=100,
              tickinterval=500, showvalue=False).pack(side=LEFT, padx=5)

        self.selection_curseur = StringVar(value="carre")

        Radiobutton(cadre2_haut, text="Carre", variable=self.selection_curseur, value="carre", indicatoron=0, width=8,
                    command=self.second_point).pack(side=LEFT)
        Radiobutton(cadre2_haut, text="Surface", variable=self.selection_curseur, value="surface", indicatoron=0, width=8,
                    command=self.second_point).pack(side=LEFT)
        Radiobutton(cadre2_haut, text="Ligne", variable=self.selection_curseur, value="ligne", indicatoron=0, width=8,
                    command=self.second_point).pack(side=LEFT)

        self.compteur_tour = StringVar(value="Tour : " + str(self.simulation.tour))
        Label(cadre2_bas, textvariable=self.compteur_tour).pack(side=LEFT)
        self.compteur_sain = StringVar(value="Sain : " + str(self.simulation.sain))
        Label(cadre2_bas, textvariable=self.compteur_sain).pack(side=LEFT)
        self.compteur_malade = StringVar(value="Malade : " + str(self.simulation.malade))
        Label(cadre2_bas, textvariable=self.compteur_malade).pack(side=LEFT)
        self.compteur_guerie = StringVar(value="Guerie : " + str(self.simulation.guerie))
        Label(cadre2_bas, textvariable=self.compteur_guerie).pack(side=LEFT)
        self.compteur_vaccin = StringVar(value="Vaccin : " + str(self.simulation.vaccin))
        Label(cadre2_bas, textvariable=self.compteur_vaccin).pack(side=LEFT)
        self.compteur_mort = StringVar(value="Mort : " + str(self.simulation.mort))
        Label(cadre2_bas, textvariable=self.compteur_mort).pack(side=LEFT)
        self.compteur_r0 = StringVar(value="R0 : 0.000")
        Label(cadre2_bas, textvariable=self.compteur_r0).pack(side=LEFT)

        self.graphe_bouton = Button(cadre7_graphe, text="Graphe", command=self.graphe, state="normal")
        self.graphe_bouton.place(width=70, x=300, y=35)
        self.graphe_sain_mode = BooleanVar(value=False)
        Checkbutton(cadre7_graphe, text="sain", variable=self.graphe_sain_mode, onvalue=True, offvalue=False, command=self.graphe_option).place(x=5,
                                                                                                                                                y=15)
        self.graphe_malade_mode = BooleanVar(value=True)
        Checkbutton(cadre7_graphe, text="malade", variable=self.graphe_malade_mode, onvalue=True, offvalue=False, command=self.graphe_option).place(
            x=75, y=15)
        self.graphe_guerie_mode = BooleanVar(value=False)
        Checkbutton(cadre7_graphe, text="guerie", variable=self.graphe_guerie_mode, onvalue=True, offvalue=False, command=self.graphe_option).place(
            x=150, y=15)
        self.graphe_mort_mode = BooleanVar(value=False)
        Checkbutton(cadre7_graphe, text="mort", variable=self.graphe_mort_mode, onvalue=True, offvalue=False, command=self.graphe_option).place(x=5,
                                                                                                                                                y=50)
        self.graphe_vaccin_mode = BooleanVar(value=False)
        Checkbutton(cadre7_graphe, text="vaccin", variable=self.graphe_vaccin_mode, onvalue=True, offvalue=False, command=self.graphe_option).place(
            x=75, y=50)
        self.graphe_sain_et_vaccin_mode = BooleanVar(value=False)
        Checkbutton(cadre7_graphe, text="sain + vaccin", variable=self.graphe_sain_et_vaccin_mode, onvalue=True, offvalue=False,
                    command=self.graphe_option).place(x=150, y=50)

        self.case_cochee = StringVar(value="malade")
        Radiobutton(cadre5_case, text="Sain (blanc)", variable=self.case_cochee, value="sain", command=self.case_masque_active).place(x=0, y=0)
        Radiobutton(cadre5_case, text="Malade (rouge)", variable=self.case_cochee, value="malade", command=self.case_masque_active).place(x=0, y=30)
        Radiobutton(cadre5_case, text="Guerie (vert)", variable=self.case_cochee, value="guerie", command=self.case_masque_active).place(x=0, y=60)
        Radiobutton(cadre5_case, text="Vaccin (orange)", variable=self.case_cochee, value="vaccin", command=self.case_masque_active).place(x=0, y=90)
        Radiobutton(cadre5_case, text="Mort (gris)", variable=self.case_cochee, value="mort", command=self.deselectionner_masque).place(x=0, y=120)
        Radiobutton(cadre5_case, text="Mur (noir)", variable=self.case_cochee, value="mur", command=self.deselectionner_masque).place(x=0, y=150)
        self.masque = IntVar()
        self.porter_masque = Checkbutton(cadre5_case, text="Masque (cercle bleu)", variable=self.masque, state='normal')
        self.porter_masque.place(x=0, y=180)

        self.effet_masque = IntVar(value=30)
        Scale(cadre5_masque, variable=self.effet_masque, from_=0, to=100, label="Effet des masques (%):", orient=HORIZONTAL, length=120,
              resolution=10,
              tickinterval=20, showvalue=False).pack(side=TOP)
        self.masque_mode = BooleanVar(value=False)
        Checkbutton(cadre5_masque, text="Masque Aléatoire", variable=self.masque_mode, onvalue=True, offvalue=False,
                    command=self.masque_mode_changer).pack(side=TOP)
        self.masque_communication = IntVar(value=50)
        self.masque_communication_scale = Scale(cadre5_masque, variable=self.masque_communication, from_=0, to=100, label="Communication (%):",
                                                orient=HORIZONTAL, length=120, resolution=5, tickinterval=25, showvalue=False, state="disabled",
                                                sliderrelief="sunken")
        self.masque_communication_scale.pack(side=TOP)

        self.vaccin_force = IntVar(value=70)
        self.vaccin_force_scale = Scale(cadre5_vaccin, variable=self.vaccin_force, from_=0, to=100, label="Efficacité (%):", orient=HORIZONTAL,
                                        length=120, resolution=5, tickinterval=20, showvalue=False)
        self.vaccin_force_scale.pack(side=TOP)
        self.vaccin_mode = BooleanVar(value=False)
        Checkbutton(cadre5_vaccin, text="Vaccin Aléatoire", variable=self.vaccin_mode, onvalue=True, offvalue=False,
                    command=self.vaccin_mode_changer).pack(side=TOP)
        self.vaccin_communication = IntVar(value=100)
        self.vaccin_communication_scale = Scale(cadre5_vaccin, variable=self.vaccin_communication, from_=0, to=100, label="Communication (%):",
                                                orient=HORIZONTAL, length=120, resolution=5, tickinterval=25, showvalue=False, state="disabled",
                                                sliderrelief="sunken")
        self.vaccin_communication_scale.pack(side=TOP)

        Label(cadre6_propagation, text="Infectiosité (%):").pack(side=TOP)
        self.infectiosite = IntVar(value=50)
        self.infectiosite_spin = Spinbox(cadre6_propagation, textvariable=self.infectiosite, from_=0, to=100)
        self.infectiosite_spin.pack(side=TOP)
        Label(cadre6_propagation, text="Letalité (%):").pack(side=TOP)
        self.letalite = IntVar(value=2)
        self.letalite_spin = Spinbox(cadre6_propagation, textvariable=self.letalite, from_=0, to=100)
        self.letalite_spin.pack(side=TOP)

        self.infection_mode = BooleanVar(value=False)
        self.infection_mode_check = Checkbutton(cadre6_propagation, text="infection infinie", variable=self.infection_mode, onvalue=True,
                                                offvalue=False, command=self.infection_mode_changer, state="normal")
        self.infection_mode_check.pack(side=TOP)
        self.infection_temps_min = IntVar(value=6)
        self.infection_temps_max = IntVar(value=12)
        self.infection_temps_min_spin = Spinbox(cadre6_propagation, text="infection min", textvariable=self.infection_temps_min, from_=1,
                                                to=self.infection_temps_max.get(), command=self.infection_temps_min_changer, state='readonly')
        self.infection_temps_max_spin = Spinbox(cadre6_propagation, text="infection max", textvariable=self.infection_temps_max,
                                                from_=self.infection_temps_min.get(), to=30, command=self.infection_temps_max_changer,
                                                state='readonly')
        Label(cadre6_propagation, text="tour min:").pack(side=TOP)
        self.infection_temps_min_spin.pack(side=TOP)
        Label(cadre6_propagation, text="tour max:").pack(side=TOP)
        self.infection_temps_max_spin.pack(side=TOP)

        self.guerison_mode = BooleanVar(value=False)
        self.guerison_mode_check = Checkbutton(cadre6_propagation, text="guerison infinie", variable=self.guerison_mode, onvalue=True, offvalue=False,
                                               command=self.guerison_mode_changer, state="normal")
        self.guerison_mode_check.pack(side=TOP)
        self.guerison_temps_min = IntVar(value=10)
        self.guerison_temps_max = IntVar(value=20)
        self.guerison_temps_min_spin = Spinbox(cadre6_propagation, text="anticorps durée min", textvariable=self.guerison_temps_min, from_=1,
                                               to=self.guerison_temps_max.get(), command=self.guerison_temps_min_changer, state='readonly')
        self.guerison_temps_max_spin = Spinbox(cadre6_propagation, text="anticorps durée max", textvariable=self.guerison_temps_max,
                                               from_=self.guerison_temps_min.get(), to=40, command=self.guerison_temps_max_changer, state='readonly')
        Label(cadre6_propagation, text="tour min:").pack(side=TOP)
        self.guerison_temps_min_spin.pack(side=TOP)
        Label(cadre6_propagation, text="tour max:").pack(side=TOP)
        self.guerison_temps_max_spin.pack(side=TOP)

        Label(cadre6_confinement, text="Taux de voyage (%):").pack(side=TOP)
        self.voyage = IntVar(value=10)
        Spinbox(cadre6_confinement, textvariable=self.voyage, from_=0, to=100).pack(side=TOP)
        self.confinement_force = IntVar(value=100)
        self.confinement_force_scale = Scale(cadre6_confinement, variable=self.confinement_force, from_=0, to=100, label="Contact (%):",
                                             orient=HORIZONTAL, length=120, resolution=5, tickinterval=20, showvalue=False)
        self.confinement_force_scale.pack(side=TOP)
        self.confinement_mode = BooleanVar(value=False)
        Checkbutton(cadre6_confinement, text="Confinement", variable=self.confinement_mode, onvalue=True, offvalue=False,
                    command=self.confinement_mode_changer, state="normal").pack(side=TOP)
        self.confinement_respect = IntVar(value=100)
        self.confinement_respect_scale = Scale(cadre6_confinement, variable=self.confinement_respect, from_=0, to=100, label="Respect confinement:",
                                               orient=HORIZONTAL, length=120, resolution=5, tickinterval=25, showvalue=False, state="disabled",
                                               sliderrelief="sunken")
        self.confinement_respect_scale.pack(side=TOP)

        self.grille()

        self.mainloop()

    def new(self):
        """Relance une simulation"""
        self.flag = False
        self.scene.delete(ALL)
        self.flag_txt.set("GO")
        self.scene.config(cursor="plus")
        self.infection_mode_check.config(state='normal')
        self.guerison_mode_check.config(state='normal')
        self.grille()
        self.curseur_ligne_premier = ()
        self.graphe_x, self.graphe_sain, self.graphe_malade, self.graphe_guerie, self.graphe_mort, self.graphe_vaccin = [], [], [], [], [], []
        del self.simulation
        self.simulation = Simulation()
        self.actu_compteur()

    def start_stop(self):
        """Stop le programme si il est en cours d'execution et inversement"""
        if self.flag:
            self.flag = False
            self.flag_txt.set("GO")
            self.scene.config(cursor="plus")
        else:
            self.flag = True
            self.curseur_ligne_premier = ()
            self.flag_txt.set("STOP")
            self.scene.config(cursor="X_cursor")
            if self.simulation.tour == 0:
                self.simulation.temps_init(self.infection_temps_min.get(), self.infection_temps_max.get(), self.guerison_temps_min.get(),
                                           self.guerison_temps_max.get())
                self.infection_mode_check.config(state='disabled')
                self.guerison_mode_check.config(state='disabled')
            self.play()

    def play(self):
        """Boucle principale de la simulation"""
        if self.flag:
            self.simulation.propagation(self.infectiosite.get(), self.letalite.get(), self.infection_mode.get(), self.infection_temps_min.get(),
                                        self.infection_temps_max.get(), self.guerison_mode.get(), self.guerison_temps_min.get(),
                                        self.guerison_temps_max.get(), self.effet_masque.get(), self.voyage.get(), self.confinement_mode.get(),
                                        self.confinement_force.get(), self.confinement_respect.get(), self.vaccin_force.get(), self.vaccin_mode.get(),
                                        self.vaccin_communication.get(), self.masque_mode.get(), self.masque_communication.get())
            self.simulation.tour += 1
            self.compteur_tour.set("Tour : " + str(self.simulation.tour))
            self.actu_compteur()
            self.actu_graphe()
            self.dessiner()
            if self.flag:
                self.after(self.vitesse.get() - 90, self.play)

    def grille(self):
        """Dessine une grille sur un canvas"""
        xi, longueur_colonne = 0, NBR_Y * TAILLE_CELLULE
        for i in range(NBR_X - 1):
            xi += TAILLE_CELLULE
            self.scene.create_line(xi, 0, xi, longueur_colonne, tags='grille')
        yi, longueur_ligne = 0, NBR_X * TAILLE_CELLULE
        for i in range(NBR_Y - 1):
            yi += TAILLE_CELLULE
            self.scene.create_line(0, yi, longueur_ligne, yi, tags='grille')

    def dessiner(self):
        """Dessine l'etat de la simulation"""
        self.scene.delete(ALL)
        self.grille()
        for y in range(NBR_Y):
            for x in range(NBR_X):
                i, j = x * TAILLE_CELLULE, y * TAILLE_CELLULE
                if self.simulation.etat[y][x] != 0:
                    self.scene.create_rectangle(i, j, i + TAILLE_CELLULE, j + TAILLE_CELLULE,
                                                fill={0: "white", 1: "red", 2: "green", 3: "grey", 4: "orange", 5: "black"}[
                                                    self.simulation.etat[y][x]],
                                                tags=str(x) + ',' + str(y))
                if self.simulation.masque[y][x]:
                    self.scene.create_oval(i, j, i + TAILLE_CELLULE, j + TAILLE_CELLULE, outline="blue", width=1, tags=str(x) + ',' + str(y))

    def sur_scene_mettre(self, y, x, numero):
        """Ajoute un carré sur la scene et en memoire"""
        self.scene.delete(str(x) + ',' + str(y))
        self.scene.create_rectangle(x * TAILLE_CELLULE, y * TAILLE_CELLULE, (x + 1) * TAILLE_CELLULE, (y + 1) * TAILLE_CELLULE,
                                    fill={0: "white", 1: "red", 2: "green", 3: "grey", 4: "orange", 5: "black"}[numero], tags=str(x) + ',' + str(y))
        self.simulation.etat[y][x] = numero
        if numero == 1:
            self.simulation.temps[y][x] = rdm.randint(self.infection_temps_min.get(), self.infection_temps_max.get())
        elif numero == 2:
            self.simulation.temps[y][x] = rdm.randint(self.guerison_temps_min.get(), self.guerison_temps_max.get())
        if self.masque.get():
            self.simulation.masque[y][x] = True
            self.scene.create_oval(x * TAILLE_CELLULE, y * TAILLE_CELLULE, (x + 1) * TAILLE_CELLULE, (y + 1) * TAILLE_CELLULE,
                                   outline="blue", width=1, tags=str(x) + ',' + str(y))
        else:
            self.simulation.masque[y][x] = False

    def clique_souris(self, event):
        """Lorsqu'on clique sur le canvas"""
        if not self.flag:
            if 0 < event.x < NBR_X * TAILLE_CELLULE and 0 < event.y < NBR_Y * TAILLE_CELLULE:
                y, x = event.y // TAILLE_CELLULE, event.x // TAILLE_CELLULE
                case = self.case_cochee.get()
                numero = {"malade": 1, "guerie": 2, "mort": 3, "vaccin": 4, "mur": 5, "sain": 0}[case]

                type_curseur = self.selection_curseur.get()

                if type_curseur == "carre":
                    self.sur_scene_mettre(y, x, numero)

                elif type_curseur == "ligne":
                    taille_div2 = TAILLE_CELLULE // 2
                    if self.curseur_ligne_premier == ():
                        x1 = event.x + taille_div2 - (event.x % TAILLE_CELLULE)  # on ajuste le clique au milieu de la cellule
                        y1 = event.y + taille_div2 - (event.y % TAILLE_CELLULE)
                        self.curseur_ligne_premier = (x1, y1)
                    else:
                        x1, y1, x2, y2 = self.curseur_ligne_premier[0], self.curseur_ligne_premier[
                            1], event.x, event.y  # on recupere les deux endroits cliques
                        self.curseur_ligne_premier = ()

                        x2 += taille_div2 - (x2 % TAILLE_CELLULE)
                        y2 += taille_div2 - (y2 % TAILLE_CELLULE)

                        if abs(x1 - x2) > abs(y1 - y2):  # on regarde qui va etre la reference
                            longueur = abs(x1 - x2) // TAILLE_CELLULE
                        else:
                            longueur = abs(y1 - y2) // TAILLE_CELLULE
                        self.scene.delete("Line")
                        if longueur != 0:
                            x_droite, y_droite = float(x1), float(y1)
                            x_pas, y_pas = (x2 - x1) / longueur, (y2 - y1) / longueur

                            for k in range(longueur + 1):
                                i = int(x_droite) - (int(x_droite) % TAILLE_CELLULE) + 1
                                j = int(y_droite) - (int(y_droite) % TAILLE_CELLULE) + 1
                                self.sur_scene_mettre(j // TAILLE_CELLULE, i // TAILLE_CELLULE, numero)
                                x_droite += x_pas
                                y_droite += y_pas

                else:  # pour la surface
                    if self.curseur_ligne_premier == ():
                        self.curseur_ligne_premier = (event.x - (event.x % TAILLE_CELLULE), event.y - (event.y % TAILLE_CELLULE))
                    else:
                        x1, y1 = self.curseur_ligne_premier[0], self.curseur_ligne_premier[1]  # on recupere les deux endroits cliques
                        x2, y2 = event.x - (event.x % TAILLE_CELLULE), event.y - (event.y % TAILLE_CELLULE)
                        self.curseur_ligne_premier = ()
                        self.scene.delete("Line")

                        if not (x1, y1) == (x2, y2):
                            x_min, x_max = min(x1, x2), max(x2, x1)
                            y_min, y_max = min(y1, y2), max(y1, y2)
                            for i in range(x_min, x_max + 1, TAILLE_CELLULE):
                                for j in range(y_min, y_max + 1, TAILLE_CELLULE):
                                    self.sur_scene_mettre(j // TAILLE_CELLULE, i // TAILLE_CELLULE, numero)
                self.actu_compteur()

    def clique_souris2(self, event):
        """Lorsqu'on maintient la souris pressé sur le canvas"""
        type_curseur = self.selection_curseur.get()
        if type_curseur == "carre":
            if not self.flag:
                if 0 < event.x < NBR_X * TAILLE_CELLULE and 0 < event.y < NBR_Y * TAILLE_CELLULE:
                    case = self.case_cochee.get()
                    self.sur_scene_mettre(event.y // TAILLE_CELLULE, event.x // TAILLE_CELLULE,
                                          {"malade": 1, "guerie": 2, "mort": 3, "vaccin": 4, "mur": 5, "sain": 0}[case])
                    self.actu_compteur()

    def ligne(self, event):
        """Dessine les lignes de suivis pour le mode ligne ou surface"""
        if self.curseur_ligne_premier != ():
            if self.selection_curseur.get() == "ligne":
                self.scene.delete("Line")
                self.scene.create_line(self.curseur_ligne_premier[0], self.curseur_ligne_premier[1], event.x, event.y, tags="Line", fill="orange",
                                       width=3)
            elif self.selection_curseur.get() == "surface":
                carre_x, carre_y = event.x - (event.x % TAILLE_CELLULE), event.y - (event.y % TAILLE_CELLULE)
                if self.curseur_ligne_deuxieme == ():
                    self.curseur_ligne_deuxieme = (carre_x, carre_y)
                if (carre_x, carre_y) != (self.curseur_ligne_deuxieme[1], self.curseur_ligne_deuxieme[0]):
                    self.curseur_ligne_deuxieme = (carre_x, carre_y)
                    self.scene.delete("Line")

                    if carre_x < self.curseur_ligne_premier[0]:
                        gauche, droite = TAILLE_CELLULE, 0
                    else:
                        gauche, droite = 0, TAILLE_CELLULE

                    if carre_y < self.curseur_ligne_premier[1]:
                        haut, bas = TAILLE_CELLULE, 0
                    else:
                        haut, bas = 0, TAILLE_CELLULE

                    self.scene.create_line(self.curseur_ligne_premier[0] + gauche, self.curseur_ligne_premier[1] + haut,
                                           self.curseur_ligne_deuxieme[0] + droite, self.curseur_ligne_premier[1] + haut, tags="Line", fill="orange",
                                           width=3)  # haut
                    self.scene.create_line(self.curseur_ligne_premier[0] + gauche, self.curseur_ligne_deuxieme[1] + bas,
                                           self.curseur_ligne_deuxieme[0] + droite, self.curseur_ligne_deuxieme[1] + bas, tags="Line", fill="orange",
                                           width=3)  # bas
                    self.scene.create_line(self.curseur_ligne_premier[0] + gauche, self.curseur_ligne_premier[1] + haut,
                                           self.curseur_ligne_premier[0] + gauche, self.curseur_ligne_deuxieme[1] + bas, tags="Line", fill="orange",
                                           width=3)  # gauche
                    self.scene.create_line(self.curseur_ligne_deuxieme[0] + droite, self.curseur_ligne_premier[1] + haut,
                                           self.curseur_ligne_deuxieme[0] + droite, self.curseur_ligne_deuxieme[1] + bas, tags="Line", fill="orange",
                                           width=3)  # droite

    def actu_compteur(self):
        """Actualise les compteurs"""
        self.simulation.sain, self.simulation.malade, self.simulation.guerie, self.simulation.mort, self.simulation.vaccin = 0, 0, 0, 0, 0
        for a in self.simulation.etat:
            for b in a:
                if b == 0:
                    self.simulation.sain += 1
                elif b == 1:
                    self.simulation.malade += 1
                elif b == 2:
                    self.simulation.guerie += 1
                elif b == 3:
                    self.simulation.mort += 1
                elif b == 4:
                    self.simulation.vaccin += 1

        self.compteur_tour.set("Tour : " + str(self.simulation.tour))
        self.compteur_sain.set("Sain : " + str(self.simulation.sain))
        self.compteur_malade.set("Malade : " + str(self.simulation.malade))
        self.compteur_guerie.set("Guerie : " + str(self.simulation.guerie))
        self.compteur_vaccin.set("Vaccin : " + str(self.simulation.vaccin))
        self.compteur_mort.set("Mort : " + str(self.simulation.mort))
        self.compteur_r0.set("R0 : " + (str(self.simulation.r0) + "0000")[:5])

    def actu_graphe(self):
        """Enregistre les données pour le graphe"""
        self.graphe_x.append(self.simulation.tour)
        self.graphe_malade.append(self.simulation.malade)
        self.graphe_sain.append(self.simulation.sain)
        self.graphe_guerie.append(self.simulation.guerie)
        self.graphe_mort.append(self.simulation.mort)
        self.graphe_vaccin.append(self.simulation.vaccin)

    def graphe(self):
        """Dessine un graphe avec pyplot"""
        if self.graphe_x:
            if self.flag:
                self.start_stop()
            if self.graphe_malade_mode.get():
                plt.plot(self.graphe_x, self.graphe_malade, color='r', label="Malade")
            if self.graphe_guerie_mode.get():
                plt.plot(self.graphe_x, self.graphe_guerie, color='g', label="Guerie")
            if self.graphe_sain_mode.get():
                plt.plot(self.graphe_x, self.graphe_sain, color='b', label="Sain")
            if self.graphe_mort_mode.get():
                plt.plot(self.graphe_x, self.graphe_mort, color='grey', label="Mort")
            if self.graphe_vaccin_mode.get():
                plt.plot(self.graphe_x, self.graphe_vaccin, color='orange', label="Vaccin")
            if self.graphe_sain_et_vaccin_mode.get():
                plt.plot(self.graphe_x, [self.graphe_vaccin[k] + self.graphe_sain[k] for k in range(self.simulation.tour)], color='b',
                         label="Sain + Vaccin")
            leg = plt.legend(bbox_to_anchor=(0, 1.05, 1., .102), loc='upper right', ncol=4, shadow=True, fancybox=True)
            leg.get_frame().set_alpha(1)
            plt.show()

    def infection_temps_min_changer(self):
        self.infection_temps_max_spin.config(from_=self.infection_temps_min.get())

    def infection_temps_max_changer(self):
        self.infection_temps_min_spin.config(to=self.infection_temps_max.get())

    def infection_mode_changer(self):
        if self.infection_mode.get():
            self.infection_temps_min_spin.config(state='disabled')
            self.infection_temps_max_spin.config(state='disabled')
        else:
            self.infection_temps_min_spin.config(state='readonly')
            self.infection_temps_max_spin.config(state='readonly')

    def guerison_temps_min_changer(self):
        self.guerison_temps_max_spin.config(from_=self.guerison_temps_min.get())

    def guerison_temps_max_changer(self):
        self.guerison_temps_min_spin.config(to=self.guerison_temps_max.get())

    def guerison_mode_changer(self):
        if self.guerison_mode.get():
            self.guerison_temps_min_spin.config(state='disabled')
            self.guerison_temps_max_spin.config(state='disabled')
        else:
            self.guerison_temps_min_spin.config(state='readonly')
            self.guerison_temps_max_spin.config(state='readonly')

    def confinement_mode_changer(self):
        if self.confinement_mode.get():
            self.confinement_respect_scale.config(state="normal", sliderrelief="raised")
        else:
            self.confinement_respect_scale.config(state="disabled", sliderrelief="sunken")

    def vaccin_mode_changer(self):
        if self.vaccin_mode.get():
            self.vaccin_communication_scale.config(state="normal", sliderrelief="raised")
        else:
            self.vaccin_communication_scale.config(state="disabled", sliderrelief="sunken")

    def masque_mode_changer(self):
        if self.masque_mode.get():
            self.masque_communication_scale.config(state="normal", sliderrelief="raised")
        else:
            self.masque_communication_scale.config(state="disabled", sliderrelief="sunken")

    def deselectionner_masque(self):
        self.porter_masque.config(state='disabled')
        self.masque.set(0)

    def case_masque_active(self):
        self.porter_masque.config(state='normal')

    def second_point(self):
        self.scene.delete("Line")
        self.curseur_ligne_premier = ()

    def graphe_option(self):
        if self.graphe_sain_mode.get() or self.graphe_malade_mode.get() or self.graphe_guerie_mode.get() or self.graphe_mort_mode.get() or self.graphe_vaccin_mode.get() or self.graphe_sain_et_vaccin_mode.get():
            self.graphe_bouton.config(state='normal')
        else:
            self.graphe_bouton.config(state='disabled')
