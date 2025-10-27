class Grille:
    def __init__(self, nb_lignes: int, nb_colonnes: int):
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.liste = ['.'] * (nb_lignes * nb_colonnes)
