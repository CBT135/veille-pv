# Veille PV & BESS

Application web (PWA) de lecture de la veille quotidienne photovoltaïque au sol et stockage par batteries. Même charte graphique que « Relevé de masque ».

URL : https://cbt135.github.io/veille-pv/

## Installation sur iPhone

1. Ouvrir l'URL dans Chrome (iOS 16.4 ou plus) ou Safari.
2. Partager › **Ajouter à l'écran d'accueil**.
3. L'application s'ouvre en plein écran. Les 30 dernières éditions (et toutes celles déjà ouvertes) restent lisibles hors ligne ; la recherche couvre toutes les éditions, même hors ligne.

## Publication GitHub Pages (une seule fois)

Settings › Pages › Source : *Deploy from a branch* › `main` / `(root)`.

## Ajouter une édition

1. Déposer `editions/AAAA-MM-JJ.md` (un suffixe est permis, par exemple `2026-10-22-test.md`).
2. Lancer `python3 tools/build_index.py`, qui régénère `editions/index.json` et l'index de recherche `editions/search.json`.
3. Faire un commit puis un push.

### Format d'une édition

```
# Veille PV & BESS — jeudi 22 octobre 2026

**Période couverte :** mercredi 21 → jeudi 22 octobre.

## L'essentiel

- point 1
- point 2

## Réglementation & tarifs

**Titre de l'item**
Deux ou trois phrases.
*Impact AMO / projet sol :* une phrase.
[Source](https://…)

## À surveiller

- **27 octobre** : …

## Sources

- [Titre](https://…)
```

## Fichiers

- `index.html` : l'application, autonome, sans dépendance hormis les polices Google.
- `sw.js` : le cache hors ligne. Les éditions sont chargées « réseau d'abord ».
- `manifest.webmanifest` et les icônes : l'installation sur l'écran d'accueil.
- `editions/` : les éditions en Markdown et `index.json`.
- `tools/build_index.py` : la génération de la liste et de l'index de recherche.
