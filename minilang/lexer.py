"""Analisador léxico manual da MiniLang.

A varredura é feita símbolo a símbolo a partir de um cursor sobre ``source``.
Nenhuma etapa divide a entrada previamente.
"""

from minilang.alfabeto import (
    eh_continuacao_ident,
    eh_digito,
    eh_espaco,
    eh_inicio_ident,
    normalizar_fonte,
)
from minilang.diagnostics import Diagnostico
from minilang.tokens import PALAVRAS_RESERVADAS, Token, TokenType

SIMBOLOS_SIMPLES = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    ";": TokenType.SEMICOLON,
}


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
    # Varredura
    # ------------------------------------------------------------------

    def scan_tokens(self) -> tuple[list[Token], list[Diagnostico]]:
        """Varre toda a entrada e devolve os tokens e os diagnósticos.

        Cada iteração registra onde o próximo lexema começa e delega a
        ``scan_token()``, que consome ao menos um símbolo. Essa invariante é o
        que impede laço infinito diante de entrada inválida.
        """
        while not self.at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column

            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))

        return self.tokens, self.diagnostics

    def scan_token(self) -> None:
        """Identifica a classe iniciada na posição atual e a consome."""
        if self.peek() == "/" and self.peek_next() == "/":
            self.advance()
            self.advance()
            self.line_comment()
            return

        atual = self.advance()

        if eh_inicio_ident(atual):
            self.identifier()
        elif eh_digito(atual):
            self.number()
        elif atual == "/":
            self.add_token(TokenType.SLASH)
        elif atual == "=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.ASSIGN)
        elif atual == "!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.report_invalid_character(atual)
        elif atual == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif atual == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif atual in SIMBOLOS_SIMPLES:
            self.add_token(SIMBOLOS_SIMPLES[atual])
        elif eh_espaco(atual):
            while eh_espaco(self.peek()):
                self.advance()
        else:
            self.report_invalid_character(atual)

    # ------------------------------------------------------------------
    # Reconhecedores de continuidade
    # ------------------------------------------------------------------

    def identifier(self) -> None:
        """Consome a continuação do identificador e consulta as reservadas.

        O primeiro símbolo já foi consumido por ``scan_token()``. A consulta à
        tabela acontece só depois do maior casamento, por isso ``intx`` é
        ``IDENT`` e não ``KW_INT`` seguido de ``IDENT``.
        """
        while eh_continuacao_ident(self.peek()):
            self.advance()

        lexema = self.source[self.start:self.current]

        if lexema in PALAVRAS_RESERVADAS:
            self.add_token(PALAVRAS_RESERVADAS[lexema])
        else:
            self.add_token(TokenType.IDENT)

    def number(self) -> None:
        """Consome os dígitos restantes do literal inteiro.

        Zeros à esquerda são preservados no lexema; ``+`` e ``-`` não fazem
        parte do literal e viram tokens próprios.
        """
        while eh_digito(self.peek()):
            self.advance()

        self.add_token(TokenType.INT_LITERAL)

    def line_comment(self) -> None:
        """Substituído na Tarefa 6."""
        raise NotImplementedError

    def report_invalid_character(self, simbolo: str) -> None:
        """Substituído na Tarefa 7."""
        raise NotImplementedError

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


def tokenizar(fonte: str) -> tuple[list[Token], list[Diagnostico]]:
    """Atalho que constrói um ``Lexer`` e executa a varredura completa."""
    return Lexer(fonte).scan_tokens()
