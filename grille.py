class Grille:

    def __init__(self, nb_lignes: int, nb_colonnes: int):
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.liste = ['∿'] * (nb_lignes * nb_colonnes)

    def tirer(self, ligne: int, colonne: int, touche: str = 'x'):
        index = ligne * self.nb_colonnes + colonne
        self.liste[index] = touche
        
    def __str__(self):
        result = []
        for l in range(self.nb_lignes):
            ligne = self.liste[l * self.nb_colonnes:(l + 1) * self.nb_colonnes]
            result.append(''.join(ligne))
        return '\n'.join(result)
 
    def ajoute(self, bateau):
        for ligne, colonne in bateau.positions:
            if not (0 <= ligne < self.nb_lignes and 0 <= colonne < self.nb_colonnes):
                return
        for ligne, colonne in bateau.positions:
            index = ligne * self.nb_colonnes + colonne
            self.liste[index] = bateau.marque    