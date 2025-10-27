from grille import Grille

grille = Grille(5, 8)

while True:
    print(grille)
    print()  

    try:
        x = int(input("Entrez la coordonnée X (colonne, 0-indexée) : "))
        y = int(input("Entrez la coordonnée Y (ligne, 0-indexée) : "))
    except ValueError:
        print("Veuillez entrer des nombres valides !")
        continue

    grille.tirer(y, x)
