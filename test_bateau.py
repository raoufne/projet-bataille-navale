from bateau import Bateau

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

def test_positions_horizontal():
    b = Bateau(2, 3, longueur=3)
    attendu = [(2, 3), (2, 4), (2, 5)]
    assert b.positions() == attendu, f"Attendu {attendu}, obtenu {b.positions()}"

def test_positions_vertical():
    b = Bateau(2, 3, longueur=3, vertical=True)
    attendu = [(2, 3), (3, 3), (4, 3)]
    assert b.positions() == attendu, f"Attendu {attendu}, obtenu {b.positions()}"
