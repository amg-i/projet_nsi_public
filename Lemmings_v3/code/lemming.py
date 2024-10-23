class Lemming:
    # defint la classe lemming
    def __init__(self, colonne, ligne, direction, jeu=None):
        self.ligne = ligne
        self.colonne = colonne
        self.direction = direction
        self.jeu = jeu

    def __str__(self):
        # renvoie la direction du lemming avec '<' ou '>'.
        if self.direction < 0:
            return '\033[93m<\033[0m'
        if self.direction > 0:
            return '\033[93m>\033[0m'

    def action(self, contourg, contourd, contourb):
        # déplace ou retourne le perso
        if contourb:
            self.colonne += 1
        elif self.direction < 0:
            if contourg:
                self.ligne -= 1
            else:
                self.direction = 1

        elif self.direction > 0:
            if contourd:
                self.ligne += 1
            else:
                self.direction = -1

    def sort(self):
        # retire le lemming du jeu.
        self.jeu.lemmings.remove(self)
