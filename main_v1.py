from grille import Grille
from bateau import PorteAvion, Croiseur, Torpilleur, SousMarin
from score_helper import load_highscores, save_highscores


playing = True
gagne = 0

difficultes = {
    "C": {"nom": "Facile", "desc": "Grille standard, 4 bateaux, coups illimités."},
    "B": {"nom": "Moyen", "desc": "Grille standard, 4 bateaux, 40 coups maximum."},
    "A": {"nom": "Difficile", "desc": "Grille standard, 4 bateaux, 40 coups, les bateaux se repositionnent après chaque tir."}
}

while playing:

    g = Grille(8, 10)
    liste_bateaux = [PorteAvion(0, 0), Croiseur(0, 0), Torpilleur(0, 0), SousMarin(0, 0)]
    
    print("\nChoisissez la difficulté :")
    for cle, info in difficultes.items():
        print(f"  {cle}: {info['nom']} - {info['desc']}")
    
    while True:
        diff = input("➡ Votre choix : ").upper()
        if diff in difficultes:
            break
        else:
            print("⚠️  Veuillez entrer une difficulté valide !")

    if diff == 'C':
        max_coups = g.nb_lignes * g.nb_colonnes + 1
        print("Mode Facile : coups illimités.")
    elif diff == 'B':
        max_coups = g.nb_lignes * g.nb_colonnes // 2
        print(f"Mode Moyen : {max_coups} coups maximum.")
    elif diff == 'A':
        max_coups = g.nb_lignes * g.nb_colonnes // 2
        print(f"Mode Difficile : {max_coups} coups et repositionnement après chaque tir.")
    elif diff == 'Z':
        g = Grille(int(g.nb_lignes * 1.5), int(g.nb_colonnes * 1.5))
        liste_bateaux.append(SousMarin(0, 0))
        max_coups = 40
        print(f"Mode Extrême activé : taille plus grand, un sous-marin supplémentaire, repositionnement et toujours {max_coups} coups !")
    
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
    cases_deja_tirees = []
    bateaux_coules = []
    bateaux_touches = []

    while True:
        print("\nGrille :")
        print(g)
        print()

        try:
            cell = input("Entrez la position (ex: A1) : ").strip().upper()
            if len(cell) < 2:
                raise ValueError("Format invalide.")
            
            letter = cell[0]
            number_part = cell[1:]

            if not letter.isalpha() or not number_part.isdigit():
                raise ValueError("Format invalide.")

            x = ord(letter) - ord('A')  
            y = int(number_part) - 1
        
        except ValueError as e:
            print(f"⚠️  Veuillez entrer une position valide ! ({e})")    
            continue
        
        if not (0 <= x < g.nb_lignes and 0 <= y < g.nb_colonnes):
            print("🚫 Coordonnées hors grille !")
            continue

        if (x, y) in cases_deja_tirees:
            print("⛔ Vous avez déjà tiré ici !")
            continue

        cases_deja_tirees.append((x, y))
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

            if touche_bateau.coule(g):
                bateaux_coules.append(touche_bateau)
                g.ajoute(touche_bateau)
                if len(bateaux_coules) != len(liste_bateaux):
                    message = f"🎯 Bravo ! Vous avez coulé le bateau {touche_bateau.marque} !"
                    if diff == 'Z':
                        coups -= 5
                        message += "(5 coups supplimentaires)"

                    elif diff == 'A':
                        coups -= 1
                        message += "(1 coup supplimentaire)"              
                    print(message)

            else:
                print("🔥 Touché ! Continuez...")
                bateaux_touches.append(touche_bateau)        
        else:
            g.tirer(x, y)
            print("💧 Plouf ! Dans l’eau...")
        if diff == 'A' or diff == 'Z':
            positions_occupees = list(cases_deja_tirees) + [pos for b_temps in bateaux_touches for pos in b_temps.positions if pos not in cases_deja_tirees]
            for b in liste_bateaux:
                if b not in bateaux_touches:
                    b.position_alea(g, positions_occupees)
                    positions_occupees.extend(b.positions)

        if len(bateaux_coules) == len(liste_bateaux) or coups == max_coups:
            if len(bateaux_coules) == len(liste_bateaux):
                print("\n🏁 Félicitations ! Tous les bateaux ont été détruits !")
                print(f"Nombre total de coups : {coups}")

                if best is None or coups < best:
                    scores[diff] = coups
                    save_highscores(scores)
                    print(f"🏆 Nouveau record pour la difficulté {difficultes[diff]['nom']} ({coups} coups) !")
                
                if diff == 'A':
                    gagne += 1
                    if gagne == 2:
                        print("🎉 Félicitations ! Vous avez gagné 2 parties en difficulté Difficile sans perdre ! Une nouvelle difficulté 'Extrême' est débloquée.")
                        difficultes["Z"] = {
                            "nom": "Extrême",
                            "desc": "Grille plus grande, repositionnement et 40 coups maximum, 5 bateaux !"
                        }

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
            
            while True:
                replay = input("Voulez-vous rejouer ? (O/N) : ").strip().upper()
                if replay not in ['O', 'N']:
                    print("⚠️  Veuillez répondre par O (oui) ou N (non).")
                else:
                    break    
            if replay == 'N':
                playing = False
            break
