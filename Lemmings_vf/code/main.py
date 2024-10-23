
*
3àom fenetre import Fenetre

import sys
from PyQt5.QtWidgets import QApplication


def main():
    '''
        lance le jeu
    '''

    app = QApplication(sys.argv)
    fenetre = Fenetre()
    sys.exit(app.exec_())

main()