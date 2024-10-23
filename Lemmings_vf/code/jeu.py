from inputs import get_gamepad
import random

from case import Case
from lemming import Lemming

class Jeu:
    '''
        Fait tourner le jeu
    '''
    def __init__(self, fenetre, lvl:int = 0):
        '''
            initialise le jeu
        '''
        self.fenetre = fenetre
        self.lvl = lvl
        self.nb_lemming_initial = 20
        self.lemmings_possede: list[Lemming] = ([Lemming(0, 0, 1, self, vie=5, speed=0, agi=0.5)] +
                                                [Lemming(0, 0, 1, self, vie=random.randint(5,12), speed=random.random(), agi=(random.randint(750, 999)/1000)) for i in range(18)] +
                                                [Lemming(0, 0, 1, self, vie=15, speed=1, agi=1)])
        self.lim_speed = True
        self.lemmings: list[Lemming] = []
        self.lemmings_sorti: list[Lemming] = []
        self.entree =  None
        self.lemming_sauve = []
        self.running: bool = False

        self.mode_facile = True




        self.__init_grotte__()

    def __init_grotte__(self):
        '''
            initialise la grotte en fonction du niveau du joueur
        '''
        with open('../assets/maps.csv', 'r') as fichier:
            tableau = fichier.read()
        tableau = tableau.split('\n')
        for ligne in range(len(tableau)):
            tableau[ligne] = tableau[ligne].split(',')
        if self.lvl + 1 < len(tableau):
            grotte = tableau[self.lvl + 1][1][1:-1].split('!')
            lien_tp = tableau[self.lvl + 1][6].split('%')
            coord_tp = {}
            if lien_tp != ['']:
                for lien in range(len(lien_tp)):
                    lien_tp[lien] = lien_tp[lien].split('->')
                    lien_tp[lien][0] = lien_tp[lien][0].split(';')
                    lien_tp[lien][0] = str((int(lien_tp[lien][0][0]), int(lien_tp[lien][0][1])))
                    lien_tp[lien][1] = lien_tp[lien][1].split(';')
                    lien_tp[lien][1] = (int(lien_tp[lien][1][0]), int(lien_tp[lien][1][1]))
                    coord_tp[lien_tp[lien][0]] = tuple(lien_tp[lien][1])


            self.entrees =  self.trouve_entree(tableau)
            self.nb_entree = int(tableau[self.lvl + 1][3])
            self.entree_selectionne = int(tableau[self.lvl + 1][4]) - 1

            self.fenetre.carte = []
            for i in range(len(grotte)):
                etage_grotte = []
                for char in range(len(grotte[i])):
                    dest_tp = (0, 0)
                    if str((i, char)) in coord_tp:
                        dest_tp = coord_tp[str((i, char))]
                    etage_grotte.append(Case(grotte[i][char], self,(i, char), dest_tp))

                    if (i, char) == self.entrees[self.entree_selectionne]:
                        etage_grotte[-1].spawn = True
                self.fenetre.carte.append(etage_grotte)


            self.reproduction()
            self.nb_lemming_initial = len(self.lemmings_possede)
            self.lemming_sauve = []
            self.lemmings: list[Lemming] = []
            self.lemmings_sorti: list[Lemming] = []
            self.direction = int(tableau[self.lvl + 1][5])
            self.lim_speed = tableau[self.lvl + 1][7] == 'True'

            self.fenetre.label_info.setText(f'{len(self.lemmings_possede)} lemmings restants.\n{len(self.lemming_sauve)} lemmings sauvés.')


            if self.fenetre.widget_carte is not None:
                self.fenetre.widget_carte.carte_init(self.fenetre.carte)
                for y in range(len(self.fenetre.widget_carte.carte)):
                    for x in range(len(self.fenetre.widget_carte.carte[y])):
                        if (y, x) == self.entrees[self.entree_selectionne]:
                            self.fenetre.widget_carte.carte[y][x].spawn = True

        else:
            self.running = False
            self.good_end()

    def reproduction(self):
        '''
            reproduit les lemmings et accroit leurs population (ou la reduit selon les conditions de réussite)
        '''
        if len(self.lemming_sauve) > 0:
            if len(self.lemmings_possede) + len(self.lemmings) + len(self.lemming_sauve) != self.nb_lemming_initial:
                nb_mort = self.nb_lemming_initial - (len(self.lemmings_possede) + len(self.lemmings) + len(self.lemming_sauve))
                ratio_mort = nb_mort / (nb_mort + len(self.lemmings) + len(self.lemming_sauve))
                index=0
                while index < len(self.lemmings_possede):
                    if 2*random.random() <= ratio_mort:
                        del self.lemmings_possede[index]
                    else :
                        index += 1
            else:
                for i in range(len(self.lemming_sauve)):
                    self.lemmings_possede.append(self.lemming_sauve[i])
            for i in range(0, len(self.lemmings_possede) - 1, 2):
                self.lemmings_possede.append(Lemming(0, 0, 1, self,
                                                     vie=(self.lemmings_possede[i].vie + self.lemmings_possede[i + 1].vie) / 2,
                                                     speed=(self.lemmings_possede[i].speed + self.lemmings_possede[i + 1].speed) / 2,
                                                     agi=(self.lemmings_possede[i].agilite + self.lemmings_possede[i + 1].agilite) / 2))


    def trouve_entree(self, tableau):
        '''
            recupere les cases d'entree dans le fichier csv
        '''
        entrees = tableau[self.lvl+1][2].split('%')
        for entree in range(len(entrees)):
            entrees[entree] = entrees[entree].split(';')
            entrees[entree][0] = int(entrees[entree][0])
            entrees[entree][1] = int(entrees[entree][1])
            entrees[entree] = tuple(entrees[entree])
        return entrees

    def tour(self):
        '''
            deplace les lemings
        '''

        for y in range(len(self.fenetre.widget_carte.carte)):
            for x in range(len(self.fenetre.widget_carte.carte[y])):
                self.fenetre.widget_carte.carte[y][x].tp_lemming()
                self.fenetre.widget_carte.carte[y][x].grimpe_echelle()
                self.fenetre.widget_carte.carte[y][x].change_gravite()
                self.fenetre.widget_carte.carte[y][x].coule()
        for y in range(len(self.fenetre.widget_carte.carte) - 1, -1, -1):
            for x in range(len(self.fenetre.widget_carte.carte[y]) - 1, -1, -1):
                self.fenetre.widget_carte.carte[y][-x - 1].coule()

        for lemming in self.lemmings:
            if not lemming.action_execute:
                if not self.mode_facile:
                    lemming.glisse()
                if self.lim_speed:
                    speed = 1
                else:
                    if lemming.speed > random.random():
                        speed = 2
                    else:
                        speed = 1
                aligne = lemming.ligne
                acolonne = lemming.colonne
                if lemming.ligne - speed >= 0 and lemming.ligne + speed < len(self.fenetre.widget_carte.carte[0]):
                    lemming.action(self.fenetre.widget_carte.carte[lemming.colonne][lemming.ligne - speed].libre(),
                                   self.fenetre.widget_carte.carte[lemming.colonne][lemming.ligne + speed].libre(),
                                   self.fenetre.widget_carte.carte[lemming.colonne + lemming.gravite][lemming.ligne].libre(True), speed)

                if not self.lim_speed and not lemming.action_execute:
                    speed = 1
                    lemming.action(self.fenetre.widget_carte.carte[lemming.colonne][lemming.ligne - speed].libre(),
                                   self.fenetre.widget_carte.carte[lemming.colonne][lemming.ligne + speed].libre(),
                                   self.fenetre.widget_carte.carte[lemming.colonne + (lemming.gravite) * speed][lemming.ligne].libre(True),
                                   speed)

                if (aligne, acolonne) != (lemming.ligne, lemming.colonne):
                     self.fenetre.widget_carte.carte[acolonne][aligne].depart()
                     self.fenetre.widget_carte.carte[lemming.colonne][lemming.ligne].arrivee(lemming)
                else:
                    lemming.retourne()
            lemming.trebuche = False
            lemming.action_execute = False


        for lemming in self.lemmings:
            lemming.check_empilement()

        for lemming in self.lemmings_sorti:
            self.lemming_sauve.append(lemming)
            lemming.gravite = 1
            lemming.sort()
        self.lemmings_sorti = []
        self.fenetre.label_info.setText(f'{len(self.lemmings_possede)} lemmings restants.\n{len(self.lemming_sauve)} lemmings sauvés.')

    def ajoute(self):
        '''
            ajoute un lemming
        '''
        if len(self.lemmings_possede) > 0:
            if self.fenetre.widget_carte.carte[self.entrees[self.entree_selectionne][0]][self.entrees[self.entree_selectionne][1]].lemming == None:
                self.lemmings.append(self.lemmings_possede[0])
                self.lemmings[-1].colonne = self.entrees[self.entree_selectionne][0]
                self.lemmings[-1].ligne = self.entrees[self.entree_selectionne][1]
                self.lemmings[-1].direction = self.direction

                del self.lemmings_possede[0]
                self.fenetre.label_info.setText(f'{len(self.lemmings_possede)} lemmings restants.\n{len(self.lemming_sauve)} lemmings sauvés.')

                self.fenetre.widget_carte.carte[self.entrees[self.entree_selectionne][0]][self.entrees[self.entree_selectionne][1]].arrivee(self.lemmings[-1])
        else:
            print("vous n'avez plus de lemming en reserve.")

    def change_lim_speed(self):
        if self.lim_speed:
            self.lim_speed = False
        else: self.lim_speed = True

    def demarre(self):
        '''
            boucle principale du jeu
        '''
        for y in range(len(self.fenetre.widget_carte.carte)):
            for x in range(len(self.fenetre.widget_carte.carte[y])):
                if (y, x) == self.entrees[self.entree_selectionne]:
                    self.fenetre.widget_carte.carte[y][x].spawn = True
        self.fenetre.update()
        events = get_gamepad()
        for event in events:

            if event.ev_type == 'Absolute' and event.state == 1023:
                if event.code == 'ABS_RZ':
                    self.direction *= -1
                if event.code == 'ABS_Z':
                    self.change_lim_speed()

            elif event.ev_type == 'Key' and event.state == 1:
                if event.code == 'BTN_START':
                    for y in range(len(self.fenetre.widget_carte.carte)):
                        for x in range(len(self.fenetre.widget_carte.carte[y])):
                            self.fenetre.widget_carte.carte[y][x].depart()
                    lemmings_eradique = []
                    for lemming in self.lemmings:
                        lemmings_eradique.append(lemming)
                    for lemming in lemmings_eradique:
                        lemming.sort()
                elif event.code == 'BTN_SELECT':
                    self.mode_facile = not self.mode_facile

                elif event.code == 'BTN_TL':
                    if self.entree_selectionne > 0:
                        self.entree_selectionne -= 1
                elif event.code == 'BTN_TR':
                    if self.entree_selectionne < self.nb_entree - 1:
                        self.entree_selectionne += 1


                elif event.code == 'BTN_SOUTH':
                    self.ajoute()
                elif event.code == 'BTN_EAST':
                    self.tour()
                elif event.code == 'BTN_WEST':
                    self.fenetre.close()
                elif event.code == 'BTN_NORTH':
                    if len(self.lemming_sauve) >= 1:
                        self.lvl += 1
                        self.__init_grotte__()

        if len(self.lemmings_possede) + len(self.lemmings) + len(self.lemming_sauve)== 0:
            self.bad_end()

    def bad_end(self):
        '''
            ecrit le message de mort
        '''

        print('\n')
        print('       ::::::::           :::          :::   :::       ::::::::::        ::::::::    :::     :::       ::::::::::       :::::::::    ')
        print('     :+:    :+:        :+: :+:       :+:+: :+:+:      :+:              :+:    :+:   :+:     :+:       :+:              :+:    :+:    ')
        print('    +:+              +:+   +:+     +:+ +:+:+ +:+     +:+              +:+    +:+   +:+     +:+       +:+              +:+    +:+     ')
        print('   :#:             +#++:++#++:    +#+  +:+  +#+     +#++:++#         +#+    +:+   +#+     +:+       +#++:++#         +#++:++#:       ')
        print('  +#+   +#+#      +#+     +#+    +#+       +#+     +#+              +#+    +#+    +#+   +#+        +#+              +#+    +#+       ')
        print(' #+#    #+#      #+#     #+#    #+#       #+#     #+#              #+#    #+#     #+#+#+#         #+#              #+#    #+#        ')
        print(' ########       ###     ###    ###       ###     ##########        ########        ###           ##########       ###    ###         ')
        quit()

    def good_end(self):
        print('\n')
        print('    :::     :::       :::::::::::       ::::::::   :::::::::::       ::::::::       :::::::::::       :::::::::       :::::::::: ')
        print('   :+:     :+:           :+:          :+:    :+:      :+:          :+:    :+:          :+:           :+:    :+:      :+:         ')
        print('  +:+     +:+           +:+          +:+             +:+          +:+    +:+          +:+           +:+    +:+      +:+          ')
        print(' +#+     +:+           +#+          +#+             +#+          +#+    +:+          +#+           +#++:++#:       +#++:++#      ')
        print(' +#+   +#+            +#+          +#+             +#+          +#+    +#+          +#+           +#+    +#+      +#+            ')
        print(' #+#+#+#             #+#          #+#    #+#      #+#          #+#    #+#          #+#           #+#    #+#      #+#             ')
        print('  ###           ###########       ########       ###           ########       ###########       ###    ###      ##########       ')
        print("\nBravo, vous avez sauvé l'espece des lemmings")
        quit()