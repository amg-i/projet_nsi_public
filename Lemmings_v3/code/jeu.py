from inputs import get_gamepad

from case import Case
from lemming import Lemming


class Jeu:
    '''
        Fait tourner le jeu
    '''
    def __init__(self, lvl: int = 0):
        '''
            initialise le jeu
        '''
        self.lvl = lvl
        self.grotte: list[list[Case]] | None = None
        self.__init_grotte__()
        self.lemmings: list[Lemming] = []
        self.lemmings_sorti: list[Lemming] = []
        self.entree = None
        self.lemming_sauvé = 0
        self.running: bool = False

        print("nombre de lemmins sauvé: ", self.lemming_sauvé)

    def affiche(self):
        '''
            affiche la grille
        '''
        for y in range(len(self.grotte)):
            ligne = []
            for x in range(len(self.grotte[y])):
                ligne.append(str(self.grotte[y][x]))
            print(''.join(ligne))

    def tour(self):
        '''
            deplace les lemings
        '''
        for lemming in self.lemmings:
            aligne = lemming.ligne
            acolonne = lemming.colonne
            lemming.action(self.grotte[lemming.colonne]
                           [lemming.ligne - 1].libre(),
                           self.grotte[lemming.colonne]
                           [lemming.ligne + 1].libre(),
                           self.grotte[lemming.colonne + 1]
                           [lemming.ligne].libre())
            if (aligne, acolonne) != (lemming.ligne, lemming.colonne):
                self.grotte[lemming.colonne][lemming.ligne].arrivee(lemming)
                self.grotte[acolonne][aligne].depart()
        for lemming in self.lemmings_sorti:
            self.lemming_sauvé += 1
            lemming.sort()
        self.lemmings_sorti = []

    def ajoute(self):
        '''
            ajoute un lemming
        '''
        lem = Lemming(self.entrees[self.entree_selectionne][0],
                      self.entrees[self.entree_selectionne][1],
                      self.direction, self)
        if self.grotte[
            self.entrees[self.entree_selectionne]
            [0]
        ][self.entrees[self.entree_selectionne][1]].lemming is not None:
            self.lemmings.append(lem)

        self.grotte[
            self.entrees[self.entree_selectionne]
            [0]
        ][self.entrees[self.entree_selectionne][1]].arrivee(lem)

    def demarre(self):
        '''
            boucle principale du jeu
        '''
        self.running = True
        while self.running:
            events = get_gamepad()
            for event in events:

                if event.ev_type == 'Absolute' and event.state == 1023:
                    if event.code == 'ABS_RZ':
                        self.direction *= -1

                        self.affiche()

                elif event.ev_type == 'Key' and event.state == 1:
                    if event.code == 'BTN_TL':
                        if self.entree_selectionne > 0:
                            self.entree_selectionne -= 1

                            self.affiche()
                    elif event.code == 'BTN_TR':
                        if self.entree_selectionne < self.nb_entree - 1:
                            self.entree_selectionne += 1

                            self.affiche()

                    elif event.code == 'BTN_SOUTH':
                        self.ajoute()
                        self.affiche()

                    elif event.code == 'BTN_EAST':
                        self.tour()
                        self.affiche()

                    elif event.code == 'BTN_WEST':
                        self.running = False

                    elif event.code == 'BTN_NORTH':
                        if self.lemming_sauvé >= 1:
                            self.lvl += 1
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
            grotte = tableau[self.lvl+1][1][1: -1].split('!')
            self.grotte = []
            for i in range(len(grotte)):
                etage_grotte = []
                for char in grotte[i]:
                    etage_grotte.append(Case(char, self))

                self.grotte.append(etage_grotte)

            self.lemmings: list[Lemming] = []
            self.lemmings_sorti: list[Lemming] = []
            self.entrees = self.trouve_entree(tableau)
            self.nb_entree = int(tableau[self.lvl + 1][3])
            self.entree_selectionne = int(tableau[self.lvl + 1][4]) - 1
            self.lemming_sauvé = 0
            self.direction = int(tableau[self.lvl + 1][5])

            self.affiche()

        else:
            print('Bravo, vous avez terminez le jeu')
            self.running = False

    def trouve_entree(self, tableau):
        entrees = tableau[self.lvl+1][2].split('%')
        for entree in range(len(entrees)):
            entrees[entree] = entrees[entree].split(';')
            entrees[entree][0] = int(entrees[entree][0])
            entrees[entree][1] = int(entrees[entree][1])
            entrees[entree] = tuple(entrees[entree])

        return entrees
