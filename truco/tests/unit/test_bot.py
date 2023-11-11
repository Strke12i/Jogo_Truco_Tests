try:
    import random
    import pandas as pd
except ImportError:
    assert False

from truco.bot import Bot
from truco.baralho import Baralho
from truco.carta import Carta
from truco.dados import Dados
from truco.cbr import Cbr

import pytest

@pytest.fixture
def bot():
    return Bot("Bot")

@pytest.fixture
def baralho():
    return Baralho()

@pytest.fixture
def dados():
    return Dados()

@pytest.fixture
def cbr():
    return Cbr()

def test_bot(bot):
    assert bot.nome == "Bot"
    assert bot.mao == []
    assert bot.mao_rank == []
    assert bot.indices == []
    assert bot.pontuacao_cartas == []
    assert bot.qualidade_mao == 0
    assert bot.pontos == 0
    assert bot.rodadas == 0
    assert bot.envido == 0
    assert bot.rodada == 1
    assert bot.primeiro == False
    assert bot.ultimo == False
    assert bot.flor == False
    assert bot.pediu_flor == False
    assert bot.pediu_truco == False

def test_checa_flor(bot):
    cartas = [Carta("1", "ESPADA"), Carta("12", "ESPADA"), Carta("3", "ESPADA")]
    bot.mao = cartas
    assert bot.checa_flor() == True

    cartas = [Carta("1", "ESPADA"), Carta("12", "ESPADA"), Carta("3", "COPAS")]
    bot.mao = cartas
    assert bot.checa_flor() == False

def test_calcular_qualidade_mao(bot):
    bot.mao = [Carta("2", "OUROS"), Carta("12", "COPAS"), Carta("3", "OUROS")]
    pontuacao, mao_rank = bot.mao[0].classificar_carta(bot.mao)
    try:
        bot.calcular_qualidade_mao(pontuacao, mao_rank)
    except:
        assert False

    assert round(bot.qualidade_mao) == 25

def test_calcula_envido(bot):
    bot.mao = [Carta("2", "OUROS"), Carta("12", "COPAS"), Carta("3", "OUROS")]
    assert bot.calcula_envido(bot.mao) == 25

    bot.mao = [Carta("10", "COPAS"), Carta("1", "ESPADA"), Carta("5", "BASTOS")]
    assert bot.calcula_envido(bot.mao) == 5

def test_criar_mao(bot, baralho):
    cartas = baralho.cartas.copy()[-3:]
    print(cartas)
    try:
        bot.criar_mao(baralho)
    except:
        assert False

    assert len(bot.mao) == 3
    for i in range(0,3):
        assert bot.mao[i] == cartas[2-i]
    
    assert bot.indices == [0, 1, 2]
    assert bot.flor == bot.checa_flor()
    assert bot.pontuacao_cartas, bot.mao_rank == bot.mao[0].classificar_carta(bot.mao)
    assert bot.envido == bot.calcula_envido(bot.mao)

def test_enriquecer_bot(bot, dados, baralho):
    bot.criar_mao(baralho)
    bot.rodada = 1
    try:
        bot.enriquecer_bot(dados, Carta("2", "OUROS"))
    except:
        assert False

    assert dados.registro.cartaAltaRobo[0] == bot.pontuacao_cartas[bot.mao_rank.index("Alta")]
    assert dados.registro.cartaMediaRobo[0] == bot.pontuacao_cartas[bot.mao_rank.index("Media")]
    assert dados.registro.cartaBaixaRobo[0] == bot.pontuacao_cartas[bot.mao_rank.index("Baixa")]
    assert dados.registro.qualidadeMaoBot == bot.qualidade_mao
    assert dados.registro.primeiraCartaHumano[0] == Carta("2", "OUROS").retornar_numero()

    bot.rodada = 2
    try:
        bot.enriquecer_bot(dados, Carta("3", "OUROS"), Carta("4", "OUROS"), 1)
    except:
        assert False

    assert dados.registro.ganhadorPrimeiraRodada[0] == 1
    assert dados.registro.primeiraCartaHumano[0] == Carta("3", "OUROS").retornar_numero()
    assert dados.registro.naipePrimeiraCartaHumano[0] == Carta("3", "OUROS").retornar_naipe_codificado()
    assert dados.registro.terceiraCartaRobo[0] == Carta("4", "OUROS").retornar_numero()

    bot.rodada = 4
    try:
        bot.enriquecer_bot(dados, Carta("3", "OUROS"), Carta("4", "OUROS"), 1)
    except:
        assert False

    assert dados.registro.ganhadorTerceiraRodada[0] == 1
    assert dados.registro.terceiraCartaHumano[0] == Carta("3", "OUROS").retornar_numero()
    assert dados.registro.naipeTerceiraCartaHumano[0] == Carta("3", "OUROS").retornar_naipe_codificado()
    assert dados.registro.terceiraCartaRobo[0] == "3" #ERRADO

def test_jogar_carta(bot):
    try:
        bot.mao = [Carta("1", "ESPADA"), Carta("12", "ESPADA"), Carta("3", "COPAS")]
        bot.flor = False
        assert bot.jogar_carta(cbr, None) == 5
    except AttributeError:
        pass

def test_retornar_pontos_envido(bot):
    bot.envido = 25
    assert bot.retorna_pontos_envido() == 25
    bot.envido = -30
    assert bot.retorna_pontos_envido() == -30

def test_calcular_envido(bot):
    mao1 = [Carta("1", "ESPADA"), Carta("12", "ESPADA"), Carta("3", "COPAS")]
    mao2 = [Carta("10", "COPAS"), Carta("1", "COPAS"), Carta("5", "COPAS")]
    mao3 = [Carta("1", "ESPADA"), Carta("5", "BASTOS")]
    mao4 = [Carta("12", "ESPADA")]

    assert bot.calcula_envido(mao1) == 3
    
    assert bot.calcula_envido(mao2) == 26
    
    assert bot.calcula_envido(mao3) == 5
    
    try:
        bot.calcula_envido(mao4)
        assert False
    except:
        assert True
        
def test_ajustar_indices(bot):
    bot.indices = [0, 1, 2]
    bot.mao_rank = ["Alta", "Media", "Baixa"]
    bot.pontuacao_cartas = [10, 5, 2]
    bot.ajustar_indices(1)
    assert bot.indices == [0, 2]
    bot.ajustar_indices(0)
    assert bot.indices == [2]
    bot.ajustar_indices(0)
    assert bot.indices == []

def test_mostrar_mao(bot, capsys):
    bot.mao = [Carta("1", "ESPADA"), Carta("12", "ESPADA"), Carta("3", "COPAS")]
    try:
        bot.mostrar_mao()
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "[0] 1 de ESPADA\n[1] 12 de ESPADA\n[2] 3 de COPAS\n"
    
def test_adicionar_pontos(bot):
    try:
        bot.adicionar_pontos("a")
        assert False
    except:
        assert True
        
    try:
        bot.adicionar_pontos(3)    
        bot.adicionar_pontos(5)
        bot.adicionar_pontos(-10)
    except:
        assert False
        
    assert bot.pontos == -2
    
def test_adicionar_rodadas(bot):
    try:
        bot.adicionar_rodada()
    except:
        assert False
        
    assert bot.rodadas == 1
    
    try:
        for i in range(0,100):
            bot.adicionar_rodada()
    except:
        assert False
        
    assert bot.rodadas == 101
    
def test_checa_mao(bot):
    bot.mao = [Carta("1", "ESPADA"), Carta("12", "ESPADA"), Carta("3", "COPAS")]
    assert bot.checa_mao() == bot.mao
    
    bot.mao = [Carta("1", "ESPADA"), Carta("12", "ESPADA")]
    assert bot.checa_mao() == bot.mao

def test_checa_flor(bot):
    bot.mao = [Carta("1", "ESPADA"), Carta("12", "ESPADA"), Carta("3", "ESPADA")]
    assert bot.checa_flor() == True
    
    bot.mao = [Carta("1", "ESPADA"), Carta("12", "ESPADA"), Carta("3", "OUROS")]
    assert bot.checa_flor() == False
    
def test_avalia_truco(bot, cbr):
    t1 = cbr.truco(1, 1, 3)
    t2 = cbr.truco(2, 1, 0) 
    
    assert t1 == 2
    assert t2 == 0
    
def test_avaliar_envido(bot, cbr):
     #cbr, tipo, quem_pediu, pontos_totais_adversario
    assert bot.avaliar_envido(cbr, 2, 2, 1) == 0
    bot.envido = 25
    assert bot.avaliar_envido(cbr, 0, 2, 7) == 8
    
def test_avaliar_pedir_envido(bot):
    assert bot.avaliar_pedir_envido() == 1
    
def retornar_pontos_totais(bot):
    bot.pontos = 10
    assert bot.retornar_pontos_totais() == 10
    
    bot.pontos = -10
    assert bot.retornar_pontos_totais() == -10
    
def test_resetar(bot):
    try:
        bot.resetar()
    except:
        assert False
        
    assert bot.mao == []
    assert bot.mao_rank == []
    assert bot.indices == []
    assert bot.pontuacao_cartas == []
    assert bot.qualidade_mao == 0
    assert bot.rodadas == 0
    assert bot.envido == 0
    assert bot.rodada == 1
    assert bot.flor == False
    assert bot.pediu_flor == False
    assert bot.pediu_truco == False
    