import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def rodar(*args):
     
    ambiente = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, "main.py", *args],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=ambiente,
    )


def test_programa_valido_sai_com_codigo_zero():
    resultado = rodar("examples/programa.min")
    assert resultado.returncode == 0
    assert "AST ESPERADA" not in resultado.stdout
    assert "Programa" in resultado.stdout


def test_programa_valido_nao_lista_diagnosticos():
    resultado = rodar("examples/programa.min")
    assert "erro léxico" not in resultado.stdout
    assert "ERRO SINTÁTICO" not in resultado.stdout


def test_programa_valido_imprime_estruturas_de_controle_e_blocos():
    resultado = rodar("examples/programa.min")
    assert "├── Se" in resultado.stdout
    assert "├── Enquanto" in resultado.stdout
    assert "└── Para" in resultado.stdout
    assert "Bloco" in resultado.stdout


def test_programa_com_erros_sai_com_codigo_um():
    resultado = rodar("examples/erros.min")
    assert resultado.returncode == 1
    assert "erro léxico" in resultado.stdout
    assert "@" in resultado.stdout


def test_arquivo_inexistente_sai_com_codigo_dois():
    resultado = rodar("examples/nao_existe.min")
    assert resultado.returncode == 2


def test_uso_sem_argumento_sai_com_codigo_dois():
    resultado = rodar()
    assert resultado.returncode == 2
    assert "uso:" in resultado.stderr
