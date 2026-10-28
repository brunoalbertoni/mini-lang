"""Parser descendente recursivo da MiniLang."""

from __future__ import annotations

from typing import Any

from minilang.lexer import Lexer
from minilang.tokens import Token, TokenType

from .ast import (
    Atribuicao,
    Binaria,
    Bloco,
    Declaracao,
    Enquanto,
    Inteiro,
    Programa,
    Saida,
    Se,
    Variavel,
)


class ParseError(Exception):
    """Erro sintático detectado durante a análise."""


class Parser:
    """Analisa uma sequência de tokens e produz uma AST."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    def parse_programa(self) -> Programa:
        instrucoes: list[Any] = []
        while not self.at_end() and self.peek().tipo is not TokenType.EOF:
            instrucoes.append(self.parse_declaracao_ou_comando())
        return Programa(instrucoes)

    def parse_declaracao_ou_comando(self) -> Any:
        if self.match(TokenType.KW_INT):
            return self.parse_declaracao()
        if self.match(TokenType.KW_PRINT):
            return self.parse_saida()
        if self.match(TokenType.KW_IF):
            return self.parse_if()
        if self.match(TokenType.KW_WHILE):
            return self.parse_while()
        if self.match(TokenType.LBRACE):
            return self.parse_bloco_aberto()
        if self.check(TokenType.IDENT):
            nome = self.advance().lexema
            self.expect(TokenType.ASSIGN, "esperado '=' após o identificador")
            valor = self.parse_expressao()
            self.expect(TokenType.SEMICOLON, "esperado ';' após atribuição")
            return Atribuicao(nome, valor)

        raise ParseError(f"comando inesperado: {self.peek()}")

    def parse_declaracao(self) -> Declaracao:
        nome = self.expect(TokenType.IDENT, "esperado identificador após 'int'").lexema
        self.expect(TokenType.SEMICOLON, "esperado ';' após declaração")
        return Declaracao(nome)

    def parse_saida(self) -> Saida:
        self.expect(TokenType.LPAREN, "esperado '(' após 'print'")
        expr = self.parse_expressao()
        self.expect(TokenType.RPAREN, "esperado ')' após expressão")
        self.expect(TokenType.SEMICOLON, "esperado ';' após print")
        return Saida(expr)

    def parse_if(self) -> Se:
        self.expect(TokenType.LPAREN, "esperado '(' após 'if'")
        condicao = self.parse_expressao()
        self.expect(TokenType.RPAREN, "esperado ')' após condição")
        entao = self.parse_declaracao_ou_comando()
        senao = None
        if self.match(TokenType.KW_ELSE):
            senao = self.parse_declaracao_ou_comando()
        return Se(condicao, entao, senao)

    def parse_while(self) -> Enquanto:
        self.expect(TokenType.LPAREN, "esperado '(' após 'while'")
        condicao = self.parse_expressao()
        self.expect(TokenType.RPAREN, "esperado ')' após condição")
        corpo = self.parse_declaracao_ou_comando()
        return Enquanto(condicao, corpo)

    def parse_bloco_aberto(self) -> Bloco:
        instrucoes: list[Any] = []
        while not self.check(TokenType.RBRACE) and not self.at_end():
            instrucoes.append(self.parse_declaracao_ou_comando())
        self.expect(TokenType.RBRACE, "esperado '}' para fechar bloco")
        return Bloco(instrucoes)

    def parse_expressao(self) -> Any:
        return self.parse_relacional()

    def parse_relacional(self) -> Any:
        expr = self.parse_aditiva()
        while self.check_any(
            TokenType.EQUAL_EQUAL,
            TokenType.BANG_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            operador = self.advance().lexema
            direita = self.parse_aditiva()
            expr = Binaria(operador, expr, direita)
        return expr

    def parse_aditiva(self) -> Any:
        expr = self.parse_multiplicativa()
        while self.check_any(TokenType.PLUS, TokenType.MINUS):
            operador = self.advance().lexema
            direita = self.parse_multiplicativa()
            expr = Binaria(operador, expr, direita)
        return expr

    def parse_multiplicativa(self) -> Any:
        expr = self.parse_unaria()
        while self.check_any(TokenType.STAR, TokenType.SLASH):
            operador = self.advance().lexema
            direita = self.parse_unaria()
            expr = Binaria(operador, expr, direita)
        return expr

    def parse_unaria(self) -> Any:
        if self.match(TokenType.MINUS):
            return Binaria("-", Inteiro(0), self.parse_unaria())
        if self.match(TokenType.PLUS):
            return self.parse_unaria()
        return self.parse_primitivo()

    def parse_primitivo(self) -> Any:
        if self.match(TokenType.INT_LITERAL):
            return Inteiro(int(self.previous().lexema))
        if self.match(TokenType.IDENT):
            return Variavel(self.previous().lexema)
        if self.match(TokenType.LPAREN):
            expr = self.parse_expressao()
            self.expect(TokenType.RPAREN, "esperado ')' após expressão")
            return expr
        raise ParseError(f"expressão inválida em: {self.peek()}")

    def match(self, *tipos: TokenType) -> bool:
        if self.check_any(*tipos):
            self.advance()
            return True
        return False

    def check_any(self, *tipos: TokenType) -> bool:
        if self.at_end():
            return False
        return self.peek().tipo in tipos

    def check(self, tipo: TokenType) -> bool:
        if self.at_end():
            return False
        return self.peek().tipo is tipo

    def expect(self, tipo: TokenType, mensagem: str) -> Token:
        if self.check(tipo):
            return self.advance()
        raise ParseError(f"{mensagem} (token atual: {self.peek()})")

    def advance(self) -> Token:
        if not self.at_end():
            token = self.tokens[self.index]
            self.index += 1
            return token
        return self.tokens[-1]

    def previous(self) -> Token:
        return self.tokens[self.index - 1]

    def at_end(self) -> bool:
        return self.peek().tipo is TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.index]


def parsear(fonte: str) -> Programa:
    """Analisa uma entrada textual da MiniLang e devolve a AST."""
    tokens, _ = Lexer(fonte).scan_tokens()
    return Parser(tokens).parse_programa()
