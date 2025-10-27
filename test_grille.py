from grille import Grille
import pytest

def test_init_basic():
    g = Grille()
    assert isinstance(g, Grille), "L'objet créé n'est pas une instance de Grille."


def test_init_dimensions_defaults():
    g = Grille()
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
    assert all(cell == g.vide for cell in g.liste), "Toutes les cases devraient être vierges au départ."


def test_tirer_case_unique():
    g = Grille(5, 8)
    ligne, colonne = 2, 3
    index = ligne * g.nb_colonnes + colonne

    g.tirer(ligne, colonne)
    assert g.liste[index] == g.touche, "La case tirée devrait contenir le symbole 'x'."

    # Toutes les autres cases restent vierges
    for i, val in enumerate(g.liste):
        if i != index:
            assert val == g.vide, f"La case {i} devrait rester vierge."


def test_tirer_differentes_positions():
    g = Grille(3, 3)
    positions = [(0, 0), (1, 2), (2, 1)]

    for ligne, colonne in positions:
        g.tirer(ligne, colonne)

    for l in range(g.nb_lignes):
        for c in range(g.nb_colonnes):
            index = l * g.nb_colonnes + c
            if (l, c) in positions:
                assert g.liste[index] == g.touche, f"Case ({l},{c}) devrait être frappée"
            else:
                assert g.liste[index] == g.vide, f"Case ({l},{c}) devrait rester vierge"


def test_grille_independante():
    g1 = Grille(2, 2)
    g2 = Grille(2, 2)
    g1.tirer(0, 0)
    assert g2.liste == [g2.vide] * 4, "L'autre grille ne doit pas être affectée"
