from minilang.diagnostics import Diagnostico
from minilang.tokens import PALAVRAS_RESERVADAS, Token, TokenType


def test_existem_24_tipos_de_token():
    assert len(TokenType) == 24


def test_tipos_obrigatorios_do_enunciado():
    esperados = [
        "KW_INT", "KW_PRINT", "KW_IF", "KW_ELSE", "KW_WHILE",
        "IDENT", "INT_LITERAL", "ASSIGN",
        "PLUS", "MINUS", "STAR", "SLASH",
        "EQUAL_EQUAL", "BANG_EQUAL", "LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL",
        "LPAREN", "RPAREN", "SEMICOLON", "LBRACE", "RBRACE",
        "EOF",
    ]
    for nome in esperados:
        assert hasattr(TokenType, nome), f"TokenType.{nome} não existe"


def test_tabela_de_palavras_reservadas():
    assert PALAVRAS_RESERVADAS == {
        "int": TokenType.KW_INT,
        "print": TokenType.KW_PRINT,
        "if": TokenType.KW_IF,
        "else": TokenType.KW_ELSE,
        "while": TokenType.KW_WHILE,
    }


def test_token_guarda_tipo_lexema_linha_e_coluna():
    token = Token(TokenType.IDENT, "total2", 3, 7)
    assert token.tipo is TokenType.IDENT
    assert token.lexema == "total2"
    assert token.linha == 3
    assert token.coluna == 7


def test_diagnostico_guarda_simbolo_posicao_e_mensagem():
    diagnostico = Diagnostico("@", 1, 1, "símbolo inválido '@'")
    assert diagnostico.simbolo == "@"
    assert diagnostico.linha == 1
    assert diagnostico.coluna == 1
    assert "@" in diagnostico.mensagem
