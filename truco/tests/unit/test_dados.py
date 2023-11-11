try:
    import pandas as pd
    import os
except ImportError:
    assert False

from truco.dados import Dados
from truco.carta import Carta
import pytest

@pytest.fixture
def dados():
    return Dados()

@pytest.fixture
def colunas():
    return ['idMao', 'jogadorMao', 'cartaAltaRobo', 'cartaMediaRobo', 'cartaBaixaRobo', 'cartaAltaHumano', 'cartaMediaHumano', 'cartaBaixaHumano', 'primeiraCartaRobo', 'primeiraCartaHumano', 'segundaCartaRobo', 'segundaCartaHumano', 'terceiraCartaRobo', 'terceiraCartaHumano', 'ganhadorPrimeiraRodada', 'ganhadorSegundaRodada', 'ganhadorTerceiraRodada', 'quemPediuEnvido', 'quemPediuFaltaEnvido', 'quemPediuRealEnvido', 'pontosEnvidoRobo', 'pontosEnvidoHumano', 'quemNegouEnvido', 'quemGanhouEnvido', 'quemFlor', 'quemContraFlor', 'quemContraFlorResto', 'quemNegouFlor', 'pontosFlorRobo', 'pontosFlorHumano', 'quemGanhouFlor', 'quemEscondeuPontosEnvido', 'quemEscondeuPontosFlor', 'quemTruco', 'quemRetruco', 'quemValeQuatro', 'quemNegouTruco', 'quemGanhouTruco','quemEnvidoEnvido', 'quemFlor', 'naipeCartaAltaRobo', 'naipeCartaMediaRobo', 'naipeCartaBaixaRobo', 'naipeCartaAltaHumano', 'naipeCartaMediaHumano', 'naipeCartaBaixaHumano', 'naipePrimeiraCartaRobo', 'naipePrimeiraCartaHumano', 'naipeSegundaCartaRobo', 'naipeSegundaCartaHumano', 'naipeTerceiraCartaRobo', 'naipeTerceiraCartaHumano', 'qualidadeMaoRobo', 'qualidadeMaoHumano']

def test_carregar_modelo_zerado(dados, colunas):
    df: pd.DataFrame = dados.carregar_modelo_zerado()
    assert df.shape == (1, 52)
    assert df.index.to_list() == [0]
    
    assert df.columns.to_list() != colunas

def test_tratamento_inicial_df(dados, colunas):
    df = dados.tratamento_inicial_df()
    c = ['naipeCartaAltaRobo', 'naipeCartaMediaRobo','naipeCartaBaixaRobo', 'naipeCartaAltaHumano','naipeCartaMediaHumano', 'naipeCartaBaixaHumano','naipePrimeiraCartaRobo', 'naipePrimeiraCartaHumano',	'naipeSegundaCartaRobo', 'naipeSegundaCartaHumano','naipeTerceiraCartaRobo', 'naipeTerceiraCartaHumano',]
    for i in c:
        assert i in df.columns.to_list()

    for i in df.columns.to_list():
        if i not in c:
            assert df[i].dtype == "int16"

def test_dados(dados, colunas):
    assert dados.colunas == colunas
        
def test_finalizar_partida(dados):
    if os.path.isfile("jogadas.csv"):
        os.remove("jogadas.csv")

    try:
        dados.finalizar_partida()
    except:
        assert False
    
    assert os.path.isfile("jogadas.csv")

    try:
        dados.finalizar_partida()
    except:
        assert False
    
    assert os.path.isfile("jogadas.csv")

def test_retornar_registro(dados):
    assert dados.registro.equals(dados.retornar_registro())

def test_retornar_casos(dados):
    assert dados.casos.equals(dados.retornar_casos())

def test_resetar(dados):
    df_casos = dados.tratamento_inicial_df()
    df_registro = dados.carregar_modelo_zerado()

    try:
        dados.resetar()
    except:
        assert False
    
    assert dados.registro.equals(df_registro)
    assert dados.casos.equals(df_casos)

def test_cartas_jogadas_pelo_bot(dados):
    c1 = Carta('1', "COPAS")
    try:
        dados.cartas_jogadas_pelo_bot("primeira", c1)
    except:
        assert False

    assert dados.registro.primeiraCartaRobo[0] == c1.retornar_numero()
    assert dados.registro.naipePrimeiraCartaRobo[0] == c1.retornar_naipe_codificado()

    try:
        dados.cartas_jogadas_pelo_bot("segunda", c1)
    except:
        assert False
    
    assert dados.registro.segundaCartaRobo[0] == c1.retornar_numero()
    assert dados.registro.naipeSegundaCartaRobo[0] == c1.retornar_naipe_codificado()

    try:
        dados.cartas_jogadas_pelo_bot("terceira", c1)
    except:
        assert False
    
    assert dados.registro.terceiraCartaRobo[0] == c1.retornar_numero()
    assert dados.registro.naipeTerceiraCartaRobo[0] == c1.retornar_naipe_codificado()

def test_primeira_rodada(dados):
    try:
        dados.primeira_rodada([1,2,3], ["Alta", "Media", "Baixa"], 1, Carta('3', "COPAS"))
    except:
        assert False

    assert dados.registro.jogadorMao[0] == 1
    assert dados.registro.cartaAltaRobo[0] == 1
    assert dados.registro.cartaMediaRobo[0] == 2
    assert dados.registro.cartaBaixaRobo[0] == 3
    assert dados.registro.qualidadeMaoBot == 1
    assert dados.registro.primeiraCartaHumano[0] == "3"
    assert dados.registro.naipePrimeiraCartaHumano[0] == 4

def test_segunda_rodada(dados):
    try:
        dados.segunda_rodada(Carta('3', "COPAS"), Carta('4', "BASTOS"), 1)
    except:
        assert False

    assert dados.registro.ganhadorPrimeiraRodada[0] == 1
    assert dados.registro.primeiraCartaHumano[0] == "3"
    assert dados.registro.naipePrimeiraCartaHumano[0] == 4
    assert dados.registro.terceiraCartaRobo[0] == "4"

def test_terceira_rodada(dados):
    try:
        dados.terceira_rodada(Carta('3', "COPAS"), Carta('4', "BASTOS"), 1)
    except:
        assert False

    assert dados.registro.ganhadorSegundaRodada[0] == 1
    assert dados.registro.SegundaCartaHumano[0] == "3"
    assert dados.registro.naipeSegundaCartaHumano[0] == 4
    assert dados.registro.terceiraCartaRobo[0] == "4"

def test_finalizar_rodadas(dados):
    try:
        dados.finalizar_rodadas(Carta('12', "OUROS"), Carta('3', "ESPADAS"), 1)
    except:
        assert False

    assert dados.registro.ganhadorTerceiraRodada[0] == 1
    assert dados.registro.terceiraCartaHumano[0] == "12"
    assert dados.registro.naipeTerceiraCartaHumano[0] == 2
    assert dados.registro.terceiraCartaRobo[0] == "12"

def test_envido(dados):
    try:
        dados.envido(1, 2, 2, 1)
    except:
        assert False

    assert dados.registro.quemEnvido == 1
    assert dados.registro.quemRealEnvido == 2
    assert dados.registro.quemFaltaEnvido == 2
    assert dados.registro.quemGanhouEnvido[0] == 1

def test_truco(dados):
    try:
        dados.truco(1, 2, 2, 1, 1)
    except:
        assert False

    assert dados.registro.quemTruco[0] == 1
    assert dados.registro.quemRetruco[0] == 2
    assert dados.registro.quemValeQuatro[0] == 2
    assert dados.registro.quemNegouTruco[0] == 1
    assert dados.registro.quemGanhouTruco[0] == 1

def test_flor(dados):
    try:
        dados.flor(1, 2, 2, 7)
    except:
        assert False

    assert dados.registro.quemGanhouFlor[0] == 2
    assert dados.registro.quemFlor[0] == 1
    assert dados.registro.quemContraFlor[0] == 2
    assert dados.registro.quemContraFlorResto[0] == 2
    assert dados.registro.pontosFlorRobo[0] == 7

def test_vencedor_envido(dados):
    try:
        dados.vencedor_envido(1, 2)
    except:
        assert False

    assert dados.registro.quemGanhouEnvido[0] == 1
    assert dados.registro.quemNegouEnvido[0] == 2

def test_vencedor_truco(dados):
    try:
        dados.vencedor_truco(1, 2)
    except:
        assert False

    assert dados.registro.quemGanhouTruco[0] == 1
    assert dados.registro.quemNegouTruco[0] == 2

def test_vencedor_flor(dados):
    try:
        dados.vencedor_flor(1, 2)
    except:
        assert False

    assert dados.registro.quemGanhouFlor[0] == 1
    assert dados.registro.quemNegouFlor[0] == 2




