class Case:
    def __init__(self, terrain, jeu, tp=(0, 0)):
        """
        initialise terrain qui represente la caracteristique de case
         et lemming qui est pour l'instant inextanant
         """
        self.terrain = terrain
        self.lemming = None

    def __str__(self):
        """
        renvoie le caractere a afficher
        pour reprezsenter cette case ou son eventuel occupant
        """
        if self.lemming is not None:
            return str(self.lemming)

        elif self.terrain == "#":
            return "\033[90m" + self.terrain + "\033[0m"
        elif self.terrain == " ":
            return self.terrain
        elif self.terrain == "0":
            return "\033[96m" + self.terrain + "\033[0m"

    def libre(self):
        """
        renvoie True si la case peut recevoir un lemming
        (elle n'est ni occupée ni un mur)
         """
        liste = [" ", '0', '_']
        if self.lemming is None and self.terrain in liste:
            return True

        return False

    def depart(self):
        """retire le lemming present dans la case s'il yen a un """
        self.lemming = None

    def arrivee(self, lem):
        """
        place le lemming lem sur la cas ou
        le fait sortir du jeu si la case est une sortie
        """
        if self.libre():
            if self.terrain == "0":
                lem.sort()
            else:
                self.lemming = lem
