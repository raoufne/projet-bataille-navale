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
