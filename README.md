# Justicia Académie

Site web de Justicia Académie — préparation à l'entrée dans les études de droit
pour les lycéens de première, terminale et les étudiants de L1. Centre à Paris.

Site statique (HTML/CSS/JS), aucune dépendance de build pour le consulter :
ouvrir `index.html` ou servir le dossier avec un serveur statique.

## Structure

- `index.html`, `etudes-de-droit.html`, `conseils.html` — pages principales
- `formule-*.html` — les quatre formules (Terminale et L1)
- `specialites-lycee-droit.html`, `parcoursup-licence-droit.html`,
  `l1-droit-difficulte.html`, `methode-commentaire-arret.html` — articles
- `espace-eleve.html` + `fiches/` — espace élève (démonstration) et fiches de
  cours réservées aux abonnés
- `styles.css`, `script.js` — styles et interactions partagés
- `_build_pages.py`, `_build_fiches_index.py` — générateurs des pages
  formule/conseils et de l'index des fiches (relancer après modification)
- `SEO-CHECKLIST.md` — état du référencement et actions restantes

## Régénérer les pages générées

```
python3 _build_pages.py
python3 _build_fiches_index.py
```
