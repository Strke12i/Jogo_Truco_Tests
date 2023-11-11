from truco.interface import Interface
from truco.jogador import Jogador
from truco.carta import Carta
import pytest

@pytest.fixture
def interface():
    return Interface()

def test_border_msg(interface, capsys):
    try:
        interface.border_msg("Teste", indent = 1)
    except:
        assert False

    out, err = capsys.readouterr()
    assert out == "╔═══════╗\n║ Teste ║\n╚═══════╝\n"


def test_limpar_tela(interface, capsys):
    try:
        print("Hello World")
        interface.limpar_tela()
    except:
        assert False

    out, err = capsys.readouterr()
    assert out != ""

def test_mostrar_carta_jogada(interface, capsys):
    try:
        interface.mostrar_carta_jogada("Jogador", Carta("1", "OUROS"))
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Jogador jogou a carta: 1 de OUROS\n"

    try:
        interface.mostrar_carta_jogada("Jogador", Carta("3", "PAUS"))
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Jogador jogou a carta: 3 de PAUS\n"

def test_mostrar_carta_ganhadora(interface, capsys):
    try:
        interface.mostrar_carta_ganhadora(Carta("1", "OUROS"))
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "\nCarta ganhadora: 1 de OUROS\n\n"

def test_mostrar_ganhador_rodada(interface, capsys):
    try:
        interface.mostrar_ganhador_rodada("Jogador")
        interface.mostrar_ganhador_rodada("Jogador 2")
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Jogador ganhou a rodada\n\nJogador 2 ganhou a rodada\n\n"

def test_mostrar_placar_jogador_fugiu(interface, capsys):
    try:
        jogador = Jogador("Felipe")
        interface.mostrar_placar_total_jogador_fugiu(jogador, "Jogador", 1, "Jogador 2", 15)
    except:
        assert False

    out, err = capsys.readouterr()
    assert out == "Jogador Felipe fugiu!\n"  

    try:
        jogador = Jogador("")
        interface.mostrar_placar_total_jogador_fugiu(jogador, "Jogador", 1, "Jogador 2", 15)
    except:
        assert False

    out, err = capsys.readouterr()
    assert out == "Jogador  fugiu!\n"  

def test_mostrar_placar_total(interface, capsys):
    try:
        interface.mostrar_placar_total("Jogador", 1, "Jogador 2", 15)
    except:
        assert False

    out, err = capsys.readouterr()
    assert out == "╔═════════════════════════════════════════════╗\n║ Pontuação Total                             ║\n║ ---------------                             ║\n║ Jogador 1 - Jogador: 1 Pontos Acumulados    ║\n║ Jogador 2 - Jogador 2: 15 Pontos Acumulados ║\n╚═════════════════════════════════════════════╝\n"
   
   
def test_mostrar_placar_rodadas(interface, capsys):
    try:
        interface.mostrar_placar_rodadas("Jogador", 2, "Jogador 2", 4)
    except:
        assert False

    out, err = capsys.readouterr()
    assert ("Jogador 1 - Jogador: Venceu 2 Rodada(s)" in out) and ("Jogador 2 - Jogador 2: Venceu 4 Rodada(s)" in out) == True


def test_mostrar_vencedor_flor(interface, capsys):
    try:
        interface.mostrar_vencedor_flor(1, "Jogador", "Jogador 2", 4)
    except:
        assert False

    out, err = capsys.readouterr()
    assert "Jogador 1 - Jogador: Venceu a flor e ganhou 4 pontos" in out

    try:
        interface.mostrar_vencedor_flor(34, "Jogador", "Felipe", 4)
    except:
        assert False

    out, err = capsys.readouterr()
    assert "Jogador 2 - Felipe: Venceu a flor e ganhou 4 pontos" in out

def test_mostrar_vencedor_envido(interface, capsys):
    try:
        interface.mostrar_vencedor_envido(1, "Jogador", 4, "Jogador 2", 2)
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert ("Jogador 1 - Jogador: Venceu o envido com 4 pontos" and "Jogador 2 - Jogador 2: PERDEU o envido com 2 pontos" in out and "Jogador 1 Vencedor Envido" in out) == True
   
    try:
        interface.mostrar_vencedor_envido(0, "Jogador", 2, "Jogador 2", 4)
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert ("Jogador 2 - Jogador 2: Venceu o envido com 4 pontos" and "Jogador 1 - Jogador: PERDEU o envido com 2 pontos" in out and "Jogador 2 Vencedor Envido" in out) == True

def test_mostrar_ganhador_jogo(interface, capsys):
    try:
        interface.mostrar_ganhador_jogo("Jogador")
    except:
        assert False

    out, err = capsys.readouterr()
    assert out == "\nJogador ganhou o jogo\n"

    try:
        interface.mostrar_ganhador_jogo("Jogador 2")
    except:
        assert False

    out, err = capsys.readouterr()
    assert out == "\nJogador 2 ganhou o jogo\n"

def test_mostrar_pediu_truco(interface, capsys):
    try:
        interface.mostrar_pediu_truco("Jogador")
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Jogador pediu truco e o pedido já foi aceito, escolha outra jogada!\n"

    try:
        interface.mostrar_pediu_truco("")
    except:
        assert False

    out, err = capsys.readouterr()
    assert out == " pediu truco e o pedido já foi aceito, escolha outra jogada!\n"

def test_mostrar_jogador_opcoes(interface, capsys):
    try:
        interface.mostrar_jogador_opcoes("Jogador")
    except:
        assert False

    out, err = capsys.readouterr()
    assert out == "Jogador 1 é mão\n"

    try:
        interface.mostrar_jogador_opcoes("")
    except:
        assert False

    out, err = capsys.readouterr()
    assert out == "Jogador 1 é mão\n"
   
def test_desenhar_cartas(interface):
    ouro = interface.desenhar_cartas("1 DE OUROS")
    copa = interface.desenhar_cartas("2 DE COPAS")
    espada = interface.desenhar_cartas("3 DE ESPADAS")
    bastos = interface.desenhar_cartas("4 DE BASTOS")

    assert ouro == ['┌─────────┐', '│.1  . . .│', '│. . . . .│', '│. . . . .│', '│. . ♦ . .│', '│. . . . .│', '│. . . . .│', '│. . . 1 .│', '└─────────┘']
    assert copa == ['┌─────────┐', '│.2  . . .│', '│. . . . .│', '│. . . . .│', '│. . ♥ . .│', '│. . . . .│', '│. . . . .│', '│. . . 2 .│', '└─────────┘']
    assert espada == ['┌─────────┐', '│.3  . . .│', '│. . . . .│', '│. . . . .│', '│. . ♠ . .│', '│. . . . .│', '│. . . . .│', '│. . . 3 .│', '└─────────┘']
    assert bastos == ['┌─────────┐', '│.4  . . .│', '│. . . . .│', '│. . . . .│', '│. . ♣ . .│', '│. . . . .│', '│. . . . .│', '│. . . 4 .│', '└─────────┘']


def test_exibir_carta_unica(interface, capsys):
    interface.exibir_unica_carta("OUROS")
    #assert False