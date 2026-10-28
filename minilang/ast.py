"""Árvores sintáticas abstratas da MiniLang."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Programa:
    declaracoes: list[Any] = field(default_factory=list)


@dataclass(frozen=True)
class Declaracao:
    nome: str


@dataclass(frozen=True)
class Atribuicao:
    nome: str
    valor: Any


@dataclass(frozen=True)
class Saida:
    expressao: Any


@dataclass(frozen=True)
class Variavel:
    nome: str


@dataclass(frozen=True)
class Inteiro:
    valor: int


@dataclass(frozen=True)
class Binaria:
    operador: str
    esquerda: Any
    direita: Any


@dataclass(frozen=True)
class Bloco:
    instrucoes: list[Any] = field(default_factory=list)


@dataclass(frozen=True)
class Se:
    condicao: Any
    entao: Any
    senao: Any | None = None


@dataclass(frozen=True)
class Enquanto:
    condicao: Any
    corpo: Any
