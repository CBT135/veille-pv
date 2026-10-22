#!/usr/bin/env python3
"""Régénère editions/index.json et editions/search.json à partir des fichiers editions/AAAA-MM-JJ*.md.

Usage : python3 tools/build_index.py   (depuis la racine du dépôt)
Chaque édition est un fichier Markdown :
  # Titre
  **Période couverte :** ...
  ## L'essentiel
  - point 1
  ...
"""
import json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
ED = ROOT / "editions"
NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})([-_a-z0-9]*)\.md$")


def strip_md(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return re.sub(r"[*_`]", "", s).strip()


def parse(path):
    m = NAME.match(path.name)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), path.stem)
    periode = ""
    for l in lines:
        if l.lower().startswith("**période"):
            periode = strip_md(l.split(":", 1)[1]) if ":" in l else strip_md(l)
            break
    essentiel, sections, cur = [], [], None
    for l in lines:
        if l.startswith("## "):
            cur = l[3:].strip()
            sections.append(cur)
            continue
        if cur and cur.lower().startswith("l'essentiel") and l.startswith("- "):
            essentiel.append(strip_md(l[2:]))
    items = sum(1 for l in lines if re.match(r"^\*\*[^*]+\*\*\s*$", l.strip()))
    return {
        "id": path.stem,
        "date": m.group(1),
        "file": f"editions/{path.name}",
        "title": title,
        "periode": periode,
        "essentiel": essentiel,
        "sections": [s for s in sections if s.lower() not in ("l'essentiel", "sources")],
        "items": items,
    }


def main():
    eds = [parse(p) for p in ED.iterdir() if NAME.match(p.name)]
    eds.sort(key=lambda e: (e["date"], e["id"]), reverse=True)
    out = {
        "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "editions": eds,
    }
    (ED / "index.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    # Index de recherche plein texte : le texte brut de toutes les éditions dans un seul fichier
    search = {"updated": out["updated"], "docs": {}}
    for e in eds:
        md = (ROOT / e["file"]).read_text(encoding="utf-8")
        md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)
        md = re.sub(r"[*#_`]", "", md)
        search["docs"][e["id"]] = re.sub(r"\s+", " ", md).strip()
    (ED / "search.json").write_text(json.dumps(search, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(eds)} édition(s) indexée(s), index de recherche écrit")


if __name__ == "__main__":
    main()
