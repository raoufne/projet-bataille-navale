class Grille:
    def __init__(self, nombre_lignes, nombre_colonnes):
        self.nombre_lignes = nombre_lignes
        self.nombre_colonnes = nombre_colonnes
        self.vide = '∿'
        self.touche_car = 'x'
        self.matrice = [self.vide] * (self.nombre_lignes * self.nombre_colonnes)

    def _index(self, ligne, colonne):
        return ligne * self.nombre_colonnes + colonne

    def _coord_valide(self, ligne, colonne):
        return 0 <= ligne < self.nombre_lignes and 0 <= colonne < self.nombre_colonnes

    def tirer(self, ligne, colonne, touche=None):
        if touche is None:
            touche = self.touche_car
        if not self._coord_valide(ligne, colonne):
            return False
        self.matrice[self._index(ligne, colonne)] = touche
        return True

    def __str__(self):
        lignes = []
        for r in range(self.nombre_lignes):
            start = r * self.nombre_colonnes
            end = start + self.nombre_colonnes
            lignes.append(''.join(self.matrice[start:end]))
        return '\n'.join(lignes)
