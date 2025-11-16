import pytest
from bateau import Bateau, PorteAvion, Croiseur, Torpilleur, SousMarin
from grille import Grille


def test_bateau_init_defaults():
    b = Bateau(2, 3)
    assert b.ligne == 2, "La ligne de départ est incorrecte"
    assert b.colonne == 3, "La colonne de départ est incorrecte"
    assert b.longueur == 1, "La longueur par défaut devrait être 1"
    assert b.vertical is False, "L'orientation par défaut devrait être horizontale (False)"

def test_bateau_custom_values():
    b = Bateau(0, 0, longueur=4, vertical=True)
    assert b.ligne == 0
    assert b.colonne == 0
    assert b.longueur == 4
    assert b.vertical is True

def test_positions_horizontal_property():
    b = Bateau(2, 3, longueur=3)
    attendu = [(2, 3), (2, 4), (2, 5)]
    assert b.positions == attendu, f"Attendu {attendu}, obtenu {b.positions}"

def test_positions_vertical_property():
    b = Bateau(2, 3, longueur=3, vertical=True)
    attendu = [(2, 3), (3, 3), (4, 3)]
    assert b.positions == attendu, f"Attendu {attendu}, obtenu {b.positions}"

def test_bateau_coule():
    g = Grille(2, 3)
    b = Bateau(1, 0, longueur=2, vertical=False)
    g.ajoute(b)
    assert b.coule(g) is False, "Bateau non touché ne doit pas être coulé"
    g.tirer(1, 0,  touche='💣')
    assert b.coule(g) is False, "Bateau partiellement touché ne doit pas être coulé"
    g.tirer(1, 1,  touche='💣')
    assert b.coule(g) is True, "Bateau totalement touché doit être coulé"

def test_types_bateaux_sur_grille():
    g = Grille(5, 5)
    bateaux = [
        PorteAvion(0, 0),
        Croiseur(1, 0),
        Torpilleur(2, 0),
        SousMarin(3, 0)
    ]
    for b in bateaux:
        for ligne, colonne in b.positions:
            index = ligne * g.nb_colonnes + colonne
            g.liste[index] = b.marque
    assert g.liste[0] == '🚢', "Porte-avion incorrectement placé"
    assert g.liste[5] == '⛴', "Croiseur incorrectement placé"
    assert g.liste[10] == '🚣', "Torpilleur incorrectement placé"
    assert g.liste[15] == '🐟', "Sous-marin incorrectement placé"    

def test_position_alea():
    g = Grille(8, 10)
    b = Bateau(0, 0, longueur=3)

    b.position_alea(g, positions_occupees=[])

    for (l, c) in b.positions:
        assert 0 <= l < g.nb_lignes
        assert 0 <= c < g.nb_colonnes

    if b.vertical:
        assert b.positions[-1][0] - b.positions[0][0] == b.longueur - 1
        assert all(c == b.colonne for (_, c) in b.positions)
    else:
        assert b.positions[-1][1] - b.positions[0][1] == b.longueur - 1
        assert all(l == b.ligne for (l, _) in b.positions)

    assert all(True for p in b.positions)
