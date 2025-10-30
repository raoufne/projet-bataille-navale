from grille import Grille
from bateau import Bateau

print("=== Test de la fonctionnalité : tir et coulage d’un bateau ===")

g = Grille(5, 5)

b = Bateau(2, 1, longueur=3, vertical=False)

g.ajoute(b)

print("Grille avec le bateau placé :")
print(g)
print()

print("Tir sur une case vide (0, 0)")
g.tirer(0, 0)
print(g)
print()

print("Tir sur une case du bateau (2, 2)")
g.tirer(2, 2, touche='💣')
print(g)
print("Bateau coulé ?", b.coule(g))
print()

print("Tir sur toutes les cases du bateau pour le couler :")
for (l, c) in b.positions:
    g.tirer(l, c, touche='💣')

print(g)
print("Bateau coulé ?", b.coule(g))
print()