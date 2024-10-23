
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QTimer

from jeu import Jeu
from carte import Carte

class Fenetre(QWidget):
    def __init__(self):
            super().__init__()

            self.setWindowTitle('Carte de Jeu')
            self.setGeometry(0,0,1000,1000)

            # Exemple de carte (tableau 2D)
            self.carte = []
            self.widget_carte = None

            self.label_info = QLabel('')


            self.jeu = Jeu(self)

            # Créer le widget de la carte
            self.widget_carte = Carte(self.carte)




            # Créer un layout principal vertical
            main_layout = QVBoxLayout()

            # Ajouter le widget de la carte au layout principal
            main_layout.addWidget(self.widget_carte)

            main_layout.addWidget(self.label_info)


            # Appliquer le layout à la fenêtre
            self.setLayout(main_layout)

            # Changer la couleur de fond de la fenêtre principale
            self.setStyleSheet('background-color: #646464;')

            # Met un icône à la fenêtre de jeu
            self.setWindowIcon(QIcon('icone_jeu_lemming.png'))

            self.show()

            # Créer un timer qui met à jour toutes les 10 ms
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.jeu.demarre)  # Associer le timer à refresh
            self.timer.start(10)  # en ms




