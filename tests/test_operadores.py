from minilang.lexer import tokenizar
from minilang.tokens import TokenType


def tipos(fonte):
    tokens, _ = tokenizar(fonte)
    return [token.tipo for token in tokens]


def test_entrada_vazia_produz_apenas_eof():
    tokens, diagnosticos = tokenizar("")
    assert len(tokens) == 1
    assert tokens[0].tipo is TokenType.EOF
    assert tokens[0].lexema == ""
    assert (tokens[0].linha, tokens[0].coluna) == (1, 1)
    assert diagnosticos == []


def test_somente_espacos_produz_apenas_eof():
    tokens, diagnosticos = tokenizar("   \t \n  ")
    assert [token.tipo for token in tokens] == [TokenType.EOF]
    assert diagnosticos == []


def test_operadores_aritmeticos():
    assert tipos("+-*/") == [
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.STAR,
        TokenType.SLASH,
        TokenType.EOF,
    ]


def test_delimitadores_e_chaves():
    assert tipos("(){};") == [
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
        TokenType.RBRACE,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]


def test_maior_casamento_do_igual():
    assert tipos("= == ===") == [
        TokenType.ASSIGN,
        TokenType.EQUAL_EQUAL,
        TokenType.EQUAL_EQUAL,
        TokenType.ASSIGN,
        TokenType.EOF,
    ]


def test_operadores_relacionais_com_prefixo_comum():
    assert tipos("< <= > >= !=") == [
        TokenType.LESS,
        TokenType.LESS_EQUAL,
        TokenType.GREATER,
        TokenType.GREATER_EQUAL,
        TokenType.BANG_EQUAL,
        TokenType.EOF,
    ]


def test_menor_igual_seguido_de_igual():
    assert tipos("<==") == [
        TokenType.LESS_EQUAL,
        TokenType.ASSIGN,
        TokenType.EOF,
    ]


def test_lexema_e_posicao_dos_operadores():
    tokens, _ = tokenizar(">= ;")
    assert tokens[0].lexema == ">="
    assert (tokens[0].linha, tokens[0].coluna) == (1, 1)
    assert tokens[1].lexema == ";"
    assert (tokens[1].linha, tokens[1].coluna) == (1, 4)
    assert (tokens[2].linha, tokens[2].coluna) == (1, 5)


def test_eof_fica_na_posicao_posterior_ao_ultimo_simbolo():
    tokens, _ = tokenizar("+\n++")
    eof = tokens[-1]
    assert eof.tipo is TokenType.EOF
    assert (eof.linha, eof.coluna) == (2, 3)


def test_espacos_entre_operadores_nao_viram_token():
    assert tipos(" + \t - \n * ") == [
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.STAR,
        TokenType.EOF,
    ]
