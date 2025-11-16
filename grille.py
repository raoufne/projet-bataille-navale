from wcwidth import wcswidth
class Grille:

    def __init__(self, nb_lignes: int, nb_colonnes: int):
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.vide = '🌊'
        self.liste = [self.vide] * (nb_lignes * nb_colonnes)

    def tirer(self, ligne: int, colonne: int, touche: str = '❌'):
        index = ligne * self.nb_colonnes + colonne
        self.liste[index] = touche
        
    def __str__(self):
        largeur_max = 0
        for case in self.liste:
            largeur_case = wcswidth(case)
            if largeur_case > largeur_max:
                largeur_max = largeur_case

        def pad_visuel(texte, largeur):
            largeur_actuelle = wcswidth(texte)
            return texte + " " * (largeur - largeur_actuelle)

        entete = " " * 3
        for num in range(1, self.nb_colonnes + 1):
            entete += pad_visuel(str(num), largeur_max) + " "

        lignes = [entete]

        for r in range(self.nb_lignes):
            etiquette = chr(ord('A') + r) + "  "
            cases = self.liste[r * self.nb_colonnes:(r + 1) * self.nb_colonnes]

            cases_formatees = [pad_visuel(c, largeur_max) for c in cases]

            lignes.append(etiquette + " ".join(cases_formatees))

        return "\n".join(lignes)
 
    def ajoute(self, bateau):
        for ligne, colonne in bateau.positions:
            if not (0 <= ligne < self.nb_lignes and 0 <= colonne < self.nb_colonnes):
                return
        for ligne, colonne in bateau.positions:
            index = ligne * self.nb_colonnes + colonne
            self.liste[index] = bateau.marque    