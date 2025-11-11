from grille import Grille
from bateau import PorteAvion, Croiseur, Torpilleur, SousMarin
import json
import os

playing = True
gagne = 0

difficultes = {
    "C": {"nom": "Facile", "desc": "Grille standard, coups illimités."},
    "B": {"nom": "Moyen", "desc": "Grille standard, 40 coups maximum."},
    "A": {"nom": "Difficile", "desc": "Grille standard, 40 coups, les bateaux se repositionnent après chaque tir."}
}

HIGHSCORE_FILE = "highscores.json"

if not os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump({"C": None, "B": None, "A": None, "Z": None}, f)

def load_highscores():
    with open(HIGHSCORE_FILE, "r") as f:
        return json.load(f)

def save_highscores(scores):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)


while playing:
    if gagne == 2:
        print("🎉 Félicitations ! Vous avez gagné 2 parties en difficulté Difficile sans perdre ! Une nouvelle difficulté 'Extrême' est débloquée.")
        difficultes["Z"] = {
            "nom": "Extrême",
            "desc": "Grille 50% plus grande, 40 coups maximum, 5 bateaux !"
        }

    g = Grille(8, 10)
    liste_bateaux = [PorteAvion(0, 0), Croiseur(0, 0), Torpilleur(0, 0), SousMarin(0, 0)]
    
    print("\nChoisissez la difficulté :")
    for cle, info in difficultes.items():
        print(f"  {cle}: {info['nom']} - {info['desc']}")
    
    try:
        diff = input("➡ Votre choix : ").upper()

        if diff not in difficultes:
            raise ValueError("Difficulté invalide !")

        if diff == 'C':
            max_coups = g.nb_lignes * g.nb_colonnes
            print("Mode Facile : coups illimités.")
        elif diff == 'B':
            max_coups = 40
            print("Mode Moyen : 40 coups maximum.")
        elif diff == 'A':
            max_coups = 40
            print("Mode Difficile : 40 coups et repositionnement après chaque tir.")
        elif diff == 'Z':
            g = Grille(int(g.nb_lignes * 1.5), int(g.nb_colonnes * 1.5))
            liste_bateaux.append(SousMarin(0, 0))
            max_coups = 40
            print("Mode Extrême activé : +50% de taille, un sous-marin supplémentaire, et toujours 40 coups !")

    except ValueError:
        print("⚠️  Veuillez entrer une difficulté valide !")
        continue
    
    scores = load_highscores()
    best = scores.get(diff)
    if best is not None:
        print(f"🏆 Meilleur score pour la difficulté {difficultes[diff]['nom']} : {best} coups.")
    else:
        print(f"🏆 Aucun score enregistré pour la difficulté {difficultes[diff]['nom']}.")


    positions_occupees = []

    for b in liste_bateaux:
        b.position_alea(g, positions_occupees)
        positions_occupees.extend(b.positions)

    coups = 0
    cases_deja_tirees = set()
    bateaux_coules = []
    finish = len(bateaux_coules) == len(liste_bateaux) or coups == max_coups

    while True:
        print("\nGrille :")
        print(g)
        print()

        try:
            x = int(input("Entrez la ligne X : ")) - 1
            y = int(input("Entrez la colonne Y : ")) - 1
        except ValueError:
            print("⚠️  Veuillez entrer des nombres valides !")
            continue

        if not (0 <= x < g.nb_lignes and 0 <= y < g.nb_colonnes):
            print("🚫 Coordonnées hors grille !")
            continue

        if (x, y) in cases_deja_tirees:
            print("⛔ Vous avez déjà tiré ici ! Choisissez une autre case.")
            continue

        cases_deja_tirees.add((x, y))
        coups += 1

        touche_bateau = None
        for b in liste_bateaux:
            if b in bateaux_coules:
                continue
            if (x, y) in b.positions:
                touche_bateau = b
                break

        if touche_bateau:
            g.tirer(x, y, touche='💣')
            print("🔥 Touché !")

            if touche_bateau.coule(g):
                bateaux_coules.append(touche_bateau)
                g.ajoute(touche_bateau)
                if len(bateaux_coules) != len(liste_bateaux):
                    print(f"🎯 Bravo ! Vous avez coulé le bateau {touche_bateau.marque} !")
        else:
            g.tirer(x, y)
            print("💧 Plouf ! Dans l’eau...")

        if finish:
            if len(bateaux_coules) == len(liste_bateaux):
                print("\n🏁 Félicitations ! Tous les bateaux ont été détruits !")
                print(f"Nombre total de coups : {coups}")

                if diff == 'A':
                    gagne += 1

                if best is None or coups < best:
                    scores[diff] = coups
                    save_highscores(scores)
                    print(f"🏆 Nouveau record pour la difficulté {difficultes[diff]['nom']} ({coups} coups) !")

            elif coups == max_coups:
                print("\n❌ Game Over ! Vous avez épuisé votre nombre de coups.")
                print("Les bateaux restants étaient aux positions suivantes :")
                for b in liste_bateaux:
                    if b not in bateaux_coules:
                        g.ajoute(b)
                gagne = 0

                if 'Z' in difficultes:
                    del difficultes['Z']


            print("\nGrille finale :")
            print(g)
            
            try:
                replay = input("Voulez-vous rejouer ? (O/N) : ").strip().upper()
            except replay not in ['O', 'N']:
                print("⚠️  Veuillez répondre par O (oui) ou N (non).")
            
            if replay == 'N':
                playing = False
            break
