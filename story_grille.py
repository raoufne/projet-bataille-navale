from grille import Grille

g = Grille(5, 8)
print("Grille initiale :")
print(g)
try:
    x = int(input("Entrez la ligne : "))
    y = int(input("Entrez la colonne : "))
except Exception:
    print("Coordonnées invalides")
    exit()

if g.tirer(x, y):
    print("Tir effectué")
else:
    print("Coordonnées hors grille")

print("Grille après le tir :")
print(g)
