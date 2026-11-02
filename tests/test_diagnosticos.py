from minilang.lexer import tokenizar
from minilang.tokens import TokenType


def test_simbolo_invalido_nao_interrompe_a_varredura():
    tokens, diagnosticos = tokenizar("@x")
    assert len(diagnosticos) == 1
    assert diagnosticos[0].simbolo == "@"
    assert (diagnosticos[0].linha, diagnosticos[0].coluna) == (1, 1)
    assert [(token.tipo, token.linha, token.coluna) for token in tokens] == [
        (TokenType.IDENT, 1, 2),
        (TokenType.EOF, 1, 3),
    ]


def test_bang_isolado_e_invalido():
    tokens, diagnosticos = tokenizar("!= ! <==")
    assert [token.tipo for token in tokens] == [
        TokenType.BANG_EQUAL,
        TokenType.LESS_EQUAL,
        TokenType.ASSIGN,
        TokenType.EOF,
    ]
    assert len(diagnosticos) == 1
    assert diagnosticos[0].simbolo == "!"
    assert (diagnosticos[0].linha, diagnosticos[0].coluna) == (1, 4)


def test_dois_diagnosticos_seguidos_de_token_valido():
    tokens, diagnosticos = tokenizar("! @ !=")
    assert [(d.simbolo, d.linha, d.coluna) for d in diagnosticos] == [
        ("!", 1, 1),
        ("@", 1, 3),
    ]
    assert tokens[0].tipo is TokenType.BANG_EQUAL
    assert (tokens[0].linha, tokens[0].coluna) == (1, 5)
    assert (tokens[-1].linha, tokens[-1].coluna) == (1, 7)


def test_acento_nao_pertence_ao_identificador():
    tokens, diagnosticos = tokenizar("vãlor")
    assert [(token.tipo, token.lexema, token.coluna) for token in tokens] == [
        (TokenType.IDENT, "v", 1),
        (TokenType.IDENT, "lor", 3),
        (TokenType.EOF, "", 6),
    ]
    assert [(d.simbolo, d.linha, d.coluna) for d in diagnosticos] == [("ã", 1, 2)]


def test_mensagem_do_diagnostico_cita_o_simbolo():
    _, diagnosticos = tokenizar("#")
    assert "#" in diagnosticos[0].mensagem
    assert diagnosticos[0].mensagem != ""


def test_diagnosticos_em_linhas_diferentes():
    _, diagnosticos = tokenizar("a @\n  #b")
    assert [(d.simbolo, d.linha, d.coluna) for d in diagnosticos] == [
        ("@", 1, 3),
        ("#", 2, 3),
    ]


def test_varredura_termina_mesmo_so_com_simbolos_invalidos():
    tokens, diagnosticos = tokenizar("@#$%&")
    assert [token.tipo for token in tokens] == [TokenType.EOF]
    assert len(diagnosticos) == 5
