class Bateau:

    def __init__(self, ligne: int, colonne: int, longueur: int = 1, vertical: bool = False):
        self.ligne = ligne       
        self.colonne = colonne   
        self.longueur = longueur 
        self.vertical = vertical 

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