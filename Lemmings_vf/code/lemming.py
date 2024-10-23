import random
class Lemming:
    # defint la classe lemming
    def __init__(self, colonne, ligne, direction, jeu = None, vie = 5, speed = 0.5, agi = 0.5):
        # l est la ligne, c la colonne, d est la direction et j accede a la classe jeu.
        self.ligne = ligne
        self.colonne = colonne
        self.direction = direction
        self.jeu = jeu
        self.action_execute = False
        self.vie = vie
        self.speed = speed
        self.gravite = 1
        self.empilement = 0
        self.agilite = agi
        self.trebuche = False

    def __str__(self):
        # renvoie la direction du lemming avec '<' ou '>'.
        if self.direction < 0:
            return '\033[93m<\033[0m'
        if self.direction > 0:
            return '\033[93m>\033[0m'

    def action(self, contourg, contourd, contourb, speed = 1):
        # déplace ou non le lemming
        if contourb:
            self.colonne += self.gravite
            self.action_execute = True

        elif not self.trebuche:

            if self.direction < 0 and contourg:
                self.ligne -= speed
                self.action_execute = True


            elif self.direction > 0 and contourd:
                self.ligne += speed
                self.action_execute = True


    def retourne(self):
        # retourne le lemming
        if not self.trebuche:
            self.direction = - self.direction

    def glisse(self):
        self.trebuche = self.agilite < random.random()

    def sort(self):
        # retire le lemming du jeu.
        self.jeu.lemmings.remove(self)

    def check_empilement(self):
        # verifie l'emplacement du lemming
        self.empilement = 0
        if self.jeu.fenetre.widget_carte.carte[self.colonne - self.gravite][self.ligne].lemming is not None:
            if self.jeu.fenetre.widget_carte.carte[self.colonne - self.gravite][self.ligne].lemming.gravite == self.gravite:
                self.empilement = self.jeu.fenetre.widget_carte.carte[self.colonne - self.gravite][self.ligne].lemming.check_empilement()
            else:
                self.empilement = 0
        else:
            self.empilement = 0
        return self.empilement + 1