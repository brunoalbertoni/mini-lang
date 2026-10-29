"""Ponto de entrada do analisador sintático da MiniLang.

Uso:
    python main.py examples/programa.min
"""

import sys
from minilang import Lexer
from minilang.parser import ParseError, parsear

CODIGO_SUCESSO = 0
CODIGO_COM_DIAGNOSTICOS = 1
CODIGO_ERRO_DE_USO = 2

def imprimir_ast(no, prefixo="", eh_ultimo=True):
    """Imprime a AST no terminal com formato de árvore visual."""
    nome_classe = no.__class__.__name__
    
    # Prepara o marcador visual para a ramificação
    marcador = "└── " if eh_ultimo else "├── "
    prefixo_filhos = prefixo + ("    " if eh_ultimo else "│   ")
    
    # Imprime o nó atual formatado conforme o diagrama
    if nome_classe == "Programa":
        print(f"Programa")
        for i, decl in enumerate(no.declaracoes):
            imprimir_ast(decl, "", i == len(no.declaracoes) - 1)
            
    elif nome_classe == "Declaracao":
        print(f"{prefixo}{marcador}Declaracao({no.nome})")
        
    elif nome_classe == "Atribuicao":
        print(f"{prefixo}{marcador}Atribuicao({no.nome})")
        imprimir_ast(no.valor, prefixo_filhos, True)
        
    elif nome_classe == "Saida":
        print(f"{prefixo}{marcador}Saida")
        imprimir_ast(no.expressao, prefixo_filhos, True)
        
    elif nome_classe == "Binaria":
        print(f"{prefixo}{marcador}Binaria({no.operador})")
        imprimir_ast(no.esquerda, prefixo_filhos, False)
        imprimir_ast(no.direita, prefixo_filhos, True)
        
    elif nome_classe == "Inteiro":
        print(f"{prefixo}{marcador}Inteiro({no.valor})")
        
    elif nome_classe == "Variavel":
        print(f"{prefixo}{marcador}Variavel({no.nome})")


def main(argv: list[str]) -> int:
    """Lê o arquivo, executa a análise sintática e imprime a AST."""
    if len(argv) != 2:
        print("uso: python main.py <arquivo.min>", file=sys.stderr)
        return CODIGO_ERRO_DE_USO

    caminho = argv[1]

    try:
        with open(caminho, "r", encoding="utf-8-sig") as arquivo:
            fonte = arquivo.read()
    except OSError as erro:
        print(f"não foi possível ler {caminho}: {erro}", file=sys.stderr)
        return CODIGO_ERRO_DE_USO

    # 1. Verifica erros léxicos primeiro
    _, diagnosticos = Lexer(fonte).scan_tokens()
    if diagnosticos:
        print("DIAGNÓSTICOS LÉXICOS ENCONTRADOS:\n")
        for d in diagnosticos:
            print(f"{d.linha}:{d.coluna} erro léxico: {d.mensagem}")
        return CODIGO_COM_DIAGNOSTICOS

    # 2. Executa o parser e captura erros sintáticos
    try:
        ast = parsear(fonte)
        print("AST ESPERADA\n")
        imprimir_ast(ast)
        print()
        return CODIGO_SUCESSO
    except ParseError as erro:
        print("ERRO SINTÁTICO:\n")
        print(erro)
        return CODIGO_COM_DIAGNOSTICOS
    except Exception as e:
        print(f"ERRO INTERNO: {e}")
        return CODIGO_COM_DIAGNOSTICOS

if __name__ == "__main__":
    sys.exit(main(sys.argv))