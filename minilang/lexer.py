"""Analisador léxico manual da MiniLang.

A varredura é feita símbolo a símbolo a partir de um cursor sobre ``source``.
Nenhuma etapa divide a entrada previamente.
"""

from minilang.alfabeto import normalizar_fonte
from minilang.diagnostics import Diagnostico
from minilang.tokens import Token, TokenType


class Lexer:
    """Percorre o código-fonte da esquerda para a direita produzindo tokens."""

    def __init__(self, source: str) -> None:
        self.source = normalizar_fonte(source)
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1
        self.tokens: list[Token] = []
        self.diagnostics: list[Diagnostico] = []

    # ------------------------------------------------------------------
    # Navegação sobre a entrada
    # ------------------------------------------------------------------

    def at_end(self) -> bool:
        """Informa se ``current`` alcançou o fim de ``source``."""
        return self.current >= len(self.source)

    def advance(self) -> str:
        """Consome um símbolo, avança ``current`` e atualiza linha e coluna.

        Este é o único ponto do lexer que altera ``line`` e ``column``.
        """
        atual = self.source[self.current]
        self.current += 1
        if atual == "\n" or atual == "\r":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return atual

    def peek(self) -> str:
        """Consulta o símbolo em ``current`` sem consumir."""
        if self.at_end():
            return ""
        return self.source[self.current]

    def peek_next(self) -> str:
        """Consulta o símbolo posterior a ``current`` sem consumir."""
        if self.current + 1 >= len(self.source):
            return ""
        return self.source[self.current + 1]

    def match(self, esperado: str) -> bool:
        """Consome o símbolo atual via ``advance()`` quando ele é o esperado."""
        if self.peek() != esperado:
            return False
        self.advance()
        return True

    # ------------------------------------------------------------------
    # Produção de saída
    # ------------------------------------------------------------------

    def add_token(self, tipo: TokenType) -> None:
        """Cria um token com ``source[start:current]`` e a posição inicial."""
        lexema = self.source[self.start:self.current]
        self.tokens.append(Token(tipo, lexema, self.start_line, self.start_column))
