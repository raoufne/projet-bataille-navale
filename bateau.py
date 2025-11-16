import random
class Bateau:

    def __init__(self, ligne: int, colonne: int, longueur: int = 1, vertical: bool = False, marque: str = '⛵'):
        self.ligne = ligne       
        self.colonne = colonne   
        self.longueur = longueur 
        self.vertical = vertical 
        self.marque = marque

    @property
    def positions(self):
        pos = []
        if self.vertical:
            for i in range(self.longueur):
                pos.append((self.ligne + i, self.colonne))
        else:
            for i in range(self.longueur):
                pos.append((self.ligne, self.colonne + i))
        return pos

    def coule(self, grille):
        for ligne, colonne in self.positions:
            index = ligne * grille.nb_colonnes + colonne
            if grille.liste[index] != '💣':
                return False
        return True    

    def position_alea(self, grille, positions_occupees=None):
        positions_valides = []

        for ligne in range(grille.nb_lignes):
            for colonne in range(grille.nb_colonnes):
                for vertical in [False, True]:
                    b_temp = type(self)(ligne, colonne, vertical=vertical)

                    if not all(0 <= l < grille.nb_lignes and 0 <= c < grille.nb_colonnes for l, c in b_temp.positions):
                        continue

                    chevauche = False
                    for l, c in b_temp.positions:
                        index = l * grille.nb_colonnes + c
                        if (l, c) in positions_occupees:
                            chevauche = True
                            break

                    if not chevauche:
                        positions_valides.append((ligne, colonne, vertical))

        if not positions_valides:
            raise Exception(f"Impossible de placer le bateau {self.marque} !")

        ligne, colonne, vertical = random.choice(positions_valides)
        self.ligne = ligne
        self.colonne = colonne
        self.vertical = vertical
    
class PorteAvion(Bateau):
    def __init__(self, ligne, colonne, vertical=False):
        super().__init__(ligne, colonne, longueur=4, vertical=vertical, marque='🚢')

class Croiseur(Bateau):
    def __init__(self, ligne, colonne, vertical=False):
        super().__init__(ligne, colonne, longueur=3, vertical=vertical, marque='⛴')

class Torpilleur(Bateau):
    def __init__(self, ligne, colonne, vertical=False):
        super().__init__(ligne, colonne, longueur=2, vertical=vertical, marque='🚣')

class SousMarin(Bateau):
    def __init__(self, ligne, colonne, vertical=False):
        super().__init__(ligne, colonne, longueur=2, vertical=vertical, marque='🐟')    