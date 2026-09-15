from minilang.lexer import Lexer
from minilang.tokens import TokenType


def test_estado_inicial():
    lexer = Lexer("abc")
    assert lexer.source == "abc"
    assert lexer.start == 0
    assert lexer.current == 0
    assert lexer.line == 1
    assert lexer.column == 1
    assert lexer.start_line == 1
    assert lexer.start_column == 1
    assert lexer.tokens == []
    assert lexer.diagnostics == []


def test_construtor_normaliza_crlf():
    assert Lexer("a\r\nb").source == "a\nb"


def test_at_end_detecta_fim_da_entrada():
    lexer = Lexer("ab")
    assert lexer.at_end() is False
    lexer.advance()
    assert lexer.at_end() is False
    lexer.advance()
    assert lexer.at_end() is True


def test_at_end_em_entrada_vazia():
    assert Lexer("").at_end() is True


def test_advance_devolve_o_simbolo_e_anda_a_coluna():
    lexer = Lexer("ab")
    assert lexer.advance() == "a"
    assert lexer.current == 1
    assert lexer.line == 1
    assert lexer.column == 2
    assert lexer.advance() == "b"
    assert lexer.column == 3


def test_advance_trata_tab_como_uma_coluna():
    lexer = Lexer("\tx")
    lexer.advance()
    assert lexer.line == 1
    assert lexer.column == 2


def test_advance_em_nl_troca_de_linha_e_zera_a_coluna():
    lexer = Lexer("a\nb")
    lexer.advance()
    assert (lexer.line, lexer.column) == (1, 2)
    lexer.advance()
    assert (lexer.line, lexer.column) == (2, 1)
    lexer.advance()
    assert (lexer.line, lexer.column) == (2, 2)


def test_advance_em_cr_isolado_tambem_troca_de_linha():
    lexer = Lexer("a\rb")
    lexer.advance()
    lexer.advance()
    assert (lexer.line, lexer.column) == (2, 1)


def test_peek_nao_consome():
    lexer = Lexer("ab")
    assert lexer.peek() == "a"
    assert lexer.peek() == "a"
    assert lexer.current == 0


def test_peek_no_fim_devolve_string_vazia():
    lexer = Lexer("a")
    lexer.advance()
    assert lexer.peek() == ""


def test_peek_next_olha_o_simbolo_seguinte_sem_consumir():
    lexer = Lexer("ab")
    assert lexer.peek_next() == "b"
    assert lexer.current == 0


def test_peek_next_no_penultimo_simbolo_devolve_string_vazia():
    lexer = Lexer("a")
    assert lexer.peek_next() == ""


def test_match_consome_quando_o_simbolo_corresponde():
    lexer = Lexer("==")
    lexer.advance()
    assert lexer.match("=") is True
    assert lexer.current == 2
    assert lexer.column == 3


def test_match_nao_consome_quando_o_simbolo_difere():
    lexer = Lexer("=x")
    lexer.advance()
    assert lexer.match("=") is False
    assert lexer.current == 1
    assert lexer.column == 2


def test_match_no_fim_da_entrada_devolve_falso():
    lexer = Lexer("=")
    lexer.advance()
    assert lexer.match("=") is False


def test_add_token_usa_o_recorte_e_a_posicao_inicial():
    lexer = Lexer("total")
    lexer.start_line = 4
    lexer.start_column = 9
    lexer.advance()
    lexer.advance()
    lexer.add_token(TokenType.IDENT)
    token = lexer.tokens[0]
    assert token.tipo is TokenType.IDENT
    assert token.lexema == "to"
    assert token.linha == 4
    assert token.coluna == 9
