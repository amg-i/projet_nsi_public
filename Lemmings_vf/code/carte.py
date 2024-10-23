
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPolygon, QPen
from PyQt5.QtCore import QPoint, Qt

class Carte(QWidget):
    def __init__(self, carte):
        super().__init__()
        self.carte = None
        self.taille_case = None
        self.lignes = None
        self.colonnes = None

        self.carte_init(carte)

    def carte_init(self,carte):
        self.carte = carte
        if len(self.carte) > len(self.carte[0]):# Taille de chaque case
            self.taille_case = 950//len(self.carte)
        else:
            self.taille_case = 950//len(self.carte[0])
        self.lignes = len(carte)  # Nombre de lignes dans la carte
        self.colonnes = len(carte[0])  # Nombre de colonnes dans la carte
        # Définir la taille du widget en fonction de la carte
        self.setFixedSize(self.colonnes * self.taille_case, self.lignes * self.taille_case)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dessiner chaque case de la carte
        for ligne in range(self.lignes):
            for colonne in range(self.colonnes):
                case = self.carte[ligne][colonne]
                particularite = case.aspect()
                color = particularite[0]
                painter.setBrush(color)
                painter.setPen(Qt.NoPen)
                if particularite[1] == 'carre':
                    painter.drawRect(colonne * self.taille_case, ligne * self.taille_case, self.taille_case, self.taille_case)
                elif particularite[1] == 'triangle':
                    if particularite[2] is not None:
                        painter.drawRect(colonne * self.taille_case, ligne * self.taille_case, self.taille_case,
                                         self.taille_case)
                    painter.setBrush(particularite[2])
                    if particularite[3] == -1:
                        self.dessiner_triangle_gauche(painter, colonne, ligne)
                    else:
                        self.dessiner_triangle_droite(painter, colonne, ligne)
                elif particularite[1] == 'ligne':
                    self.dessiner_trait_horizontal(painter, colonne, ligne)
                    if particularite[2] == 'triangle':
                        painter.setBrush(particularite[3])
                        if particularite[4] == -1:
                            self.dessiner_triangle_gauche(painter, colonne, ligne)
                        else:
                            self.dessiner_triangle_droite(painter, colonne, ligne)
                elif particularite[1] == 'ligne_haut':
                    self.dessiner_trait_horizontal_haut(painter, colonne, ligne)
                    if particularite[2] == 'triangle':
                        painter.setBrush(particularite[3])
                        if particularite[4] == -1:
                            self.dessiner_triangle_gauche(painter, colonne, ligne)
                        else:
                            self.dessiner_triangle_droite(painter, colonne, ligne)
                elif particularite[1] == 'ligne_vertical':
                    self.dessiner_trait_vertical(painter, colonne, ligne)
                    if particularite[2] == 'triangle':
                        painter.setBrush(particularite[3])
                        if particularite[4] == -1:
                            self.dessiner_triangle_gauche(painter, colonne, ligne)
                        else:
                            self.dessiner_triangle_droite(painter, colonne, ligne)
    def dessiner_triangle_gauche(self, painter, colonne, ligne):
        # Dessiner un triangle pointant vers la gauche
        points = QPolygon([
            QPoint(colonne * self.taille_case + self.taille_case // 2, ligne * self.taille_case + 10),
            QPoint(colonne * self.taille_case + 10, ligne * self.taille_case + self.taille_case // 2),
            QPoint(colonne * self.taille_case + self.taille_case // 2, (ligne + 1) * self.taille_case - 10)
        ])
        #painter.setBrush(QBrush(QColor(255, 255, 0)))  # Remplir le triangle avec du jaune
        painter.drawPolygon(points)

    def dessiner_triangle_droite(self, painter, colonne, ligne):
        # Dessiner un triangle pointant vers la droite
        points = QPolygon([
            QPoint(colonne * self.taille_case + self.taille_case // 2, ligne * self.taille_case + 10),
            QPoint((colonne + 1) * self.taille_case - 10, ligne * self.taille_case + self.taille_case // 2),
            QPoint(colonne * self.taille_case + self.taille_case // 2, (ligne + 1) * self.taille_case - 10)
        ])
        #painter.setBrush(QBrush(QColor(255, 255, 0)))  # Remplir le triangle avec du jaune
        painter.drawPolygon(points)
    def dessiner_trait_horizontal(self, painter, colonne, ligne):
        # Définir un stylo noir avec une épaisseur de 5 pour le trait horizontal
        pen = QPen(Qt.black, 5)
        painter.setPen(pen)

        # Calculer les coordonnées pour dessiner le trait horizontal
        x1 = colonne * self.taille_case + 10
        x2 = (colonne + 1) * self.taille_case - 10
        y = (ligne + 1) * self.taille_case - 10

        # Dessiner le trait
        painter.drawLine(x1, y, x2, y)

        # Remettre le stylo pour les contours des cases
        painter.setPen(QPen(Qt.NoPen))

    def dessiner_trait_horizontal_haut(self, painter, colonne, ligne):
        # Définir un stylo noir avec une épaisseur de 5 pour le trait horizontal
        pen = QPen(Qt.black, 5)
        painter.setPen(pen)

        # Calculer les coordonnées pour dessiner le trait horizontal
        x1 = colonne * self.taille_case + 10
        x2 = (colonne + 1) * self.taille_case - 10
        y = ligne * self.taille_case + 10

        # Dessiner le trait
        painter.drawLine(x1, y, x2, y)

        # Remettre le stylo pour les contours des cases
        painter.setPen(QPen(Qt.NoPen))

    def dessiner_trait_vertical(self, painter, colonne, ligne):
        # Définir un stylo noir avec une épaisseur de 5 pour le trait vertical
        pen = QPen(Qt.white, 5)
        painter.setPen(pen)

        # Calculer les coordonnées pour dessiner le trait horizontal
        x = colonne * self.taille_case + self.taille_case//2
        y1 = (ligne + 1) * self.taille_case
        y2 = ligne * self.taille_case

        # Dessiner le trait
        painter.drawLine(x, y1, x, y2)

        # Remettre le stylo pour les contours des cases
        painter.setPen(QPen(Qt.NoPen))