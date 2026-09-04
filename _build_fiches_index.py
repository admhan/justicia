# -*- coding: utf-8 -*-
"""Génère site/fiches/index.html à partir des métadonnées figées dans
_fiches_metadata.json.

Les fiches elles-mêmes ne sont plus stockées dans le dépôt : elles vivent
dans le compartiment privé Supabase Storage "fiches", livrées via URL
signée après vérification de l'abonnement (voir supabase/schema.sql).
Ce script ne fait donc que régénérer la page qui liste leurs titres.

Pour ajouter/retirer une fiche : mettre à jour _fiches_metadata.json (et
le contenu réel du compartiment Storage), puis relancer ce script.

Usage : python3 _build_fiches_index.py
"""
import json
from pathlib import Path

SITE = Path(__file__).parent
FICHES = SITE / "fiches"
METADATA = json.loads((SITE / "_fiches_metadata.json").read_text(encoding="utf-8"))

SUBJECTS = {
    "introduction-generale-au-droit": "Introduction générale au droit",
    "methodologie-universitaire": "Méthodologie universitaire",
    "droit-constitutionnel": "Droit constitutionnel",
    "histoire-du-droit": "Histoire du droit",
}

MARK_SVG = """<svg class="brand-mark" viewBox="0 0 64 68" aria-hidden="true" focusable="false">
        <g fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle class="mk-gold" cx="32" cy="34" r="28" stroke-width="1.3"/>
          <g class="mk-main" stroke-width="2.2">
            <path d="M32 20 V45"/>
            <path d="M14 20 H50"/>
            <circle cx="32" cy="15.6" r="2.3"/>
            <path d="M32 46 C25 41.5 16 41.5 10 44.5 L10 50.5 C16 47.5 25 47.5 32 52 C39 47.5 48 47.5 54 50.5 L54 44.5 C48 41.5 39 41.5 32 46 Z"/>
          </g>
          <g class="mk-gold" stroke-width="1.7">
            <path d="M14 20 L9 31 M14 20 L19 31"/>
            <path d="M7.5 31 A6.5 5 0 0 0 20.5 31"/>
            <path d="M50 20 L45 31 M50 20 L55 31"/>
            <path d="M43.5 31 A6.5 5 0 0 0 56.5 31"/>
            <path d="M13 46.6 C18.5 44.7 25 45 29.5 47.6 M51 46.6 C45.5 44.7 39 45 34.5 47.6"/>
          </g>
        </g>
      </svg>"""
WORDMARK = '<span class="brand-word"><span class="w1">Justicia</span><span class="w2">Académie</span></span>'


def gather():
    return {slug: METADATA[slug] for slug in SUBJECTS}


def render_matiere(slug, label, items, roman):
    # Chaque fiche est écrite verrouillée : c'est le navigateur qui lève le
    # verrou à la date dite (voir script.js). Sans cela, une page servie en
    # statique resterait figée sur l'état du jour de sa génération — et un
    # script cassé ouvrirait tout, au lieu de ne rien ouvrir.
    rows = "\n".join(
        f'''            <li class="fiche-item is-locked" data-date="{it['date']}">
              <span class="sub-num" aria-hidden="true">{it['num']}.</span>
              <a href="#" class="fiche-link" data-path="{slug}/{it['file']}" aria-disabled="true" tabindex="-1">{it['title']}</a>
              <span class="fiche-date"></span>
            </li>'''
        for it in items
    )
    return f'''
  <section id="{slug}">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="numeral" aria-hidden="true">{roman}.</span>
        <div class="head-text">
          <span class="head-rule" aria-hidden="true"></span>
          <h2>{label}</h2>
          <p class="fiche-count" data-total="{len(items)}">{len(items)} fiches de cours.</p>
        </div>
      </div>
      <ul class="fiche-list reveal">
{rows}
      </ul>
    </div>
  </section>'''


def render_index(data):
    romans = ["I", "II", "III", "IV"]
    sections = "\n".join(
        render_matiere(slug, data[slug]["label"], data[slug]["items"], romans[i])
        for i, slug in enumerate(SUBJECTS)
    )
    total = sum(len(data[s]["items"]) for s in SUBJECTS)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mes fiches de cours — Justicia Académie</title>
  <meta name="description" content="Fiches de cours réservées aux élèves de Justicia Académie disposant d'un abonnement actif.">
  <meta name="robots" content="noindex, nofollow">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="../index.html" aria-label="Justicia Académie, accueil">
      {MARK_SVG}
      {WORDMARK}
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Navigation principale">
      <a href="../etudes-de-droit.html">Les études de droit</a>
      <a href="../index.html#formules">Les formules</a>
      <a href="../conseils.html">Conseils</a>
      <a href="../index.html#questions">Questions</a>
      <a class="nav-espace is-connected" href="../espace-eleve.html">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.4"/><path d="M5.5 19c1.2-3.1 3.6-4.6 6.5-4.6s5.3 1.5 6.5 4.6"/></svg>
        <span class="nav-espace-label">Mon espace</span>
        <span class="status-dot" aria-hidden="true"></span>
      </a>
      <a class="btn" href="../index.html#rendez-vous">Prendre rendez-vous</a>
    </nav>
  </div>
</header>

<main>

  <section class="page-hero">
    <div class="wrap">
      <p class="crumbs"><a href="../espace-eleve.html">Mon espace</a> · Mes fiches de cours</p>
      <h1>Mes fiches de <span class="accent-italic">cours</span>.</h1>
      <p class="lede">{total} fiches réparties en quatre matières, rédigées par l'équipe pédagogique de Justicia Académie. Elles s'ouvrent au fil du semestre, au rythme du programme : chaque fiche indique sa date de mise à disposition.</p>
      <p class="login-error" id="fiche-access-error">Cette fiche n'est pas accessible : elle n'est pas encore ouverte, ou votre abonnement ne la couvre pas. Contactez votre référent pédagogique si vous pensez qu'il s'agit d'une erreur.</p>
    </div>
  </section>
{sections}

</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-brand">
      <div class="brand-lockup">
        {MARK_SVG}
        {WORDMARK}
      </div>
      <p>Préparer les lycéens et les étudiants de L1 à réussir leur entrée dans les études de droit. Centre à Paris.</p>
    </div>
    <div>
      <h4>Naviguer</h4>
      <ul>
        <li><a href="../etudes-de-droit.html">Les études de droit</a></li>
        <li><a href="../index.html#formules">Les formules</a></li>
        <li><a href="../conseils.html">Conseils</a></li>
        <li><a href="../index.html#questions">Questions</a></li>
      </ul>
    </div>
    <div>
      <h4>Les formules</h4>
      <ul>
        <li><a href="../formule-terminale-hebdomadaire.html">Terminale : formule hebdomadaire</a></li>
        <li><a href="../formule-terminale-vacances.html">Terminale : formule vacances</a></li>
        <li><a href="../formule-l1-stage-prerentree.html">L1 : stage de pré-rentrée</a></li>
        <li><a href="../formule-l1-accompagnement-annuel.html">L1 : accompagnement annuel</a></li>
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul>
        <li><a href="mailto:contact@justicia-academie.com">contact@justicia-academie.com</a></li>
        <li>Paris</li>
        <li><a href="../index.html#rendez-vous">Prendre rendez-vous</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>Justicia Académie</span>
    <span><a href="../mentions-legales.html">Mentions légales</a> · <a href="../politique-de-confidentialite.html">Politique de confidentialité</a></span>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="../script.js"></script>
</body>
</html>
"""


def main():
    data = gather()
    (FICHES / "index.html").write_text(render_index(data), encoding="utf-8")
    print(f"écrit : fiches/index.html ({sum(len(data[s]['items']) for s in SUBJECTS)} fiches indexées)")


if __name__ == "__main__":
    main()
