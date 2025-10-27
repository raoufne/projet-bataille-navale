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