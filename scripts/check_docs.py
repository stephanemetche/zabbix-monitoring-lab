#!/usr/bin/env python3
"""Contrôles de qualité de la documentation (aucune dépendance).

Vérifie dans tous les .md : blocs de code fermés, liens et images relatifs
existants, titres bien formés, absence de secrets évidents.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BAD_HEADING = re.compile(r"^#{1,6}[^#\s]")
SECRET = re.compile(r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key)\s*[:=]\s*[^\s<*$\"']{4,}")


def check(path: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)
    in_fence = False
    fence_line = 0
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence, fence_line = (not in_fence), n
            continue
        if in_fence:
            if SECRET.search(line):
                errors.append(f"{rel}:{n}: secret potentiel dans un bloc de code")
            continue
        if BAD_HEADING.match(line):
            errors.append(f"{rel}:{n}: titre mal formé (espace manquant après #)")
        for target in LINK.findall(line):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            file_part = target.split("#", 1)[0]
            if file_part and not (path.parent / file_part).resolve().exists():
                errors.append(f"{rel}:{n}: lien ou image introuvable : {target}")
    if in_fence:
        errors.append(f"{rel}:{fence_line}: bloc de code non fermé")
    return errors


def main() -> int:
    files = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
    errors = [e for f in sorted(files) for e in check(f)]
    for e in errors:
        print(f"ERREUR {e}")
    print(f"{len(files)} fichiers .md contrôlés, {len(errors)} erreur(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
