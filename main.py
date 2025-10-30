import random
from grille import Grille
from bateau import PorteAvion, Croiseur, Torpilleur, SousMarin

g = Grille(8, 10)

liste_bateaux = [PorteAvion(0,0), Croiseur(0,0), Torpilleur(0,0), SousMarin(0,0)]

for b in liste_bateaux:
    positions_valides = []

    for ligne in range(g.nb_lignes):
        for colonne in range(g.nb_colonnes):
            for vertical in [False, True]:
                b_temp = type(b)(ligne, colonne, vertical=vertical)
                if all(0 <= l < g.nb_lignes and 0 <= c < g.nb_colonnes for l, c in b_temp.positions):
                    chevauche = False
                    for l, c in b_temp.positions:
                        if g.liste[l * g.nb_colonnes + c] != '∿':
                            chevauche = True
                            break
                    if not chevauche:
                        positions_valides.append((ligne, colonne, vertical))

    if positions_valides:
        ligne, colonne, vertical = random.choice(positions_valides)
        b.ligne = ligne
        b.colonne = colonne
        b.vertical = vertical
    else:
        raise Exception(f"Impossible de placer le bateau {b.marque} !")

coups = 0
cases_deja_tirees = set() 
bateaux_coules = [] 

while True:
    print("\nGrille :")
    print(g)
    print()

    try:
        x = int(input("Entrez la coordonnée X (ligne, 0-indexée) : "))
        y = int(input("Entrez la coordonnée Y (colonne, 0-indexée) : "))
    except ValueError:
        print(" Veuillez entrer des nombres valides !")
        continue

    if not (0 <= y < g.nb_lignes and 0 <= x < g.nb_colonnes):
        print(" Coordonnées hors grille !")
        continue

    if (y, x) in cases_deja_tirees:
        print(" Vous avez déjà tiré ici ! Choisissez une autre case.")
        continue

    cases_deja_tirees.add((y, x))
    coups += 1

    touche_bateau = None
    for b in liste_bateaux:
        if b in bateaux_coules:
            continue
        if (y, x) in b.positions:
            touche_bateau = b
            break

    if touche_bateau:
        g.tirer(y, x, touche='💣')
        print("🔥 Touché !")

        if touche_bateau.coule(g):
            bateaux_coules.append(touche_bateau)
            print(f"🎯 Bravo ! Vous avez coulé le bateau {touche_bateau.marque} !")
            for l, c in touche_bateau.positions:
                g.tirer(l, c, touche_bateau.marque)
    else:
        g.tirer(y, x)
        print("💧 Plouf ! Dans l’eau...")

    # --- Vérifier si tout est coulé ---
    if len(bateaux_coules) == len(liste_bateaux):
        print("\n🏁 Félicitations ! Tous les bateaux ont été détruits !")
        print(f"Nombre total de coups : {coups}")
        print("\nGrille finale :")
        print(g)
        break
