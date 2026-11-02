import pytest
from minilang.ast import Atribuicao, Binaria, Declaracao, Inteiro, Programa, Saida, Variavel
from minilang.parser import ParseError, parsear

def test_programa_simples_com_declaracao_atribuicao_e_saida():
    ast = parsear("int x; x = 2 + 3 * 4; print(x);")
    assert isinstance(ast, Programa)
    assert len(ast.declaracoes) == 3
    assert ast.declaracoes[0] == Declaracao("x")
    # Testa indiretamente precedência: '*' (3 * 4) fica à direita na base, '+' no topo
    assert ast.declaracoes[1] == Atribuicao(
        "x",
        Binaria("+", Inteiro(2), Binaria("*", Inteiro(3), Inteiro(4))),
    )
    assert ast.declaracoes[2] == Saida(Variavel("x"))

def test_expressao_precedencia_produto_na_raiz():
    # Testa print((2+3)*4);
    ast = parsear("print((2+3)*4);")
    assert len(ast.declaracoes) == 1
    saida = ast.declaracoes[0]
    
    assert saida == Saida(
        Binaria("*", Binaria("+", Inteiro(2), Inteiro(3)), Inteiro(4))
    )

def test_expressao_associatividade_a_esquerda():
    # Testa print(10 - 3 - 2); 
    # O agrupamento esperado é (10 - 3) - 2 e não 10 - (3 - 2)
    ast = parsear("print(10 - 3 - 2);")
    saida = ast.declaracoes[0]
    
    assert saida == Saida(
        Binaria("-", Binaria("-", Inteiro(10), Inteiro(3)), Inteiro(2))
    )

def test_sintaticamente_valido_com_variavel():
    ast = parsear("print(y);")
    assert len(ast.declaracoes) == 1
    assert ast.declaracoes[0] == Saida(Variavel("y"))

def test_entrada_vazia_retorna_programa_vazio():
    ast = parsear("")
    assert isinstance(ast, Programa)
    assert len(ast.declaracoes) == 0

def test_erro_sintatico_sinalizado_com_posicao_correta():
    # Testa a entrada inválida: print(2+);
    with pytest.raises(ParseError) as excinfo:
        parsear("print(2+);")
    
    mensagem = str(excinfo.value)
    # A mensagem deve mencionar a linha, a coluna e o token (neste caso, o RPAREN / ')')
    assert "linha 1" in mensagem
    assert "coluna 9" in mensagem
    assert "')'" in mensagem