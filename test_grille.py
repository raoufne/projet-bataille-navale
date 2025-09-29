import pytest
from grille import Grille

def test_init():
    g = Grille(5, 8)
    assert g.nombre_lignes == 5
    assert g.nombre_colonnes == 8
    assert len(g.matrice) == 5*8
    assert all(c == g.vide for c in g.matrice)

def test_tirer():
    g = Grille(2, 2)
    assert g.tirer(0,0)
    assert g.matrice[0] == 'x'
    assert not g.tirer(-1,0)
    assert not g.tirer(0,3)

def test_str():
    g = Grille(2,3)
    expected = '\n'.join(['∿'*3, '∿'*3])
    assert str(g)==expected
    g.tirer(1,2)
    assert 'x' in str(g)
