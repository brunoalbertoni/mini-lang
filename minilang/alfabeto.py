"""Definição manual do alfabeto da MiniLang.

O enunciado proíbe ``re``, ``isalpha()`` e ``isdigit()`` como definição do
alfabeto. Cada predicado abaixo compara faixas de code points ASCII, o que
rejeita naturalmente letras acentuadas: ``ã`` é U+00E3, acima de ``z``.

Todos os predicados aceitam a string vazia, que é o valor devolvido por
``Lexer.peek()`` no fim da entrada, e respondem ``False`` para ela.
"""


def eh_letra(c: str) -> bool:
    """Informa se ``c`` é uma letra ASCII, maiúscula ou minúscula."""
    return ("a" <= c <= "z") or ("A" <= c <= "Z")


def eh_digito(c: str) -> bool:
    """Informa se ``c`` é um dígito ASCII de 0 a 9."""
    return "0" <= c <= "9"


def eh_inicio_ident(c: str) -> bool:
    """Informa se ``c`` pode abrir um identificador: letra ASCII ou ``_``."""
    return eh_letra(c) or c == "_"


def eh_continuacao_ident(c: str) -> bool:
    """Informa se ``c`` pode continuar um identificador: letra, dígito ou ``_``."""
    return eh_letra(c) or eh_digito(c) or c == "_"


def eh_espaco(c: str) -> bool:
    """Informa se ``c`` pertence à classe WHITESPACE: espaço, TAB, CR ou NL."""
    return c == " " or c == "\t" or c == "\r" or c == "\n"


def normalizar_fonte(texto: str) -> str:
    """Converte cada CRLF em um único NL, símbolo a símbolo.

    CR e NL isolados são preservados: ambos contam como quebra de linha para o
    controle de posição, e apenas o par CRLF precisa virar um único símbolo
    para não incrementar a linha duas vezes.
    """
    normalizado = []
    indice = 0
    while indice < len(texto):
        atual = texto[indice]
        if atual == "\r" and indice + 1 < len(texto) and texto[indice + 1] == "\n":
            normalizado.append("\n")
            indice += 2
        else:
            normalizado.append(atual)
            indice += 1
    return "".join(normalizado)
