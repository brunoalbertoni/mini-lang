"""Parser descendente recursivo da MiniLang - Trabalho 02."""

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
    Para,
    Programa,
    Saida,
    Se,
    Variavel,
)

class ParseError(Exception):
    """Erro sintático detectado durante a análise."""
    def __init__(self, mensagem: str, token: Token):
        super().__init__(f"Erro sintático na linha {token.linha}, coluna {token.coluna} no token '{token.lexema}': {mensagem}")
        self.token = token

class Parser:
    """Analisa uma sequência de tokens e produz uma AST."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    # ==========================================
    # ETAPA 2: Comandos e Programa
    # ==========================================
    def programa(self) -> Programa:
        """Nó raiz do programa."""
        return Programa(self.lista_itens())

    def lista_itens(self) -> list[Any]:
        """Consome uma sequência de itens até o fim do arquivo."""
        instrucoes = []
        while not self.at_end():
            instrucoes.append(self.item())
        return instrucoes

    def item(self) -> Any:
        """Roteia para um comando da linguagem."""
        if self.match(TokenType.KW_INT):
            return self.declaracao()
        if self.match(TokenType.KW_PRINT):
            return self.saida()
        if self.match(TokenType.KW_IF):
            return self.condicional()
        if self.match(TokenType.KW_WHILE):
            return self.enquanto()
        if self.match(TokenType.KW_FOR):
            return self.para()
        if self.match(TokenType.LBRACE):
            return self.bloco()
        
        # Se não for int nem print, obrigatoriamente deve ser uma atribuição
        return self.atribuicao()

    def atribuicao(self, consumir_ponto_e_virgula: bool = True) -> Atribuicao:
        """Reconhece uma atribuição, opcionalmente consumindo seu ';'."""
        nome_token = self.expect(TokenType.IDENT, "esperado identificador para atribuição")
        nome = nome_token.lexema
        self.expect(TokenType.ASSIGN, "esperado '=' após o identificador")
        valor = self.expressao()
        if consumir_ponto_e_virgula:
            self.expect(TokenType.SEMICOLON, "esperado ';' após atribuição")
        return Atribuicao(nome, valor)

    def declaracao(self) -> Declaracao:
        """Reconhece: int ident ;"""
        nome = self.expect(TokenType.IDENT, "esperado identificador após 'int'").lexema
        self.expect(TokenType.SEMICOLON, "esperado ';' após declaração")
        return Declaracao(nome)

    def saida(self) -> Saida:
        """Reconhece: print ( expressao ) ;"""
        self.expect(TokenType.LPAREN, "esperado '(' após 'print'")
        expr = self.expressao()
        self.expect(TokenType.RPAREN, "esperado ')' após expressão")
        self.expect(TokenType.SEMICOLON, "esperado ';' após print")
        return Saida(expr)

    def bloco(self) -> Bloco:
        """Reconhece uma sequência de comandos entre chaves."""
        instrucoes = []
        while not self.check(TokenType.RBRACE) and not self.at_end():
            instrucoes.append(self.item())
        self.expect(TokenType.RBRACE, "esperado '}' para fechar bloco")
        return Bloco(instrucoes)

    def condicao(self) -> Any:
        """Reconhece uma comparação entre duas expressões aritméticas."""
        esquerda = self.expressao()
        operadores = (
            TokenType.EQUAL_EQUAL,
            TokenType.BANG_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        )
        if not self.check_any(*operadores):
            raise ParseError("esperado operador relacional na condição", self.peek())
        operador = self.advance().lexema
        direita = self.expressao()
        return Binaria(operador, esquerda, direita)

    def condicao_parentizada(self) -> Any:
        self.expect(TokenType.LPAREN, "esperado '(' antes da condição")
        condicao = self.condicao()
        self.expect(TokenType.RPAREN, "esperado ')' após a condição")
        return condicao

    def condicional(self) -> Se:
        """Reconhece: if (condição) bloco [else bloco|if]."""
        condicao = self.condicao_parentizada()
        self.expect(TokenType.LBRACE, "esperado '{' após condição do if")
        entao = self.bloco()
        senao = None
        if self.match(TokenType.KW_ELSE):
            if self.match(TokenType.KW_IF):
                senao = self.condicional()
            else:
                self.expect(TokenType.LBRACE, "esperado '{' após 'else'")
                senao = self.bloco()
        return Se(condicao, entao, senao)

    def enquanto(self) -> Enquanto:
        """Reconhece: while (condição) bloco."""
        condicao = self.condicao_parentizada()
        self.expect(TokenType.LBRACE, "esperado '{' após condição do while")
        return Enquanto(condicao, self.bloco())

    def para(self) -> Para:
        """Reconhece: for (inicialização; condição; incremento) bloco.

        As três cláusulas podem ficar vazias. A inicialização aceita uma
        atribuição ou uma declaração (com inicializador opcional).
        """
        self.expect(TokenType.LPAREN, "esperado '(' após 'for'")

        inicializacao = None
        if not self.check(TokenType.SEMICOLON):
            if self.match(TokenType.KW_INT):
                nome = self.expect(TokenType.IDENT, "esperado identificador após 'int'").lexema
                valor = None
                if self.match(TokenType.ASSIGN):
                    valor = self.expressao()
                inicializacao = Declaracao(nome, valor)
            else:
                inicializacao = self.atribuicao(consumir_ponto_e_virgula=False)
        self.expect(TokenType.SEMICOLON, "esperado ';' após inicialização do for")

        condicao = None
        if not self.check(TokenType.SEMICOLON):
            condicao = self.condicao()
        self.expect(TokenType.SEMICOLON, "esperado ';' após condição do for")

        incremento = None
        if not self.check(TokenType.RPAREN):
            incremento = self.atribuicao(consumir_ponto_e_virgula=False)
        self.expect(TokenType.RPAREN, "esperado ')' após cláusulas do for")
        self.expect(TokenType.LBRACE, "esperado '{' após cláusulas do for")
        return Para(inicializacao, condicao, incremento, self.bloco())

    # ==========================================
    # ETAPA 1: Expressões Matemáticas
    # ==========================================
    def expressao(self) -> Any:
        """Reconhece operadores aditivos (+, -) preservando precedência à esquerda."""
        expr = self.termo()
        while self.check_any(TokenType.PLUS, TokenType.MINUS):
            operador = self.advance().lexema
            direita = self.termo()
            expr = Binaria(operador, expr, direita)
        return expr

    def termo(self) -> Any:
        """Reconhece operadores multiplicativos (*, /) preservando precedência à esquerda."""
        expr = self.fator()
        while self.check_any(TokenType.STAR, TokenType.SLASH):
            operador = self.advance().lexema
            direita = self.fator()
            expr = Binaria(operador, expr, direita)
        return expr

    def fator(self) -> Any:
        """Reconhece literais, variáveis ou expressões entre parênteses."""
        if self.match(TokenType.INT_LITERAL):
            return Inteiro(int(self.previous().lexema))
        if self.match(TokenType.IDENT):
            return Variavel(self.previous().lexema)
        if self.match(TokenType.LPAREN):
            expr = self.expressao()
            self.expect(TokenType.RPAREN, "esperado ')' após expressão")
            return expr
        
        # Etapa 3: Falha no primeiro erro encontrado com token detalhado
        raise ParseError("expressão inválida", self.peek())

    # ==========================================
    # Funções Auxiliares (Já prontas / Mantidas)
    # ==========================================
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
        raise ParseError(mensagem, self.peek())

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
    tokens, diagnósticos = Lexer(fonte).scan_tokens()
    # Verifica se o lexer já disparou algum erro antes de passar ao parser
    if diagnósticos:
        raise ValueError(f"Erros léxicos encontrados: {diagnósticos}")
    
    return Parser(tokens).programa()