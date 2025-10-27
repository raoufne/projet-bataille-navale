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
        else:  # horizontal
            for i in range(self.longueur):
                pos.append((self.ligne, self.colonne + i))
        return pos

    def coule(self, grille):
        for ligne, colonne in self.positions:
            index = ligne * grille.nb_colonnes + colonne
            if grille.liste[index] != 'x':
                return False
        return True    
    
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