# Analisador Léxico da MiniLang

Implementação manual do lexer da MiniLang: percorre o código-fonte da esquerda
para a direita, símbolo a símbolo, e produz a lista de tokens e a lista de
diagnósticos de símbolos inválidos.

## 1. Integrantes

* *Luis Felipi Ildefonco Lins* - 1996781
* *Hugo Loiola de Oliveira* - 2013653
* *Wallaf Felipe Lyra de Oliveira* - 2003058
* *Felipe Sizilio Pelissari de Oliveira* - 1990260
* *Bruno Henrique Albertoni Silva* - 1988433

## 2. Execução

```
python main.py examples/programa.min
python main.py examples/erros.min
```

A saída traz a tabela de tokens (`linha:coluna`, tipo e lexema) seguida da lista
de diagnósticos. Código de saída: `0` sem diagnósticos, `1` quando há símbolo
inválido, `2` para erro de uso ou de leitura do arquivo.

## 3. Testes

```
python -m pytest tests/ -v
```

São 96 testes. O pytest é a única dependência, e serve só aos testes — o lexer
usa apenas a biblioteca padrão. Instale com `pip install pytest` se necessário.

## 4. Organização do lexer

| Arquivo | Responsabilidade |
| :--- | :--- |
| `minilang/tokens.py` | `TokenType` (24 tipos), `Token` e a tabela `PALAVRAS_RESERVADAS` |
| `minilang/diagnostics.py` | `Diagnostico`: símbolo inválido, linha, coluna e mensagem |
| `minilang/alfabeto.py` | Definição manual do alfabeto e normalização CRLF→NL |
| `minilang/lexer.py` | Classe `Lexer`: estado da varredura e as 12 operações |
| `main.py` | Leitura do arquivo e formatação da saída |

A classe `Lexer` mantém `source`, `start`, `current`, `line`, `column`,
`start_line`, `start_column`, `tokens` e `diagnostics`, e implementa
`scan_tokens`, `scan_token`, `at_end`, `advance`, `peek`, `peek_next`, `match`,
`add_token`, `identifier`, `number`, `line_comment` e
`report_invalid_character`.

Decisões centrais:

* **Maior casamento.** `scan_token()` consome o maior lexema válido antes de
  classificar. Por isso `intx` é um `IDENT` inteiro: a tabela de palavras
  reservadas só é consultada em `identifier()`, depois que toda a continuação
  foi consumida. O mesmo vale para `===`, que vira `EQUAL_EQUAL` e `ASSIGN`.
* **Posição em um lugar só.** `advance()` é o único método que altera `line` e
  `column`. `match()` consome através dele, o que evita duas implementações
  divergentes de controle de posição.
* **Alfabeto manual.** `alfabeto.py` compara faixas de code points ASCII em vez
  de usar `re`, `isalpha()` ou `isdigit()`. Como `ã` é U+00E3, acima de `z`, a
  comparação já rejeita acentos sem tratamento especial.
* **Progresso garantido.** Todo símbolo inválido é consumido *antes* do
  diagnóstico ser registrado, então cada iteração de `scan_tokens()` avança pelo
  menos uma posição. Não há entrada capaz de provocar laço infinito.

## 5. Limitações conhecidas

* **Alfabeto restrito a ASCII.** Letras acentuadas geram diagnóstico por
  definição do padrão IDENT_BASE. `vãlor` produz `IDENT("v")`, um diagnóstico
  para `ã` e `IDENT("lor")`.
* **Sem análise sintática.** O lexer não julga se a sequência de tokens forma um
  programa válido. `2total` produz `INT_LITERAL("2")` e `IDENT("total")` sem
  erro léxico; essa decisão cabe ao analisador sintático.
* **CR solitário conta como quebra de linha.** Arquivos no padrão Mac clássico
  avançam a linha corretamente, mas o par CRLF é normalizado antes da varredura
  para não contar duas linhas.
* **Recuperação de erro mínima.** Diante de símbolo inválido o lexer consome um
  único símbolo e segue. Não há tentativa de agrupar erros vizinhos nem de
  sugerir correções.
