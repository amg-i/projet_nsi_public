from random import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtCore import QTimer
class Case:
    def __init__(self, terrain, jeu, coord, tp=(0, 0)):
        """initialise terrain qui represente la caracteristique de case et lemming qui est pour l'instant inextanant"""
        self.terrain = terrain
        self.lemming = None
        self.duree_presence = 0
        self.spawn = False
        self.durabilite = 3
        self.tp = tp
        self.teleported = False
        self.jeu = jeu
        self.coord = coord
        self.active = False
        self.profondeur = 0
        self.l = [" ", '0', '_', '‾', '(', '¬', '□', '⬡', 'O', '¦','„', '“', '~', '﹋', '9', '°', '$']
        self.lb = [" ", '0', '_', '‾', '(', '¬', '□', '⬡', 'O','„', '“', '~', '﹋', '9', '°', '$']

    def aspect(self):
        """renvoie le caractere a afficher pour representer cette case ou son eventuel occupant"""
        if self.terrain in ('-', '9', '°', '⬡'):
            if not self.jeu.mode_facile:
                couleur_fond = QColor(169,169,169)
            else:
                couleur_fond = QColor(100,100,100)
            if self.lemming is not None : self.desintegre_lemming()
            return couleur_fond,'carre'

        if self.lemming is not None:
            if self.jeu.lim_speed:
                player_color=QColor(255,255,0)
            else:
                player_color = QColor(255,127,0)
            self.desintegre_lemming()
            self.tuer_lemming()
            self.return_leming()
            if self.lemming is not None:
                if self.spawn:
                    self.spawn = False
                    return QColor(238,130,238), 'triangle', player_color, self.lemming.direction
                p2 = 'triangle',player_color,self.lemming.direction
            else:
                p2 = 'carre', None, None
        else:
            p2 = 'carre', None, None
        if self.terrain == "¦":
            return QColor(255,255,255),'ligne_vertical', p2[0], p2[1], p2[2]
        elif self.terrain == '(':
            return QColor(100,100,100), p2[0], p2[1], p2[2]
        elif self.terrain in ("±", "+", '/'):
            return QColor(169,169,169), p2[0], p2[1], p2[2]
        if self.terrain =='□':

            return QColor(255,0,0), p2[0], p2[1], p2[2]
        elif self.terrain == '$':
            if not self.jeu.mode_facile:
                couleur_return = QColor(169,169,169)
            else:
                couleur_return = QColor(100,100,100)
            return couleur_return, 'triangle', QColor(238,130,238), self.jeu.direction
        elif self.terrain == "¬":
            return QColor(255,130,0), p2[0], p2[1], p2[2]
        elif self.terrain == "#":
            return QColor(169,169,169), p2[0], p2[1], p2[2]
        elif self.terrain == " ":
            if not self.jeu.mode_facile:
                couleur = QColor(169,169,169)
            else:
                couleur = QColor(100,100,100)
            if self.spawn:
                self.spawn = False
                if self.jeu.direction == 1:
                    return QColor(238,130,238), 'triangle',QColor(100,100,100),1
                else:
                    return QColor(238,130,238), 'triangle',QColor(100,100,100),-1
            return couleur, p2[0], p2[1], p2[2]
        elif self.terrain == "_":
            if self.teleported:
                self.teleported = False
                return QColor(0,255,255), p2[0], p2[1], p2[2]
            return QColor(100,100,100),'ligne', p2[0], p2[1], p2[2]
        elif self.terrain == '‾':
            if self.teleported:
                self.teleported = False
                return QColor(0,255,255), p2[0], p2[1], p2[2]
            return QColor(100,100,100),'ligne_haut', p2[0], p2[1], p2[2]
        elif self.terrain == "0":
            return QColor(0, 255, 255), p2[0], p2[1], p2[2]
        elif self.terrain == 'O':
            return QColor(0, 210, 210), p2[0], p2[1], p2[2]
        elif self.terrain == "‡":
            return QColor(152,152,152), p2[0], p2[1], p2[2]
        elif self.terrain == '†':
            return QColor(135,135,135), p2[0], p2[1], p2[2]
        elif self.terrain == '|':
            return QColor(118,118,118), p2[0], p2[1], p2[2]
        elif self.terrain == '„':
            if self.active:
                self.active = False
                return QColor(0,255,11), p2[0], p2[1], p2[2]
            return QColor(100,100,100), 'ligne', p2[0], p2[1], p2[2]
        elif self.terrain == '“':
            if self.active:
                self.active = False
                return QColor(0,255,11), p2[0], p2[1], p2[2]
            return QColor(100,100,100), 'ligne_haut', p2[0], p2[1], p2[2]
        elif self.terrain == '~':
            return QColor(0,0,255), p2[0], p2[1], p2[2]
        elif self.terrain == '﹋':
            return QColor(0,0,255), p2[0], p2[1], p2[2]
        elif self.terrain == '*':
            return QColor(255,255,255), p2[0], p2[1], p2[2]

        else:
            return QColor(100,100,100), p2[0], p2[1], p2[2]

    def libre(self, bas = False):
        """renvoie True si la case peut recevoir un lemming (elle n'est ni occupée ni un mur """
        if self.lemming is None:
            if self.terrain in ("‡", "†", '|', '±', '+', '/'):
                self.check_durabilite()
            if not bas:
                if self.terrain in self.l:
                    return True
            else:
                if self.terrain in self.lb:
                    return True

        return False

    def depart(self):
        """retire le lemming present dans la case s'il yen a un """
        self.lemming = None
        self.duree_presence = 0

    def arrivee(self, lem):
        """ place le lemming lem sur la cas ou le fait sortir du jeu si la case est une sortie"""
        if self.libre():
            if self.terrain == "0":
                self.jeu.lemmings_sorti.append(lem)

            elif self.terrain == '9':
                self.jeu.running = False
                self.jeu.good_end()


            else:
                self.lemming = lem

    def tp_lemming(self):
        """ teleporte et place le lemming present sur la case a la destination si elle est disponible"""
        if self.terrain in ("_", '‾', '(') and self.lemming is not None and self.jeu.fenetre.widget_carte.carte[self.tp[0]][self.tp[1]].libre():

            self.lemming.colonne = self.tp[0]
            self.lemming.ligne = self.tp[1]
            self.lemming.action_execute = True
            self.jeu.fenetre.widget_carte.carte[self.lemming.colonne][self.lemming.ligne].arrivee(self.lemming)
            self.depart()
            self.teleported = True

    def grimpe_echelle(self):
        """deplace le lemming en le faisant grimper a l'echelle"""
        if self.coord[0] > 0:
            if self.terrain == "¦" and self.lemming is not None and self.jeu.fenetre.widget_carte.carte[self.coord[0] - 1][self.coord[1]].libre():
                if not self.lemming.action_execute:
                    self.lemming.colonne -= self.lemming.gravite
                    self.lemming.action_execute = True
                    self.jeu.fenetre.widget_carte.carte[self.coord[0] - 1][self.coord[1]].arrivee(self.lemming)
                    self.depart()

    def tuer_lemming(self):
        """reduit la vie du lemming aléatoirement pouvant le tuer ou non en fonction de la quantité de vie enlevé """
        if self.terrain == "¬":

            self.lemming.vie -= random()
            if self.lemming.vie <= 0:
                self.lemming.vie = 0
                self.lemming.sort()
                self.lemming = None

    def desintegre_lemming(self):
        """tue le lemming qui va sur cette case"""
        if self.terrain in ('□', 'O', '⬡'):
            self.lemming.sort()
            self.lemming = None

    def check_durabilite(self):
        """verifie la durabilité du bloc cassable"""
        self.durabilite -= 1
        if self.terrain in ("‡", "†", '|'):
            if self.durabilite == 2:
                self.terrain = "†"
            elif self.durabilite == 1:
                self.terrain = "|"
            elif self.durabilite == 0:
                self.terrain = " "
        elif self.terrain in ("±", "+", '/'):
            if self.durabilite == 2:
                self.terrain = "+"
            elif self.durabilite == 1:
                self.terrain = "/"
            elif self.durabilite == 0:
                self.terrain = " "

    def change_gravite(self):
        """inverse la gravité du lemming"""
        if self.terrain in ('„', '“') and self.lemming is not None and not self.lemming.action_execute:
            self.lemming.gravite *= -1
            self.lemming.direction *= -1
            self.active = True

    def calcul_profondeur(self, gravite):
        """calcul la profondeur de la collone d'eau"""
        self.profondeur = 0
        if self.jeu.fenetre.widget_carte.carte[self.coord[0] - gravite][self.coord[1]].terrain == self.terrain:
            self.profondeur = self.jeu.fenetre.widget_carte.carte[self.coord[0] - gravite][self.coord[1]].calcul_profondeur(gravite)
        else:
            self.profondeur = 0
        return self.profondeur + 1

    def coule(self):
        """fait couler les lemming en fonction du nombre de lemming empilé dessus"""
        if self.terrain in ('~','﹋') :
            if self.terrain == '~':
                gravite = 1
            else: gravite = -1

            self.calcul_profondeur(gravite)

            if self.profondeur > 0:
                if '~' in self.lb and gravite == 1:
                    self.lb.remove('~')
                if '﹋'in self.lb and gravite == -1:
                    self.lb.remove('﹋')

            if self.lemming is not None:
                if not self.lemming.action_execute:

                    self.lemming.check_empilement()

                    if self.lemming.empilement > self.profondeur and self.jeu.fenetre.widget_carte.carte[self.coord[0] + self.lemming.gravite][self.coord[1]].libre():
                            self.lemming.colonne += self.lemming.gravite
                            self.lemming.action_execute = True
                            self.jeu.fenetre.widget_carte.carte[self.coord[0] + self.lemming.gravite][self.coord[1]].arrivee(self.lemming)
                            self.depart()
                    elif self.lemming.empilement < self.profondeur and self.jeu.fenetre.widget_carte.carte[self.coord[0] - self.lemming.gravite][self.coord[1]].libre():
                            self.lemming.colonne -= self.lemming.gravite
                            self.lemming.action_execute = True
                            self.jeu.fenetre.widget_carte.carte[self.coord[0] - self.lemming.gravite][self.coord[1]].arrivee(self.lemming)
                            self.depart()

    def return_leming(self):
        if self.terrain == '$':
            self.jeu.lemmings_possede.append(self.lemming)
            self.lemming.sort()
            self.lemming = None

            self.jeu.fenetre.label_info.setText(
                f'{len(self.jeu.lemmings_possede)} lemmings restants.\n{len(self.jeu.lemming_sauve)} lemmings sauvés.')