# Analisador Sintático (Parser) da MiniLang - Trabalho 02

Implementação de um parser descendente recursivo para a MiniLang, construído sobre o analisador léxico prévio. O parser consome a lista de tokens, avalia a gramática da linguagem, constrói uma Árvore Sintática Abstrata (AST) e relata erros sintáticos precisos.

## 1. Integrantes

*Luis Felipi Ildefonco Lins* 1996781
*Hugo Loiola de Oliveira* 2013653
*Wallaf Felipe Lyra de Oliveira* 2003058
*Felipe Sizilio Pelissari de Oliveira* 1990260
*Bruno Henrique Albertoni Silva* 1988433

## 2. Execução

```powershell
python main.py examples/programa.min
```

A saída do programa agora executa duas fases:
1. **Fase Léxica:** Se houver símbolos inválidos, exibe os diagnósticos e encerra.
2. **Fase Sintática:** Se a sintaxe for válida, exibe no terminal a **Árvore Sintática Abstrata (AST)** formatada. Se o código for malformado (ex: `print(2+);`), a execução para imediatamente no primeiro erro e exibe a linha, a coluna e o token inesperado.

## 3. Testes

```powershell
python -m pytest
```

São **102 testes** automatizados cobrindo tanto as regras do Analisador Léxico quanto as novas regras do Analisador Sintático (Precedência, Associatividade à esquerda e Erros). O `pytest` é a única dependência. Instale com `pip install pytest` se necessário.

## 4. Organização do Projeto

| Arquivo | Responsabilidade |
| :--- | :--- |
| `minilang/parser.py` | Classe `Parser`: implementa a descida recursiva (expressões e comandos). |
| `minilang/ast.py` | Estruturas de dados (DataClasses) que formam os nós da AST (`Programa`, `Binaria`, `Atribuicao`, etc). |
| `minilang/tokens.py` | `TokenType` (24 tipos), `Token` e a tabela `PALAVRAS_RESERVADAS`. |
| `minilang/diagnostics.py` | `Diagnostico`: símbolo inválido, linha, coluna e mensagem. |
| `minilang/alfabeto.py` | Definição manual do alfabeto e normalização CRLF→NL. |
| `minilang/lexer.py` | Classe `Lexer`: estado da varredura e operações léxicas. |
| `main.py` | Leitura do arquivo e ponto de entrada da compilação. |

### Decisões centrais do Parser (Trabalho 02):

*   **Descida Recursiva:** As regras da gramática foram mapeadas diretamente para métodos estruturais: `programa()`, `lista_itens()`, `item()`, `atribuicao()`, `declaracao()` e `saida()`.
*   **Precedência e Associatividade (Etapa 1):** Tratadas através do encadeamento de chamadas `expressao()` (Somas/Subtrações) -> `termo()` (Multiplicações/Divisões) -> `fator()` (Agrupamentos e Literais). O uso de laços `while` no parser garante a associatividade à esquerda, agrupando `10 - 3 - 2` corretamente como `(10 - 3) - 2`.
*   **Diagnóstico Fail-Fast (Etapa 3):** O parser aborta a execução no primeiro erro sintático detectado. A exceção customizada `ParseError` captura o token atual para gerar mensagens amigáveis informando exatamente onde o código quebrou.

### Decisões centrais do Lexer (Trabalho 01):

*   **Maior casamento:** O lexer consome o maior lexema válido antes de classificar (ex: `intx` é um `IDENT` inteiro, não `KW_INT` + `IDENT`).
*   **Alfabeto manual:** Comparação de *code points* ASCII em vez de Regex.
*   **Progresso garantido:** Evita laços infinitos consumindo símbolos inválidos antes de registrar o diagnóstico léxico.

## 5. Limitações de Escopo (Trabalho 02)

*   **Escopo Restrito do Parser:** Conforme estipulado nos requisitos obrigatórios, a implementação atual foca unicamente em `int`, `print`, atribuições e expressões matemáticas. Comandos de bloco, condicionais (`if/else`) e laços (`while`) foram intencionalmente **removidos/ignorados** no `parser.py` para alinhar com os limites avaliativos desta entrega.
*   **Sem Execução Semântica:** A AST gerada reflete a estrutura do programa. O parser não executa as operações matemáticas (ex: não resolve `2+3`), nem faz análise semântica (como verificar se uma variável foi declarada antes de ser usada).