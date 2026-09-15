"""Analisador léxico da MiniLang."""

from minilang.diagnostics import Diagnostico
from minilang.lexer import Lexer, tokenizar
from minilang.tokens import PALAVRAS_RESERVADAS, Token, TokenType

__all__ = [
    "Diagnostico",
    "Lexer",
    "PALAVRAS_RESERVADAS",
    "Token",
    "TokenType",
    "tokenizar",
]
