from minilang.lexer import tokenizar
from minilang.tokens import TokenType


def tipos(fonte):
    tokens, _ = tokenizar(fonte)
    return [token.tipo for token in tokens]


def test_comentario_vazio_e_valido():
    tokens, diagnosticos = tokenizar("//")
    assert [token.tipo for token in tokens] == [TokenType.EOF]
    assert diagnosticos == []


def test_terceira_barra_pertence_ao_comentario():
    tokens, diagnosticos = tokenizar("///x")
    assert [token.tipo for token in tokens] == [TokenType.EOF]
    assert diagnosticos == []


def test_comentario_termina_na_quebra_de_linha():
    assert tipos("// nada aqui\nx") == [TokenType.IDENT, TokenType.EOF]


def test_simbolos_invalidos_dentro_do_comentario_nao_geram_diagnostico():
    _, diagnosticos = tokenizar("// @ ! ç á 123 ###\n")
    assert diagnosticos == []


def test_barra_isolada_continua_sendo_divisao():
    assert tipos("1/2") == [
        TokenType.INT_LITERAL,
        TokenType.SLASH,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_comentario_no_fim_da_linha_de_codigo():
    assert tipos("x = 1; // atribui\ny") == [
        TokenType.IDENT,
        TokenType.ASSIGN,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.IDENT,
        TokenType.EOF,
    ]


def test_comentario_nao_consome_a_quebra_de_linha_mas_a_posicao_avanca():
    tokens, _ = tokenizar("a//x\n  >==b")
    assert (tokens[0].linha, tokens[0].coluna) == (1, 1)
    assert tokens[1].tipo is TokenType.GREATER_EQUAL
    assert (tokens[1].linha, tokens[1].coluna) == (2, 3)


def test_comentario_em_cr_isolado():
    tokens, _ = tokenizar("//abc\rx")
    assert tokens[0].tipo is TokenType.IDENT
    assert (tokens[0].linha, tokens[0].coluna) == (2, 1)
