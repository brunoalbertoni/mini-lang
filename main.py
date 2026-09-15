"""Ponto de entrada do analisador léxico da MiniLang.

Uso:
    python main.py examples/programa.min
"""

import sys

from minilang import Diagnostico, Lexer, Token

CODIGO_SUCESSO = 0
CODIGO_COM_DIAGNOSTICOS = 1
CODIGO_ERRO_DE_USO = 2


def formatar_tokens(tokens: list[Token]) -> str:
    """Monta a tabela de tokens com posição, tipo e lexema."""
    linhas = ["TOKENS", f"{'LINHA:COL':>10}  {'TIPO':<14}  LEXEMA"]
    for token in tokens:
        posicao = f"{token.linha}:{token.coluna}"
        linhas.append(f"{posicao:>10}  {token.tipo.value:<14}  {token.lexema!r}")
    linhas.append(f"total de tokens: {len(tokens)}")
    return "\n".join(linhas)


def formatar_diagnosticos(diagnosticos: list[Diagnostico]) -> str:
    """Monta a lista de diagnósticos, ou avisa que não houve nenhum."""
    if not diagnosticos:
        return "DIAGNÓSTICOS\nnenhum símbolo inválido encontrado."

    linhas = ["DIAGNÓSTICOS"]
    for diagnostico in diagnosticos:
        linhas.append(
            f"{diagnostico.linha}:{diagnostico.coluna} erro léxico: "
            f"{diagnostico.mensagem}"
        )
    linhas.append(f"total de diagnósticos: {len(diagnosticos)}")
    return "\n".join(linhas)


def main(argv: list[str]) -> int:
    """Lê o arquivo indicado, executa o lexer e imprime o resultado."""
    if len(argv) != 2:
        print("uso: python main.py <arquivo.min>", file=sys.stderr)
        return CODIGO_ERRO_DE_USO

    caminho = argv[1]

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            fonte = arquivo.read()
    except OSError as erro:
        print(f"não foi possível ler {caminho}: {erro}", file=sys.stderr)
        return CODIGO_ERRO_DE_USO

    tokens, diagnosticos = Lexer(fonte).scan_tokens()

    print(formatar_tokens(tokens))
    print()
    print(formatar_diagnosticos(diagnosticos))

    if diagnosticos:
        return CODIGO_COM_DIAGNOSTICOS
    return CODIGO_SUCESSO


if __name__ == "__main__":
    sys.exit(main(sys.argv))
