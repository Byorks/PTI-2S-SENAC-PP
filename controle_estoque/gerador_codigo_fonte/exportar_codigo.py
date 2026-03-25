from __future__ import annotations

import argparse
import html
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceFile:
    path: Path
    rel_posix: str
    language: str


def _language_for(path: Path) -> str:
    return {
        ".py": "python",
        ".toml": "toml",
        ".md": "markdown",
        ".txt": "text",
    }.get(path.suffix.lower(), "")


def _read_text_robust(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            text = path.read_text(encoding=encoding)
            return text.replace("\r\n", "\n").replace("\r", "\n")
        except UnicodeDecodeError:
            continue

    text = path.read_text(encoding="utf-8", errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _md_fence_for(text: str) -> str:
    max_run = 0
    run = 0
    for ch in text:
        if ch == "`":
            run += 1
            max_run = max(max_run, run)
        else:
            run = 0
    return "`" * max(3, max_run + 1)


def _sort_key(rel_posix: str) -> tuple[int, str]:
    if rel_posix == "README.md":
        return (0, rel_posix)
    if rel_posix == "controle_estoque/pyproject.toml":
        return (1, rel_posix)

    if rel_posix.endswith("/src/app/config.py"):
        return (2, rel_posix)
    if rel_posix.endswith("/src/app/main.py"):
        return (3, rel_posix)

    if "/src/app/models/" in rel_posix:
        return (4, rel_posix)

    if rel_posix.endswith("/src/app/repositories/protocols.py"):
        return (5, rel_posix)
    if rel_posix.endswith("/src/app/repositories/memoria_produtos.py"):
        return (6, rel_posix)
    if rel_posix.endswith("/src/app/repositories/produtos.py"):
        return (7, rel_posix)
    if "/src/app/repositories/" in rel_posix:
        return (8, rel_posix)

    if "/src/app/services/" in rel_posix:
        return (9, rel_posix)
    if "/src/app/utils/" in rel_posix:
        return (10, rel_posix)

    return (50, rel_posix)


def collect_files(repo_root: Path, include_readme: bool, include_pyproject: bool) -> list[SourceFile]:
    files: list[SourceFile] = []

    if include_readme:
        readme = repo_root / "README.md"
        if readme.is_file():
            rel = readme.relative_to(repo_root).as_posix()
            files.append(SourceFile(readme, rel, _language_for(readme)))

    if include_pyproject:
        pyproject = repo_root / "controle_estoque" / "pyproject.toml"
        if pyproject.is_file():
            rel = pyproject.relative_to(repo_root).as_posix()
            files.append(SourceFile(pyproject, rel, _language_for(pyproject)))

    app_dir = repo_root / "controle_estoque" / "src" / "app"
    if app_dir.is_dir():
        for p in app_dir.rglob("*.py"):
            if not p.is_file():
                continue
            if "__pycache__" in p.parts or "controle_estoque.egg-info" in p.parts:
                continue
            if p.name == "__init__.py":
                continue

            rel = p.relative_to(repo_root).as_posix()
            files.append(SourceFile(p, rel, _language_for(p)))

    files.sort(key=lambda f: _sort_key(f.rel_posix))
    return files


def build_markdown(files: list[SourceFile]) -> str:
    parts: list[str] = ["# Código-fonte\n"]
    parts.append("Este arquivo foi gerado automaticamente para facilitar a entrega em PDF.\n")

    for f in files:
        content = _read_text_robust(f.path)
        fence = _md_fence_for(content)
        info = f.language if f.language else ""
        parts.append(f"## {f.rel_posix}\n\n{fence}{info}\n{content.rstrip()}\n{fence}\n")

    return "\n".join(parts).rstrip() + "\n"


def build_html(files: list[SourceFile]) -> str:
    toc_items = "\n".join(
        f'<li><a href="#f{i}">{html.escape(f.rel_posix)}</a></li>'
        for i, f in enumerate(files)
    )

    sections: list[str] = []
    for i, f in enumerate(files):
        content = _read_text_robust(f.path)
        lang_class = f"language-{html.escape(f.language)}" if f.language else ""
        sections.append(
            "\n".join(
                [
                    f'<section class="file-section" id="f{i}">',
                    f'  <div class="file-header">{html.escape(f.rel_posix)}</div>',
                    f'  <pre><code class="{lang_class}">{html.escape(content, quote=False)}</code></pre>',
                    "</section>",
                ]
            )
        )

    return (
        "<!doctype html>\n"
        '<html lang="pt-br">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "  <title>Código-fonte</title>\n"
        "  <style>\n"
        "    :root { --font: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; }\n"
        "    body { font-family: var(--font); font-size: 10.5pt; line-height: 1.35; color: #111; }\n"
        "    a { color: inherit; }\n"
        "    .toc { margin: 0.7in; }\n"
        "    .toc h1 { font-size: 16pt; margin: 0 0 0.2in; }\n"
        "    .toc ul { margin: 0.15in 0 0 0.25in; padding: 0; }\n"
        "    .toc li { margin: 0.05in 0; }\n"
        "    .file-section { page-break-after: always; break-after: page; padding: 0.6in 0.7in; }\n"
        "    .file-header { font-weight: 700; margin: 0 0 0.15in; word-break: break-word; }\n"
        "    pre { margin: 0; padding: 0.15in; border: 1px solid #ddd; background: #fafafa; }\n"
        "    code { white-space: pre-wrap; overflow-wrap: anywhere; }\n"
        "    @page { size: A4; margin: 0.6in; }\n"
        "    @media print { .toc { page-break-after: always; break-after: page; } }\n"
        "  </style>\n"
        "</head>\n"
        "<body>\n"
        "  <div class=\"toc\">\n"
        "    <h1>Código-fonte</h1>\n"
        "    <div>Conteúdo:</div>\n"
        f"    <ul>{toc_items}</ul>\n"
        "  </div>\n"
        f"  {'\n\n'.join(sections)}\n"
        "</body>\n"
        "</html>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera controle_estoque/codigo_fonte.html e controle_estoque/codigo_fonte.md para impressão em PDF."
    )
    parser.add_argument("--no-readme", action="store_true", help="Não incluir README.md")
    parser.add_argument(
        "--no-pyproject",
        action="store_true",
        help="Não incluir controle_estoque/pyproject.toml",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    out_dir = repo_root / "controle_estoque"
    out_dir.mkdir(parents=True, exist_ok=True)

    files = collect_files(
        repo_root=repo_root,
        include_readme=not args.no_readme,
        include_pyproject=not args.no_pyproject,
    )

    if not files:
        raise SystemExit("Nenhum arquivo encontrado para exportar.")

    (out_dir / "codigo_fonte.md").write_text(build_markdown(files), encoding="utf-8", newline="\n")
    (out_dir / "codigo_fonte.html").write_text(build_html(files), encoding="utf-8", newline="\n")

    print(f"OK: gerado {out_dir / 'codigo_fonte.html'}")
    print(f"OK: gerado {out_dir / 'codigo_fonte.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
