from minilang.ast import Atribuicao, Binaria, Declaracao, Inteiro, Programa, Saida, Variavel
from minilang.parser import parsear


def test_programa_simples_com_declaracao_atribuicao_e_saida():
    ast = parsear("int x; x = 2 + 3 * 4; print(x);")

    assert isinstance(ast, Programa)
    assert len(ast.declaracoes) == 3
    assert ast.declaracoes[0] == Declaracao("x")
    assert ast.declaracoes[1] == Atribuicao(
        "x",
        Binaria(
            "+",
            Inteiro(2),
            Binaria("*", Inteiro(3), Inteiro(4)),
        ),
    )
    assert ast.declaracoes[2] == Saida(Variavel("x"))


def test_expressao_comparacao_e_if():
    ast = parsear("if (x < 10) { print(x); }")

    assert hasattr(ast, "declaracoes")
    assert len(ast.declaracoes) == 1
    assert ast.declaracoes[0].__class__.__name__ == "Se"
