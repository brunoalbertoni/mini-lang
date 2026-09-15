"""Diagnósticos emitidos pelo lexer para símbolos fora do alfabeto."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Diagnostico:
    """Registro de um símbolo inválido encontrado durante a varredura."""

    simbolo: str
    linha: int
    coluna: int
    mensagem: str

    def __str__(self) -> str:
        return f"{self.linha}:{self.coluna} erro léxico: {self.mensagem}"
