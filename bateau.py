class Bateau:

    def __init__(self, ligne: int, colonne: int, longueur: int = 1, vertical: bool = False):
        self.ligne = ligne       
        self.colonne = colonne   
        self.longueur = longueur 
        self.vertical = vertical 