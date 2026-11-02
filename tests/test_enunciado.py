"""Testes que reproduzem literalmente as tabelas de exemplos do enunciado."""

import pytest

from minilang.lexer import tokenizar
from minilang.tokens import TokenType

T = TokenType


def tipos(fonte):
    tokens, _ = tokenizar(fonte)
    return [token.tipo for token in tokens]


def posicoes(fonte):
    tokens, _ = tokenizar(fonte)
    return [(token.tipo, token.lexema, token.linha, token.coluna) for token in tokens]


# ----------------------------------------------------------------------
# Seção 4.1 — Tokenização
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "fonte, esperado",
    [
        ("int intx ifx while", [T.KW_INT, T.IDENT, T.IDENT, T.KW_WHILE, T.EOF]),
        (
            "007 -10 +7",
            [T.INT_LITERAL, T.MINUS, T.INT_LITERAL, T.PLUS, T.INT_LITERAL, T.EOF],
        ),
        (
            "2total total-2",
            [T.INT_LITERAL, T.IDENT, T.IDENT, T.MINUS, T.INT_LITERAL, T.EOF],
        ),
        ("= == ===", [T.ASSIGN, T.EQUAL_EQUAL, T.EQUAL_EQUAL, T.ASSIGN, T.EOF]),
        ("!= ! <==", [T.BANG_EQUAL, T.LESS_EQUAL, T.ASSIGN, T.EOF]),
        ("a/b", [T.IDENT, T.SLASH, T.IDENT, T.EOF]),
        ("//", [T.EOF]),
        ("///x", [T.EOF]),
        (
            "{print(x);}",
            [
                T.LBRACE,
                T.KW_PRINT,
                T.LPAREN,
                T.IDENT,
                T.RPAREN,
                T.SEMICOLON,
                T.RBRACE,
                T.EOF,
            ],
        ),
        ("", [T.EOF]),
    ],
)
def test_tabela_4_1_tokenizacao(fonte, esperado):
    assert tipos(fonte) == esperado


def test_tabela_4_1_entrada_vazia_nao_gera_diagnostico():
    tokens, diagnosticos = tokenizar("")
    assert (tokens[0].linha, tokens[0].coluna) == (1, 1)
    assert diagnosticos == []


# ----------------------------------------------------------------------
# Seção 4.2 — Posições e diagnósticos
# ----------------------------------------------------------------------


def test_tabela_4_2_quebra_de_linha_com_recuo():
    assert posicoes("int\n  valor") == [
        (T.KW_INT, "int", 1, 1),
        (T.IDENT, "valor", 2, 3),
        (T.EOF, "", 2, 8),
    ]


def test_tabela_4_2_simbolo_invalido_no_inicio():
    tokens, diagnosticos = tokenizar("@x")
    assert [(d.simbolo, d.linha, d.coluna) for d in diagnosticos] == [("@", 1, 1)]
    assert [(t.tipo, t.linha, t.coluna) for t in tokens] == [
        (T.IDENT, 1, 2),
        (T.EOF, 1, 3),
    ]


def test_tabela_4_2_comentario_antes_de_reservada():
    assert posicoes("// comentário\n  while") == [
        (T.KW_WHILE, "while", 2, 3),
        (T.EOF, "", 2, 8),
    ]


def test_tabela_4_2_comentario_colado_e_operadores():
    assert posicoes("a//x\n  >==b") == [
        (T.IDENT, "a", 1, 1),
        (T.GREATER_EQUAL, ">=", 2, 3),
        (T.ASSIGN, "=", 2, 5),
        (T.IDENT, "b", 2, 6),
        (T.EOF, "", 2, 7),
    ]


# ----------------------------------------------------------------------
# Seção 6 — Verificação individual
# ----------------------------------------------------------------------


def test_secao_6_condicional_completa():
    assert tipos("if(total2>=10){print(total2);}") == [
        T.KW_IF,
        T.LPAREN,
        T.IDENT,
        T.GREATER_EQUAL,
        T.INT_LITERAL,
        T.RPAREN,
        T.LBRACE,
        T.KW_PRINT,
        T.LPAREN,
        T.IDENT,
        T.RPAREN,
        T.SEMICOLON,
        T.RBRACE,
        T.EOF,
    ]


def test_secao_6_ident_colado_em_operadores():
    tokens, _ = tokenizar("intx===007;")
    assert [(t.tipo, t.lexema) for t in tokens] == [
        (T.IDENT, "intx"),
        (T.EQUAL_EQUAL, "=="),
        (T.ASSIGN, "="),
        (T.INT_LITERAL, "007"),
        (T.SEMICOLON, ";"),
        (T.EOF, ""),
    ]


def test_secao_6_identificador_com_digito():
    tokens, _ = tokenizar("while1 != while")
    assert [(t.tipo, t.lexema) for t in tokens] == [
        (T.IDENT, "while1"),
        (T.BANG_EQUAL, "!="),
        (T.KW_WHILE, "while"),
        (T.EOF, ""),
    ]


def test_secao_6_numero_colado_em_reservada():
    tokens, _ = tokenizar("2if <= 03")
    assert [(t.tipo, t.lexema) for t in tokens] == [
        (T.INT_LITERAL, "2"),
        (T.KW_IF, "if"),
        (T.LESS_EQUAL, "<="),
        (T.INT_LITERAL, "03"),
        (T.EOF, ""),
    ]


def test_secao_6_erros_e_continuidade():
    tokens, diagnosticos = tokenizar("! @ !=")
    assert [(d.simbolo, d.linha, d.coluna) for d in diagnosticos] == [
        ("!", 1, 1),
        ("@", 1, 3),
    ]
    assert [(t.tipo, t.linha, t.coluna) for t in tokens] == [
        (T.BANG_EQUAL, 1, 5),
        (T.EOF, 1, 7),
    ]


def test_secao_6_identificador_ascii():
    tokens, diagnosticos = tokenizar("vãlor")
    assert [(t.tipo, t.lexema, t.coluna) for t in tokens] == [
        (T.IDENT, "v", 1),
        (T.IDENT, "lor", 3),
        (T.EOF, "", 6),
    ]
    assert [(d.simbolo, d.linha, d.coluna) for d in diagnosticos] == [("ã", 1, 2)]


def test_secao_6_posicoes_em_programa_multilinha():
    fonte = "int x;\nif(x<10){\n  print(x);\n}"
    tokens, diagnosticos = tokenizar(fonte)
    por_posicao = {(t.linha, t.coluna): (t.tipo, t.lexema) for t in tokens}

    assert por_posicao[(1, 1)] == (T.KW_INT, "int")
    assert por_posicao[(1, 5)] == (T.IDENT, "x")
    assert por_posicao[(2, 1)] == (T.KW_IF, "if")
    assert por_posicao[(2, 5)] == (T.LESS, "<")
    assert por_posicao[(3, 3)] == (T.KW_PRINT, "print")
    assert por_posicao[(4, 1)] == (T.RBRACE, "}")
    assert por_posicao[(4, 2)] == (T.EOF, "")
    assert diagnosticos == []


def test_secao_6_tab_avanca_uma_coluna():
    assert posicoes("\tprint") == [
        (T.KW_PRINT, "print", 1, 2),
        (T.EOF, "", 1, 7),
    ]


def test_secao_6_rastreamento_de_tres_iguais():
    tokens, _ = tokenizar("===")
    assert [(t.tipo, t.lexema, t.coluna) for t in tokens] == [
        (T.EQUAL_EQUAL, "==", 1),
        (T.ASSIGN, "=", 3),
        (T.EOF, "", 4),
    ]


def test_secao_6_exatamente_um_eof():
    for fonte in ["", "x", "@", "// c", "int x;\n", "a\n\n\n"]:
        tokens, _ = tokenizar(fonte)
        eofs = [t for t in tokens if t.tipo is T.EOF]
        assert len(eofs) == 1, fonte
        assert eofs[0] is tokens[-1]
        assert eofs[0].lexema == ""
