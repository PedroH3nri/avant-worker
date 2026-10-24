"""Checagem de clean code do Groone Avant: nomes claros e um comentário curto por função.

Regras (docs/skills/avant-clean-code):
- toda função e método tem docstring de 1 ou 2 linhas (dunders e @overload ficam de fora);
- nada de comentário ao lado do código (só `# noqa`, `# type:` e `# pragma:`);
- nada de nome de uma letra só em variável, argumento ou laço (`_` pode).

Uso: `uv run python scripts/clean_code.py` confere todo o src/ e sai com 1 se algo falhar.
"""

import ast
import io
import pathlib
import sys
import tokenize

SOURCE_DIR = pathlib.Path("src")
SKIPPED_PARTS = {"migrations", "__pycache__"}
ALLOWED_COMMENT_PREFIXES = ("# noqa", "# type:", "# pragma:")
MAX_DOCSTRING_LINES = 2

FunctionNode = ast.FunctionDef | ast.AsyncFunctionDef


def source_files() -> list[pathlib.Path]:
    """Arquivos Python de src/, sem migrations geradas pelo Alembic."""
    return sorted(path for path in SOURCE_DIR.rglob("*.py") if not SKIPPED_PARTS & set(path.parts))


def is_exempt(function: FunctionNode) -> bool:
    """Dunders e assinaturas @overload não precisam de docstring."""
    if function.name.startswith("__") and function.name.endswith("__"):
        return True
    return any(
        (isinstance(decorator, ast.Name) and decorator.id == "overload")
        or (isinstance(decorator, ast.Attribute) and decorator.attr == "overload")
        for decorator in function.decorator_list
    )


def docstring_problems(tree: ast.AST) -> list[tuple[int, str]]:
    """Funções sem docstring ou com docstring maior que duas linhas."""
    problems = []
    for node in ast.walk(tree):
        if not isinstance(node, FunctionNode) or is_exempt(node):
            continue
        docstring = ast.get_docstring(node)
        if not docstring:
            problems.append((node.lineno, f"função {node.name} sem comentário de 1 ou 2 linhas"))
        elif len([line for line in docstring.splitlines() if line.strip()]) > MAX_DOCSTRING_LINES:
            problems.append((node.lineno, f"comentário de {node.name} passa de 2 linhas"))
    return problems


def single_letter_names(tree: ast.AST) -> list[tuple[int, str]]:
    """Variáveis, argumentos e alvos de laço com nome de uma letra só."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            found.append((node.lineno, node.id))
        elif isinstance(node, ast.arg):
            found.append((node.lineno, node.arg))
        elif isinstance(node, ast.ExceptHandler) and node.name:
            found.append((node.lineno, node.name))
    return [
        (line, f"nome '{name}' pouco claro")
        for line, name in found
        if len(name) == 1 and name != "_"
    ]


def inline_comments(source: str) -> list[tuple[int, str]]:
    """Comentários na mesma linha de um código."""
    found = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.COMMENT:
            continue
        before = token.line[: token.start[1]].strip()
        if before and not token.string.startswith(ALLOWED_COMMENT_PREFIXES):
            found.append((token.start[0], "comentário ao lado do código"))
    return found


def check_file(path: pathlib.Path) -> list[str]:
    """Todos os problemas de um arquivo, em ordem de linha."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    problems = sorted(
        docstring_problems(tree) + single_letter_names(tree) + inline_comments(source)
    )
    return [f"{path}:{line}: {message}" for line, message in problems]


def main() -> int:
    """Roda a checagem e devolve 1 quando há algum problema."""
    problems = [problem for path in source_files() for problem in check_file(path)]
    print("\n".join(problems) if problems else "clean code ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
