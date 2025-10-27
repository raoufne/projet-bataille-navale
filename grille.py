class Grille:

    def __init__(self, nb_lignes: int, nb_colonnes: int):
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.vide = '∿'
        self.touche = 'x'
        self.liste = [self.vide] * (nb_lignes * nb_colonnes)

    def tirer(self, ligne: int, colonne: int):
        if 0 <= ligne < self.nb_lignes and 0 <= colonne < self.nb_colonnes:
            index = ligne * self.nb_colonnes + colonne
            self.liste[index] = self.touche
        else:
            raise ValueError(f"Coordonnées hors grille : ({ligne}, {colonne})")
        
    def __str__(self):
        result = []
        for l in range(self.nb_lignes):
            ligne = self.liste[l * self.nb_colonnes:(l + 1) * self.nb_colonnes]
            result.append(''.join(ligne))
        return '\n'.join(result)