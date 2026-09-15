from minilang.lexer import tokenizar
from minilang.tokens import TokenType


def pares(fonte):
    tokens, _ = tokenizar(fonte)
    return [(token.tipo, token.lexema) for token in tokens]


def test_palavras_reservadas_do_nucleo_e_da_extensao():
    assert pares("int print if else while") == [
        (TokenType.KW_INT, "int"),
        (TokenType.KW_PRINT, "print"),
        (TokenType.KW_IF, "if"),
        (TokenType.KW_ELSE, "else"),
        (TokenType.KW_WHILE, "while"),
        (TokenType.EOF, ""),
    ]


def test_reservada_so_e_consultada_apos_o_maior_ident():
    assert pares("int intx ifx while") == [
        (TokenType.KW_INT, "int"),
        (TokenType.IDENT, "intx"),
        (TokenType.IDENT, "ifx"),
        (TokenType.KW_WHILE, "while"),
        (TokenType.EOF, ""),
    ]


def test_identificador_com_digito_no_fim_nao_vira_reservada():
    assert pares("while1 != while") == [
        (TokenType.IDENT, "while1"),
        (TokenType.BANG_EQUAL, "!="),
        (TokenType.KW_WHILE, "while"),
        (TokenType.EOF, ""),
    ]


def test_identificador_aceita_underscore_e_maiusculas():
    assert pares("_x Total_2 __ INT") == [
        (TokenType.IDENT, "_x"),
        (TokenType.IDENT, "Total_2"),
        (TokenType.IDENT, "__"),
        (TokenType.IDENT, "INT"),
        (TokenType.EOF, ""),
    ]


def test_reservadas_sao_case_sensitive():
    assert pares("If WHILE Print") == [
        (TokenType.IDENT, "If"),
        (TokenType.IDENT, "WHILE"),
        (TokenType.IDENT, "Print"),
        (TokenType.EOF, ""),
    ]


def test_inteiro_aceita_zeros_a_esquerda():
    assert pares("007 0 42") == [
        (TokenType.INT_LITERAL, "007"),
        (TokenType.INT_LITERAL, "0"),
        (TokenType.INT_LITERAL, "42"),
        (TokenType.EOF, ""),
    ]


def test_sinais_formam_tokens_separados_do_literal():
    assert pares("007 -10 +7") == [
        (TokenType.INT_LITERAL, "007"),
        (TokenType.MINUS, "-"),
        (TokenType.INT_LITERAL, "10"),
        (TokenType.PLUS, "+"),
        (TokenType.INT_LITERAL, "7"),
        (TokenType.EOF, ""),
    ]


def test_numero_seguido_de_letra_produz_dois_tokens_validos():
    assert pares("2total total-2") == [
        (TokenType.INT_LITERAL, "2"),
        (TokenType.IDENT, "total"),
        (TokenType.IDENT, "total"),
        (TokenType.MINUS, "-"),
        (TokenType.INT_LITERAL, "2"),
        (TokenType.EOF, ""),
    ]


def test_numero_colado_em_reservada():
    assert pares("2if <= 03") == [
        (TokenType.INT_LITERAL, "2"),
        (TokenType.KW_IF, "if"),
        (TokenType.LESS_EQUAL, "<="),
        (TokenType.INT_LITERAL, "03"),
        (TokenType.EOF, ""),
    ]


def test_ident_colado_em_operadores():
    assert pares("intx===007;") == [
        (TokenType.IDENT, "intx"),
        (TokenType.EQUAL_EQUAL, "=="),
        (TokenType.ASSIGN, "="),
        (TokenType.INT_LITERAL, "007"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, ""),
    ]


def test_divisao_entre_identificadores():
    assert pares("a/b") == [
        (TokenType.IDENT, "a"),
        (TokenType.SLASH, "/"),
        (TokenType.IDENT, "b"),
        (TokenType.EOF, ""),
    ]


def test_posicao_inicial_do_identificador_e_do_numero():
    tokens, _ = tokenizar("  total2 99")
    assert (tokens[0].linha, tokens[0].coluna) == (1, 3)
    assert (tokens[1].linha, tokens[1].coluna) == (1, 10)
