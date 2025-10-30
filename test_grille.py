import pytest
from grille import Grille
from bateau import Bateau

def test_init_basic():
    g = Grille(0,0)
    assert isinstance(g, Grille), "L'objet créé n'est pas une instance de Grille."


def test_init_dimensions_defaults():
    g = Grille(5,8)
    assert g.nb_lignes == 5, f"Nombre de lignes attendu : 5, obtenu : {g.nb_lignes}"
    assert g.nb_colonnes == 8, f"Nombre de colonnes attendu : 8, obtenu : {g.nb_colonnes}"


def test_init_custom_dimensions():
    g = Grille(3, 4)
    assert g.nb_lignes == 3, "La grille ne conserve pas le bon nombre de lignes."
    assert g.nb_colonnes == 4, "La grille ne conserve pas le bon nombre de colonnes."


def test_init_invalid_dimensions():
    g = Grille(0, -5)
    assert isinstance(g, Grille), "Créer une grille avec des valeurs invalides plante le code."


def test_multiple_instances_are_independent():
    g1 = Grille(5, 5)
    g2 = Grille(10, 10)

    g1.nb_lignes = 99
    assert g2.nb_lignes != g1.nb_lignes, (
        "Les deux grilles partagent les mêmes attributs, ce qui ne devrait pas être le cas."
    )

def test_init_liste_vide():
    g = Grille(5, 8)
    assert all(cell == '∿' for cell in g.liste), "Toutes les cases devraient être vierges au départ."


def test_tirer_case_unique():
    g = Grille(5, 8)
    ligne, colonne = 2, 3
    index = ligne * g.nb_colonnes + colonne

    g.tirer(ligne, colonne)
    assert g.liste[index] == 'x', "La case tirée devrait contenir le symbole 'x'."

    # Toutes les autres cases restent vierges
    for i, val in enumerate(g.liste):
        if i != index:
            assert val == '∿', f"La case {i} devrait rester vierge."


def test_tirer_differentes_positions():
    g = Grille(3, 3)
    positions = [(0, 0), (1, 2), (2, 1)]

    for ligne, colonne in positions:
        g.tirer(ligne, colonne)

    for l in range(g.nb_lignes):
        for c in range(g.nb_colonnes):
            index = l * g.nb_colonnes + c
            if (l, c) in positions:
                assert g.liste[index] == 'x', f"Case ({l},{c}) devrait être frappée"
            else:
                assert g.liste[index] == '∿', f"Case ({l},{c}) devrait rester vierge"


def test_grille_independante():
    g1 = Grille(2, 2)
    g2 = Grille(2, 2)
    g1.tirer(0, 0)
    assert g2.liste == ['∿'] * 4, "L'autre grille ne doit pas être affectée"

def test_str_affichage():
    g = Grille(5, 8)

    attendu_initial = ('∿' * 8 + '\n') * 5
    attendu_initial = attendu_initial.rstrip() 
    assert str(g) == attendu_initial, "Grille initiale incorrecte"

    g.tirer(2, 3)

    lignes = []
    for l in range(5):
        ligne = []
        for c in range(8):
            if l == 2 and c == 3:
                ligne.append('x')
            else:
                ligne.append('∿')
        lignes.append(''.join(ligne))
    attendu_apres_tir = '\n'.join(lignes)

    assert str(g) == attendu_apres_tir, "Affichage après tir incorrect"

def test_ajoute_bateau_horizontal():
    g = Grille(2, 3)
    b = Bateau(1, 0, longueur=2, vertical=False)
    g.ajoute(b)
    attendu = ["∿", "∿", "∿", "⛵", "⛵", "∿"]
    assert g.liste == attendu, f"Grille incorrecte après ajout : {g.liste}"

def test_ajoute_bateau_vertical_hors_grille():
    g = Grille(2, 3)
    b = Bateau(1, 0, longueur=2, vertical=True)
    g.ajoute(b)
    attendu = ["∿", "∿", "∿", "∿", "∿", "∿"]
    assert g.liste == attendu, "La grille ne doit pas changer pour un bateau hors limite"

def test_ajoute_bateau_trop_long():
    g = Grille(2, 3)
    b = Bateau(1, 0, longueur=4, vertical=True)
    g.ajoute(b)
    attendu = ["∿", "∿", "∿", "∿", "∿", "∿"]
    assert g.liste == attendu, "La grille ne doit pas changer pour un bateau trop long"

def test_tir_personnalise():
    g = Grille(2, 2)
    g.tirer(0, 1, touche='*')
    assert g.liste[1] == '*', "Le tir personnalisé n'a pas été appliqué correctement"    