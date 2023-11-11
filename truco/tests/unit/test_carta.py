from truco.carta import Carta
import pytest

@pytest.fixture
def carta():
    c1 = Carta("3", "ESPADAS")
    c2 = Carta("2", "OUROS")
    c3 = Carta("1", "BASTOS")
    return c1, c2, c3

def test_retornar_naipe_codificado(carta):
    c1, c2, c3 = carta
    assert c1.retornar_naipe_codificado() == 1
    assert c2.retornar_naipe_codificado() == 2
    assert c3.retornar_naipe_codificado() == 3

def test_retornar_naipe(carta):
    c1, c2, c3 = carta
    assert c1.retornar_naipe() == "ESPADAS"
    assert c2.retornar_naipe() == "OUROS"
    assert c3.retornar_naipe() == "BASTOS"

def test_retornar_numero(carta):
    c1, c2, c3 = carta
    assert c1.retornar_numero() == "3"
    assert c2.retornar_numero() == "2"
    assert c3.retornar_numero() == "1"

def test_retornar_carta(carta):
    c1, c2, c3 = carta
    assert c1.retornar_carta() == "3 de ESPADAS"
    assert c2.retornar_carta() == "2 de OUROS"
    assert c3.retornar_carta() == "1 de BASTOS"

def test_exibir_carta(carta, capsys):
    c1, c2, c3 = carta
    c1.exibir_carta(i = 1)
    c2.exibir_carta(i = 2)
    c3.exibir_carta(i = None)
    out, err = capsys.readouterr()
    assert out == "[1] 3 de ESPADAS\n[2] 2 de OUROS\n[] 1 de BASTOS\n"

def test_retornar_pontos_carta(carta):
    c1, c2, c3 = carta
    assert c1.retornar_pontos_carta(c1) == 24
    assert c2.retornar_pontos_carta(c2) == 16
    assert c3.retornar_pontos_carta(c3) == 50

def test_verificar_carta_alta(carta):
    c1, c2, c3 = carta
    cError = Carta("3", "PAUS")
    cError2 = Carta("0", "PAUS")
    assert c1.verificar_carta_alta(c1, c2) == c1
    assert c2.verificar_carta_alta(c2, c3) == c3
    assert c3.verificar_carta_alta(c3, c1) == c3
    assert c1.verificar_carta_alta(c1, cError) == cError
    with pytest.raises(KeyError) as e_info:
        c1.verificar_carta_alta(c1, cError2)
    assert str(e_info.value) == "'0'"

def test_verificar_carta_baixa(carta):
    c1, c2, c3 = carta
    cError = Carta("3", "PAUS")
    cError2 = Carta("0", "PAUS")
    assert c1.verificar_carta_baixa(c1, c2) == c2
    assert c2.verificar_carta_baixa(c2, c3) == c2
    assert c3.verificar_carta_baixa(c3, c1) == c1
    assert c1.verificar_carta_baixa(c1, cError) == cError
    with pytest.raises(KeyError) as e_info:
        c1.verificar_carta_baixa(c1, cError2)
    assert str(e_info.value) == "'0'"

def test_classificar_carta(carta):
    c1, c2, c3 = carta
    assert c1.classificar_carta([c1, c2, c3]) == ([24, 16, 50], ['Media', 'Baixa', 'Alta'])
    assert c2.classificar_carta([c2, c3, c1]) == ([16, 50, 24], ['Baixa', 'Alta', 'Media'])
    assert c3.classificar_carta([c3, c1, c2]) == ([50, 24, 16], ['Alta', 'Media', 'Baixa'])
    cError = Carta("3", "PAUS")
    cError2 = Carta("0", "PAUS")

    assert c1.classificar_carta([c1, c2, c3, cError, cError2]) == ([24, 16, 50], ['Media', 'Baixa', 'Alta'])
    with pytest.raises(KeyError) as e_info:
        c1.classificar_carta([c1, c2, cError2, c3, cError2]) == ([24, 16, 50], ['Media', 'Baixa', 'Alta'])
    assert str(e_info.value) == "'0'"

    assert c1.classificar_carta([c1, c1, c1]) == ([24, 24, 24], ['Baixa', 'Baixa', 'Baixa'])
    

