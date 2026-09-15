from minilang.alfabeto import (
    eh_continuacao_ident,
    eh_digito,
    eh_espaco,
    eh_inicio_ident,
    eh_letra,
    normalizar_fonte,
)


def test_eh_letra_aceita_apenas_ascii():
    for c in ["a", "z", "A", "Z", "m", "Q"]:
        assert eh_letra(c) is True
    for c in ["0", "9", "_", "@", " ", "", "ã", "Ç", "é", "ñ"]:
        assert eh_letra(c) is False


def test_eh_digito_aceita_apenas_0_a_9():
    for c in ["0", "5", "9"]:
        assert eh_digito(c) is True
    for c in ["a", "Z", "_", "", " ", "٣"]:
        assert eh_digito(c) is False


def test_inicio_de_identificador_aceita_letra_e_underscore():
    assert eh_inicio_ident("a") is True
    assert eh_inicio_ident("Z") is True
    assert eh_inicio_ident("_") is True
    assert eh_inicio_ident("0") is False
    assert eh_inicio_ident("") is False


def test_continuacao_de_identificador_aceita_digito():
    assert eh_continuacao_ident("0") is True
    assert eh_continuacao_ident("_") is True
    assert eh_continuacao_ident("x") is True
    assert eh_continuacao_ident("-") is False
    assert eh_continuacao_ident("") is False


def test_eh_espaco_cobre_espaco_tab_cr_e_nl():
    for c in [" ", "\t", "\r", "\n"]:
        assert eh_espaco(c) is True
    for c in ["a", "0", "", "\v"]:
        assert eh_espaco(c) is False


def test_normalizar_fonte_converte_crlf_em_nl():
    assert normalizar_fonte("a\r\nb") == "a\nb"
    assert normalizar_fonte("a\r\n\r\nb") == "a\n\nb"


def test_normalizar_fonte_preserva_cr_e_nl_isolados():
    assert normalizar_fonte("a\rb") == "a\rb"
    assert normalizar_fonte("a\nb") == "a\nb"
    assert normalizar_fonte("a\n\rb") == "a\n\rb"


def test_normalizar_fonte_lida_com_cr_no_fim_da_entrada():
    assert normalizar_fonte("a\r") == "a\r"
    assert normalizar_fonte("") == ""
