# -*- coding: utf-8 -*-
"""Génère les pages intérieures (formules + conseils) de Justicia Académie.

Usage : python3 _build_pages.py
Chaque page est définie dans PAGES ; le gabarit (head SEO, en-tête, pied de
page) est partagé. Pour ajouter un article : ajouter une entrée dans PAGES
et une carte dans conseils.html, puis relancer le script et mettre à jour
sitemap.xml.
"""

import json
from pathlib import Path

SITE = Path(__file__).parent
DOMAIN = "https://justicia-academie.com"

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


def header(active=""):
    def cur(name):
        return ' aria-current="page"' if name == active else ""
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Justicia Académie, accueil">
      {MARK_SVG}
      {WORDMARK}
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Navigation principale">
      <a href="etudes-de-droit.html"{cur('etudes')}>Les études de droit</a>
      <a href="index.html#formules">Les formules</a>
      <a href="conseils.html"{cur('conseils')}>Conseils</a>
      <a href="index.html#questions">Questions</a>
      <a class="nav-espace" href="espace-eleve.html">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.4"/><path d="M5.5 19c1.2-3.1 3.6-4.6 6.5-4.6s5.3 1.5 6.5 4.6"/></svg>
        <span class="nav-espace-label">Espace élève</span>
        <span class="status-dot" aria-hidden="true"></span>
      </a>
      <a class="btn" href="index.html#rendez-vous">Prendre rendez-vous</a>
    </nav>
  </div>
</header>"""


FOOTER = f"""<footer class="site-footer">
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
        <li><a href="etudes-de-droit.html">Les études de droit</a></li>
        <li><a href="index.html#formules">Les formules</a></li>
        <li><a href="conseils.html">Conseils</a></li>
        <li><a href="index.html#questions">Questions</a></li>
      </ul>
    </div>
    <div>
      <h4>Les formules</h4>
      <ul>
        <li><a href="formule-terminale-hebdomadaire.html">Terminale : formule hebdomadaire</a></li>
        <li><a href="formule-terminale-vacances.html">Terminale : formule vacances</a></li>
        <li><a href="formule-l1-stage-prerentree.html">L1 : stage de pré-rentrée</a></li>
        <li><a href="formule-l1-accompagnement-annuel.html">L1 : accompagnement annuel</a></li>
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul>
        <li><a href="mailto:contact@justicia-academie.com">contact@justicia-academie.com</a></li>
        <li>Paris</li>
        <li><a href="index.html#rendez-vous">Prendre rendez-vous</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>Justicia Académie</span>
    <span><a href="mentions-legales.html">Mentions légales</a> · <a href="politique-de-confidentialite.html">Politique de confidentialité</a></span>
  </div>
</footer>"""


def breadcrumb_jsonld(slug, name, parent=None):
    items = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{DOMAIN}/"}]
    pos = 2
    if parent:
        items.append({"@type": "ListItem", "position": pos, "name": parent[0], "item": f"{DOMAIN}/{parent[1]}"})
        pos += 1
    items.append({"@type": "ListItem", "position": pos, "name": name, "item": f"{DOMAIN}/{slug}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def course_jsonld(slug, name, description, mode):
    return {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": name,
        "description": description,
        "url": f"{DOMAIN}/{slug}",
        "inLanguage": "fr",
        "provider": {
            "@type": "EducationalOrganization",
            "name": "Justicia Académie",
            "url": f"{DOMAIN}/",
        },
        "hasCourseInstance": {
            "@type": "CourseInstance",
            "courseMode": mode,
            "location": {"@type": "Place", "name": "Justicia Académie", "address": {"@type": "PostalAddress", "addressLocality": "Paris", "addressCountry": "FR"}},
        },
    }


def article_jsonld(slug, headline, description):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "inLanguage": "fr",
        "author": {"@type": "Organization", "name": "Justicia Académie"},
        "publisher": {"@type": "Organization", "name": "Justicia Académie", "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/logo.png"}},
        "mainEntityOfPage": f"{DOMAIN}/{slug}",
        "datePublished": "2026-08-31",
        "dateModified": "2026-08-31",
    }


def render(page):
    jsonld_blocks = "\n".join(
        f'  <script type="application/ld+json">\n{json.dumps(block, ensure_ascii=False, indent=2)}\n  </script>'
        for block in page["jsonld"]
    )
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page['title']}</title>
  <meta name="description" content="{page['description']}">
  <link rel="canonical" href="{DOMAIN}/{page['slug']}">
  <meta property="og:type" content="{page.get('og_type', 'article')}">
  <meta property="og:site_name" content="Justicia Académie">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:title" content="{page['title']}">
  <meta property="og:description" content="{page['description']}">
  <meta property="og:url" content="{DOMAIN}/{page['slug']}">
  <meta property="og:image" content="{DOMAIN}/assets/logo.png">
  <meta name="twitter:card" content="summary">
{jsonld_blocks}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
</head>
<body>

{header(page.get('active', ''))}

<main>
{page['body']}
</main>

{FOOTER}

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="script.js"></script>
</body>
</html>
"""


def cta(title, text):
    return f"""
  <section class="rdv rdv-simple">
    <div class="wrap">
      <div class="reveal">
        <h2>{title}</h2>
        <p class="lede">{text}</p>
        <a class="btn btn--on-dark" href="index.html#rendez-vous">Prendre rendez-vous</a>
      </div>
    </div>
  </section>"""


def sec(numeral, heading, inner, bg=""):
    cls = f' class="{bg}"' if bg else ""
    return f"""
  <section{cls}>
    <div class="wrap">
      <div class="section-head reveal">
        <span class="numeral" aria-hidden="true">{numeral}</span>
        <div class="head-text">
          <span class="head-rule" aria-hidden="true"></span>
          <h2>{heading}</h2>
        </div>
      </div>
      <div class="prose article-body reveal">
{inner}
      </div>
    </div>
  </section>"""


def page_hero(crumb, h1, lede, meta=""):
    meta_html = f'\n      <p class="article-meta">{meta}</p>' if meta else ""
    return f"""
  <section class="page-hero">
    <div class="wrap">
      <p class="crumbs">{crumb}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>{meta_html}
    </div>
  </section>"""


CRUMB_FORMULES = '<a href="index.html">Accueil</a> · <a href="index.html#formules">Les formules</a>'
CRUMB_CONSEILS = '<a href="index.html">Accueil</a> · <a href="conseils.html">Conseils</a>'

PAGES = []

# ---------------------------------------------------------------- formules

PAGES.append({
    "slug": "formule-terminale-hebdomadaire.html",
    "title": "Prépa droit en terminale : la formule hebdomadaire — Justicia Académie",
    "description": "Une séance de préparation au droit chaque semaine pendant l'année de terminale : découverte du droit, méthode universitaire et accompagnement Parcoursup, en petit groupe à Paris.",
    "jsonld": [
        course_jsonld("formule-terminale-hebdomadaire.html", "Terminale Droit : formule hebdomadaire",
                      "Préparation hebdomadaire à l'entrée en licence de droit pendant l'année de terminale : découverte du droit, méthode universitaire, accompagnement Parcoursup.", "Onsite"),
        breadcrumb_jsonld("formule-terminale-hebdomadaire.html", "Terminale : formule hebdomadaire"),
    ],
    "body": page_hero(
        CRUMB_FORMULES,
        'La formule <span class="accent-italic">hebdomadaire</span>, pour préparer le droit toute l\'année de terminale.',
        "Un rendez-vous chaque semaine, en petit groupe, au centre à Paris : le temps de découvrir le droit en profondeur, de construire une méthode et de soigner son dossier Parcoursup sans précipitation.")
    + sec("I.", "À qui s'adresse cette formule.", """
        <p>Aux élèves de terminale qui envisagent sérieusement une licence de droit et veulent transformer cette intuition en projet solide. Aucun prérequis juridique n'est attendu : c'est précisément l'objet de l'année que de construire ce socle.</p>
        <p>C'est la formule la plus complète que nous proposons au lycée. Elle convient particulièrement aux élèves qui préfèrent un travail régulier et progressif à des sessions intensives, et à ceux qui veulent être accompagnés sur Parcoursup au moment où chaque échéance se présente, pas après coup.</p>""")
    + sec("II.", "Ce qu'on y travaille.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>La découverte du droit réel</h3>
          <p>Les grandes branches du droit, le raisonnement juridique, les institutions : un panorama construit sur l'année, avec des cas concrets tirés de l'actualité, pour savoir de quoi on parle avant de s'engager.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>La méthode universitaire</h3>
          <p>Premiers pas guidés dans la dissertation juridique et le commentaire, entraînement à la prise de notes : les exercices qui décideront des résultats de L1, abordés sans pression de notation.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>Le dossier Parcoursup</h3>
          <p>Projet motivé relu et retravaillé, choix des vœux argumenté, calendrier suivi ensemble : au moment de valider le dossier, rien n'est laissé au hasard ni écrit la veille.</p></div>
        </div>""")
    + sec("III.", "L'organisation concrète.", """
        <ul>
          <li>Une séance par semaine, tout au long de l'année scolaire, au centre à Paris.</li>
          <li>Des groupes volontairement restreints, pour que chaque élève soit connu et suivi.</li>
          <li>Des travaux écrits corrigés individuellement, avec des retours détaillés.</li>
          <li>Un point régulier avec les familles sur la progression et le projet d'orientation.</li>
        </ul>
        <p class="pull-aside">Une année pour faire d'une intuition, « le droit, peut-être », un projet construit et un dossier qui le prouve.</p>""", bg="formules")
    + cta("Parlons du projet de votre élève.",
          "Trente minutes avec l'équipe pédagogique pour vérifier que cette formule est la bonne, ou en recommander une autre en toute franchise."),
})

PAGES.append({
    "slug": "formule-terminale-vacances.html",
    "title": "Prépa droit en terminale : la formule vacances — Justicia Académie",
    "description": "Des stages intensifs de préparation au droit pendant les vacances scolaires de terminale : immersion dans la discipline, méthode et point Parcoursup, en petit groupe à Paris.",
    "jsonld": [
        course_jsonld("formule-terminale-vacances.html", "Terminale Droit : formule vacances",
                      "Stages intensifs de préparation à l'entrée en licence de droit pendant les vacances scolaires : immersion dans le droit, méthode universitaire, point Parcoursup.", "Onsite"),
        breadcrumb_jsonld("formule-terminale-vacances.html", "Terminale : formule vacances"),
    ],
    "body": page_hero(
        CRUMB_FORMULES,
        'La formule <span class="accent-italic">vacances</span>, l\'intensité sans l\'engagement hebdomadaire.',
        "Des stages d'une semaine pendant les vacances scolaires, pour se préparer sérieusement au droit quand l'emploi du temps de terminale ne laisse pas de place à un rendez-vous chaque semaine.")
    + sec("I.", "À qui s'adresse cette formule.", """
        <p>Aux élèves de terminale motivés par le droit mais dont l'année est déjà chargée : spécialités exigeantes, activités sportives ou artistiques, temps de transport. Plutôt que d'ajouter une contrainte hebdomadaire, la préparation se concentre sur des semaines dédiées, pendant les vacances.</p>
        <p>C'est aussi une excellente formule pour tester son intérêt : une première semaine d'immersion suffit souvent à savoir si la discipline plaît vraiment, avant de s'engager davantage.</p>""")
    + sec("II.", "Ce qui se passe pendant une semaine de stage.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Une immersion dans le droit</h3>
          <p>Cours interactifs, cas concrets, débats juridiques préparés et arbitrés : une semaine dense qui donne une image fidèle de ce qui attend l'étudiant en faculté.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Un socle de méthode</h3>
          <p>Chaque stage comprend un volet méthodologique : structurer une argumentation, découvrir la dissertation juridique, comprendre ce qu'un correcteur attend d'une copie de droit.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>Un point d'étape Parcoursup</h3>
          <p>À chaque session, un temps dédié au dossier : où en est le projet motivé, quels vœux formuler, quelles échéances arrivent. Les stages jalonnent l'année aux bons moments.</p></div>
        </div>""")
    + sec("III.", "L'organisation concrète.", """
        <ul>
          <li>Des stages d'une semaine, proposés à chaque période de vacances scolaires.</li>
          <li>Au centre à Paris, en petit groupe.</li>
          <li>Chaque session peut se suivre indépendamment des autres.</li>
          <li>Un compte rendu individuel est remis à la famille en fin de stage.</li>
        </ul>
        <p class="pull-aside">Un emploi du temps chargé n'a jamais empêché de préparer son entrée en droit : il demande juste une autre organisation.</p>""", bg="formules")
    + cta("Vérifions ensemble que c'est la bonne formule.",
          "Trente minutes avec l'équipe pédagogique, avec l'élève et ses parents, pour choisir la préparation adaptée à son année."),
})

PAGES.append({
    "slug": "formule-l1-stage-prerentree.html",
    "title": "Stage de pré-rentrée L1 droit à Paris — Justicia Académie",
    "description": "Une semaine intensive juste avant la rentrée en L1 de droit : matières du premier semestre, méthode de la dissertation et du commentaire, organisation du travail universitaire.",
    "jsonld": [
        course_jsonld("formule-l1-stage-prerentree.html", "L1 Droit : stage de pré-rentrée",
                      "Stage intensif d'une semaine avant la rentrée en L1 de droit : introduction aux matières fondamentales, méthode des exercices juridiques, organisation du travail.", "Onsite"),
        breadcrumb_jsonld("formule-l1-stage-prerentree.html", "L1 : stage de pré-rentrée"),
    ],
    "body": page_hero(
        CRUMB_FORMULES,
        'Le stage de <span class="accent-italic">pré-rentrée</span>, pour arriver en L1 avec un temps d\'avance.',
        "Une semaine intensive à la fin de l'été, juste avant la rentrée universitaire : quand les autres découvriront l'amphithéâtre, vous saurez déjà comment y travailler.")
    + sec("I.", "Pourquoi une pré-rentrée.", """
        <p>Les premières semaines de L1 sont décisives et déroutantes : des centaines d'étudiants en amphithéâtre, un vocabulaire nouveau, des exercices dont personne n'explique longuement les règles. Beaucoup d'étudiants passent leur premier semestre à comprendre ce qu'on attend d'eux ; les résultats s'en ressentent.</p>
        <p>Le stage de pré-rentrée déplace cet apprentissage avant le premier cours. Ce que la faculté suppose acquis en quelques semaines, nous le posons en une semaine, calmement, avant que tout commence.</p>""")
    + sec("II.", "Le programme de la semaine.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Les matières fondamentales</h3>
          <p>Introduction au droit civil et au droit constitutionnel : les notions clés du premier semestre, présentées pour comprendre les cours magistraux dès le premier jour.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>La méthode des exercices juridiques</h3>
          <p>Dissertation en deux parties, fiche et commentaire d'arrêt, cas pratique : les formats exacts des travaux dirigés et des partiels, pratiqués et corrigés pendant la semaine.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>L'organisation du travail</h3>
          <p>Prise de notes en cours magistral, préparation des séances de TD, planification des révisions : le métier d'étudiant en droit, expliqué avant de devoir l'improviser.</p></div>
        </div>""")
    + sec("III.", "L'organisation concrète.", """
        <ul>
          <li>Une semaine intensive fin août, avant la rentrée universitaire.</li>
          <li>Au centre à Paris, en petit groupe.</li>
          <li>Supports de cours et fiches de méthode remis à chaque participant.</li>
          <li>Ouvert à tous les inscrits en L1 de droit, quelle que soit la faculté.</li>
        </ul>
        <p class="pull-aside">Un semestre de tâtonnements évité en une semaine : c'est le meilleur rapport temps investi sur résultat de toute la L1.</p>""", bg="formules")
    + cta("Réservez la semaine qui change le premier semestre.",
          "Un échange de trente minutes pour présenter le stage, répondre aux questions et confirmer l'inscription."),
})

PAGES.append({
    "slug": "formule-l1-accompagnement-annuel.html",
    "title": "Accompagnement annuel en L1 de droit — Justicia Académie",
    "description": "Un suivi méthodologique tout au long de la première année de droit : séances régulières, copies corrigées, préparation des partiels et interlocuteur pédagogique disponible toute l'année.",
    "jsonld": [
        course_jsonld("formule-l1-accompagnement-annuel.html", "L1 Droit : accompagnement annuel",
                      "Accompagnement méthodologique pendant toute la première année de licence de droit : séances régulières, copies corrigées, préparation des partiels.", "Blended"),
        breadcrumb_jsonld("formule-l1-accompagnement-annuel.html", "L1 : accompagnement annuel"),
    ],
    "body": page_hero(
        CRUMB_FORMULES,
        'L\'accompagnement <span class="accent-italic">annuel</span>, pour ne jamais rester seul face à la L1.',
        "Un suivi régulier tout au long de la première année : consolider la méthode, préparer chaque session d'examens, et avoir quelqu'un à qui poser ses questions quand elles se présentent.")
    + sec("I.", "À qui s'adresse cette formule.", """
        <p>Aux étudiants de L1 qui veulent mettre toutes les chances de leur côté sur l'année entière, et à ceux qui, après quelques semaines de cours, sentent que la méthode ne suit pas malgré le travail fourni. Dans les deux cas, le principe est le même : un cadre régulier, un interlocuteur qui connaît votre progression, des exigences alignées sur celles de votre faculté.</p>
        <p>L'accompagnement se combine naturellement avec le stage de pré-rentrée, mais peut aussi commencer en cours d'année.</p>""")
    + sec("II.", "Ce que comprend l'accompagnement.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Des séances régulières de méthode</h3>
          <p>Dissertation, commentaire d'arrêt, cas pratique : chaque exercice est retravaillé sur des sujets réels, au rythme du programme du semestre.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Des copies corrigées en continu</h3>
          <p>Des entraînements écrits réguliers, corrigés avec des annotations détaillées : c'est la correction individuelle, plus que le cours, qui fait progresser une copie.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>La préparation des partiels</h3>
          <p>Avant chaque session d'examens, un programme de révision structuré et des simulations en conditions réelles, pour arriver aux épreuves préparé plutôt qu'inquiet.</p></div>
        </div>""")
    + sec("III.", "L'organisation concrète.", """
        <ul>
          <li>Un suivi sur toute l'année universitaire, de septembre aux derniers partiels.</li>
          <li>Séances au centre à Paris ; certains suivis peuvent être aménagés à distance.</li>
          <li>Un interlocuteur pédagogique joignable entre les séances.</li>
          <li>Entrée possible en cours d'année, avec une remise à niveau sur ce qui a été traité.</li>
        </ul>
        <p class="pull-aside">La L1 n'élimine pas les étudiants qui travaillent mal : elle élimine ceux qui travaillent seuls, sans retour sur ce qu'ils produisent.</p>""", bg="formules")
    + cta("Construisons votre année de L1.",
          "Trente minutes pour faire le point sur votre situation, votre faculté et vos objectifs, et définir le suivi adapté."),
})

# ---------------------------------------------------------------- conseils : index

PAGES.append({
    "slug": "conseils.html",
    "title": "Conseils pour entrer en droit : spécialités, Parcoursup, L1 — Justicia Académie",
    "description": "Nos conseils pour préparer l'entrée dans les études de droit : choix des spécialités au lycée, dossier Parcoursup, difficulté réelle de la L1 et méthode des exercices juridiques.",
    "og_type": "website",
    "active": "conseils",
    "jsonld": [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Conseils pour entrer en droit",
            "url": f"{DOMAIN}/conseils.html",
            "inLanguage": "fr",
            "isPartOf": {"@type": "WebSite", "name": "Justicia Académie", "url": f"{DOMAIN}/"},
        },
        breadcrumb_jsonld("conseils.html", "Conseils"),
    ],
    "body": page_hero(
        '<a href="index.html">Accueil</a> · Conseils',
        'Nos <span class="accent-italic">conseils</span> pour entrer en droit.',
        "Les questions que se posent les lycéens et leurs parents, traitées sérieusement : choix des spécialités, Parcoursup, réalité de la première année, méthode des exercices juridiques. Par l'équipe pédagogique de Justicia Académie.")
    + """
  <section class="conseils-section">
    <div class="wrap">
      <div class="conseils-grid">
        <article class="article-card reveal">
          <p class="a-theme">Orientation au lycée</p>
          <h2><a href="specialites-lycee-droit.html">Quelles spécialités choisir au lycée pour faire du droit ?</a></h2>
          <p>Aucune spécialité n'est obligatoire pour entrer en licence de droit. Certaines combinaisons servent pourtant mieux un dossier et préparent mieux aux études : voici lesquelles, et pourquoi.</p>
          <p class="a-meta">Première et terminale · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Parcoursup</p>
          <h2><a href="parcoursup-licence-droit.html">Parcoursup : réussir sa candidature en licence de droit</a></h2>
          <p>La licence de droit est l'une des formations les plus demandées de Parcoursup. Ce que regardent vraiment les commissions, et comment construire un dossier qui se distingue.</p>
          <p class="a-meta">Terminale · Lecture 6 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">La première année</p>
          <h2><a href="l1-droit-difficulte.html">La L1 de droit est-elle vraiment difficile ?</a></h2>
          <p>Près d'un étudiant sur deux ne passe pas en L2. Ce chiffre dit moins la difficulté du droit que l'impréparation des étudiants : ce qui échoue vraiment en L1, et comment s'en prémunir.</p>
          <p class="a-meta">Terminale et L1 · Lecture 6 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Méthode</p>
          <h2><a href="methode-commentaire-arret.html">Le commentaire d'arrêt expliqué simplement</a></h2>
          <p>L'exercice le plus déroutant de la première année, présenté pas à pas : ce qu'est un arrêt, ce qu'on attend d'un commentaire, et les erreurs qui coûtent des points aux débutants.</p>
          <p class="a-meta">L1 · Lecture 7 min</p>
        </article>
      </div>
    </div>
  </section>"""
    + cta("Une question qui n'a pas sa réponse ici ?",
          "Le premier rendez-vous sert aussi à cela : trente minutes pour poser toutes vos questions à des juristes qui connaissent le parcours."),
})

# ---------------------------------------------------------------- conseils : articles

PAGES.append({
    "slug": "specialites-lycee-droit.html",
    "title": "Quelles spécialités choisir au lycée pour faire du droit ? — Justicia Académie",
    "description": "HGGSP, SES, HLP, mathématiques : quelles spécialités choisir en première et terminale pour entrer en licence de droit ? Ce que les facultés attendent vraiment d'un dossier.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("specialites-lycee-droit.html", "Quelles spécialités choisir au lycée pour faire du droit ?",
                       "HGGSP, SES, HLP : les spécialités qui préparent le mieux à la licence de droit, et ce que les facultés attendent vraiment d'un dossier."),
        breadcrumb_jsonld("specialites-lycee-droit.html", "Quelles spécialités pour le droit ?", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Quelles spécialités choisir au lycée pour <span class="accent-italic">faire du droit</span> ?',
        "C'est la première question que posent les élèves de seconde et de première qui pensent au droit. La réponse honnête tient en deux temps : aucune spécialité n'est exigée, mais certains choix servent mieux un dossier que d'autres.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en août 2026")
    + sec("I.", "Ce que les facultés attendent vraiment.", """
        <p>Le droit ne s'enseigne pas au lycée : les facultés le savent et n'attendent aucune connaissance juridique. Les attendus nationaux de la licence de droit sur Parcoursup parlent d'autre chose : savoir argumenter, s'exprimer correctement à l'écrit comme à l'oral, s'intéresser aux questions historiques, sociétales et politiques, et être capable de fournir un travail régulier.</p>
        <p>Autrement dit, les commissions ne cherchent pas une combinaison de spécialités : elles cherchent des preuves de ces aptitudes, où qu'elles se trouvent dans le dossier. Les notes et les appréciations en français, en philosophie et en histoire pèsent souvent davantage que l'intitulé des spécialités choisies.</p>""")
    + sec("II.", "Les spécialités qui préparent le mieux.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>HGGSP, la plus proche du droit</h3>
          <p>Histoire-géographie, géopolitique et sciences politiques entraîne à l'analyse de documents, à la dissertation et à la compréhension des institutions : trois compétences directement réinvesties en faculté de droit. C'est la spécialité la plus fréquemment citée dans les dossiers admis.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>SES, pour comprendre les mécanismes</h3>
          <p>Les sciences économiques et sociales donnent les clés de lecture des débats que le droit encadre : marché du travail, protection sociale, régulation économique. Le droit des affaires, le droit social et le droit fiscal s'appuient sur ces intuitions.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>HLP, pour la rigueur de l'écrit</h3>
          <p>Humanités, littérature et philosophie forme à l'argumentation structurée et à la précision du vocabulaire, deux qualités décisives dans une copie de droit. Une excellente option pour les profils littéraires.</p></div>
        </div>
        <p>Et les mathématiques ? Elles ne sont ni requises ni pénalisantes. Un très bon dossier scientifique est un très bon dossier : la rigueur démontrée en mathématiques ou en physique se transfère sans difficulté au raisonnement juridique.</p>""")
    + sec("III.", "Le principe qui doit guider le choix.", """
        <p>Mieux vaut exceller dans des spécialités que l'on aime que s'imposer une combinaison « stratégique » subie. Un 16 en mathématiques sert davantage un dossier qu'un 11 en HGGSP choisi par calcul. Les commissions lisent les notes et les appréciations avant les intitulés.</p>
        <p class="pull-aside">La meilleure combinaison de spécialités est celle où l'élève aura les meilleures notes et les meilleures appréciations.</p>
        <p>Le choix des spécialités n'est donc pas le vrai enjeu : le vrai enjeu est de montrer, dès la première, un intérêt réel pour le droit et une capacité de travail régulière. C'est exactement ce qu'une préparation anticipée construit, et ce qu'un projet motivé pourra ensuite raconter avec des éléments concrets. Notre page sur <a href="etudes-de-droit.html">les études de droit</a> détaille la suite du parcours.</p>""")
    + cta("Un doute sur les spécialités de votre enfant ?",
          "Nous en parlons lors d'un rendez-vous de trente minutes, avec l'élève et ses parents, en fonction de son profil réel."),
})

PAGES.append({
    "slug": "parcoursup-licence-droit.html",
    "title": "Parcoursup : réussir sa candidature en licence de droit — Justicia Académie",
    "description": "Comment construire un dossier Parcoursup solide pour la licence de droit : ce que regardent les commissions, le projet motivé, les erreurs à éviter et le calendrier à respecter.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("parcoursup-licence-droit.html", "Parcoursup : réussir sa candidature en licence de droit",
                       "Ce que regardent les commissions des licences de droit sur Parcoursup, comment rédiger le projet motivé et quelles erreurs éviter."),
        breadcrumb_jsonld("parcoursup-licence-droit.html", "Parcoursup et licence de droit", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Parcoursup : réussir sa candidature en <span class="accent-italic">licence de droit</span>.',
        "La licence de droit figure chaque année parmi les formations les plus demandées de Parcoursup. Un dossier s'y distingue rarement par miracle : il se construit, en amont, avec méthode.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en août 2026")
    + sec("I.", "Ce que regardent les commissions.", """
        <p>Les licences de droit reçoivent des milliers de candidatures pour quelques centaines de places. L'examen des dossiers s'appuie d'abord sur les résultats de première et de terminale, avec une attention particulière aux matières qui mobilisent l'écrit et l'argumentation : français, philosophie, histoire, spécialités littéraires ou de sciences humaines.</p>
        <p>Viennent ensuite les appréciations des professeurs, qui pèsent plus que les élèves ne l'imaginent : « travail régulier », « excellente expression écrite », « esprit rigoureux » sont exactement les qualités que cherchent les facultés. Enfin, le projet motivé et la rubrique activités départagent les dossiers comparables.</p>""")
    + sec("II.", "Le projet motivé, pièce maîtresse.", """
        <p>La plupart des projets motivés se ressemblent : « j'ai toujours été intéressé par la justice », « je regarde des séries d'avocats », « je souhaite défendre les droits ». Les commissions en lisent des centaines. Un bon projet motivé fait l'inverse : il apporte des preuves concrètes plutôt que des déclarations d'intention.</p>
        <ul>
          <li>Citer des démarches réelles : une journée portes ouvertes en faculté, un cours suivi, une audience à laquelle on a assisté, une préparation entamée.</li>
          <li>Montrer qu'on sait ce qui attend un étudiant en droit : cours magistraux, travaux dirigés, exercices spécifiques. Comprendre la réalité de la formation est déjà un signe de maturité.</li>
          <li>Relier son parcours au projet : une spécialité, un travail personnel, un engagement qui prépare aux exigences du droit.</li>
        </ul>
        <p class="pull-aside">Un lycéen qui peut écrire « j'ai déjà rédigé une dissertation juridique » ne ressemble plus aux autres candidats.</p>""")
    + sec("III.", "Les erreurs qui coûtent cher.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Écrire le projet motivé la veille</h3>
          <p>Le texte se relit, se fait relire, se réécrit. Un projet rédigé en une soirée se reconnaît immédiatement.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Négliger la cohérence des vœux</h3>
          <p>Un dossier qui vise le droit gagne à le montrer partout : des vœux dispersés entre des formations sans lien affaiblissent le récit d'ensemble que lit la commission.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>Oublier que la terminale compte double</h3>
          <p>Les notes des deux premiers trimestres de terminale arrivent sous les yeux des commissions. Le relâchement de janvier se paie en juin.</p></div>
        </div>
        <p>Le calendrier, enfin, ne pardonne pas l'improvisation : ouverture de la plateforme en décembre, formulation des vœux jusqu'en mars, dossiers finalisés début avril. Chez Justicia Académie, l'accompagnement Parcoursup est intégré aux <a href="formule-terminale-hebdomadaire.html">formules de terminale</a>, échéance par échéance.</p>""")
    + cta("Faites relire le projet de votre enfant par des juristes.",
          "Un rendez-vous de trente minutes pour évaluer le dossier tel qu'une commission le lira, et définir ce qui peut encore le renforcer."),
})

PAGES.append({
    "slug": "l1-droit-difficulte.html",
    "title": "La L1 de droit est-elle vraiment difficile ? — Justicia Académie",
    "description": "Près d'un étudiant sur deux ne passe pas en L2. Pourquoi la première année de droit élimine autant, ce qui distingue ceux qui réussissent, et comment se préparer avant la rentrée.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("l1-droit-difficulte.html", "La L1 de droit est-elle vraiment difficile ?",
                       "Pourquoi la première année de droit élimine près d'un étudiant sur deux, ce qui distingue ceux qui réussissent, et comment se préparer avant la rentrée."),
        breadcrumb_jsonld("l1-droit-difficulte.html", "La L1 de droit est-elle difficile ?", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'La L1 de droit est-elle <span class="accent-italic">vraiment difficile</span> ?',
        "C'est la question qui inquiète les lycéens et leurs parents, et elle mérite une réponse honnête : oui, la première année élimine beaucoup. Mais pas pour les raisons qu'on imagine.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en août 2026")
    + sec("I.", "Ce que disent les chiffres, et ce qu'ils ne disent pas.", """
        <p>Selon les facultés et les années, moins d'un étudiant sur deux valide sa première année de droit du premier coup. Le chiffre impressionne, mais il faut le lire correctement : il agrège des étudiants venus en droit par défaut, des étudiants qui abandonnent dès les premières semaines, et des étudiants sérieux mais mal préparés.</p>
        <p>Pour un étudiant motivé, présent et bien préparé, la L1 n'a rien d'insurmontable : le programme est dense mais accessible, et aucune notion n'exige de talent hors du commun. Ce qui élimine, ce n'est pas la difficulté intellectuelle du droit ; c'est l'écart entre les habitudes du lycée et les exigences de l'université.</p>""")
    + sec("II.", "Ce qui échoue vraiment en première année.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>La méthode, avant les connaissances</h3>
          <p>Les partiels ne demandent pas de réciter un cours mais de produire une dissertation en deux parties, un commentaire d'arrêt, un cas pratique. Ces formats ont des règles précises que la faculté explique vite et suppose acquises. L'étudiant qui les découvre en janvier a déjà perdu son premier semestre.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>L'autonomie sans filet</h3>
          <p>Personne ne vérifie la présence en amphithéâtre, personne ne réclame les devoirs. La liberté nouvelle de l'université est une épreuve en soi : elle demande une organisation que le lycée n'a jamais enseignée.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>La solitude face aux copies</h3>
          <p>Quelques notes par semestre, des corrections collectives rapides : l'étudiant de L1 reçoit très peu de retours individuels sur ce qu'il produit. Sans regard extérieur, les mêmes erreurs se répètent d'une copie à l'autre.</p></div>
        </div>""")
    + sec("III.", "Comment mettre les chances de son côté.", """
        <p>La conclusion s'impose d'elle-même : puisque ce qui élimine est presque toujours l'impréparation, la parade est la préparation. Découvrir la méthode des exercices juridiques avant la rentrée, apprendre à prendre des notes en cours magistral, comprendre l'organisation d'une année universitaire : tout cela peut s'acquérir dès la terminale ou pendant l'été.</p>
        <p class="pull-aside">La L1 ne trie pas les plus intelligents : elle trie ceux qui savaient où ils mettaient les pieds.</p>
        <p>C'est exactement l'objet de nos préparations : les <a href="formule-terminale-hebdomadaire.html">formules de terminale</a> pour anticiper dès le lycée, le <a href="formule-l1-stage-prerentree.html">stage de pré-rentrée</a> pour poser la méthode juste avant le premier cours, et l'<a href="formule-l1-accompagnement-annuel.html">accompagnement annuel</a> pour ne jamais rester seul face à ses copies.</p>""")
    + cta("Préparez la rentrée plutôt que de la subir.",
          "Trente minutes avec l'équipe pédagogique pour évaluer la situation de l'élève et choisir la préparation adaptée."),
})

PAGES.append({
    "slug": "methode-commentaire-arret.html",
    "title": "Le commentaire d'arrêt expliqué simplement — Justicia Académie",
    "description": "Qu'est-ce qu'un commentaire d'arrêt ? La méthode pas à pas : fiche d'arrêt, problème de droit, construction du plan en deux parties et erreurs classiques des étudiants de L1.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("methode-commentaire-arret.html", "Le commentaire d'arrêt expliqué simplement",
                       "La méthode du commentaire d'arrêt pas à pas : fiche d'arrêt, problème de droit, plan en deux parties et erreurs classiques des débutants."),
        breadcrumb_jsonld("methode-commentaire-arret.html", "Le commentaire d'arrêt", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Le commentaire d\'arrêt, <span class="accent-italic">expliqué simplement</span>.',
        "C'est l'exercice le plus déroutant de la première année de droit, et l'un des plus discriminants aux examens. Voici ce qu'il est réellement, et par où le prendre quand on part de zéro.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en août 2026")
    + sec("I.", "D'abord, qu'est-ce qu'un arrêt ?", """
        <p>Un arrêt est une décision rendue par certaines juridictions, notamment les cours d'appel et la Cour de cassation. Les arrêts que l'on commente en L1 viennent le plus souvent de la Cour de cassation : quelques paragraphes denses, dans une langue codifiée, qui tranchent une question de droit précise.</p>
        <p>Avant tout commentaire, il faut donc apprendre à lire l'arrêt : identifier les faits, retracer la procédure, isoler la question posée à la cour et la réponse qu'elle y apporte. Cette lecture ordonnée porte un nom, la fiche d'arrêt, et c'est le premier réflexe à acquérir.</p>""")
    + sec("II.", "Ce qu'on attend d'un commentaire.", """
        <p>L'erreur universelle du débutant consiste à raconter l'arrêt : reformuler les faits, répéter la solution, conclure que la cour a bien jugé. Or commenter n'est pas raconter. Le correcteur attend qu'on explique la décision, qu'on la situe et qu'on l'évalue :</p>
        <ul>
          <li>Expliquer : quelle règle la cour applique-t-elle, et comment raisonne-t-elle pour passer des faits à la solution ?</li>
          <li>Situer : cette décision confirme-t-elle une jurisprudence établie, ou marque-t-elle une évolution, un revirement ?</li>
          <li>Évaluer : la solution est-elle cohérente avec les textes et les principes ? Quelles conséquences emporte-t-elle ?</li>
        </ul>
        <p class="pull-aside">Le commentaire ne demande pas ce que dit l'arrêt, mais pourquoi il le dit et ce que cela change.</p>""")
    + sec("III.", "Construire le plan en deux parties.", """
        <p>Comme la dissertation juridique, le commentaire s'organise en deux parties, chacune divisée en deux sous-parties, annoncées par des intitulés qualifiés. Le plan ne tombe pas du ciel : il découle du sens de la décision. Une démarche simple pour débuter consiste à consacrer la première partie au raisonnement de la cour (la règle mobilisée, son application aux faits) et la seconde à la portée de la décision (son apport, ses limites ou ses incertitudes).</p>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Les erreurs qui coûtent le plus de points</h3>
          <p>La paraphrase, d'abord, qui transforme le commentaire en résumé. Le hors-sujet de cours, ensuite : réciter tout ce que l'on sait du thème au lieu de commenter la décision précise. L'absence de fiche d'arrêt rigoureuse, enfin, qui fait commettre des contresens sur la solution elle-même.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Comment progresser</h3>
          <p>Le commentaire d'arrêt s'apprend en le pratiquant sur des décisions réelles, avec des corrections individuelles qui pointent les réflexes à corriger. C'est le cœur de notre <a href="formule-l1-stage-prerentree.html">stage de pré-rentrée</a> et de l'<a href="formule-l1-accompagnement-annuel.html">accompagnement annuel</a> : des copies rédigées, annotées et retravaillées jusqu'à ce que la méthode devienne naturelle.</p></div>
        </div>""")
    + cta("Apprenez la méthode avant qu'elle soit notée.",
          "Un rendez-vous de trente minutes pour comprendre où en est l'élève et construire un entraînement adapté."),
})


def main():
    for page in PAGES:
        path = SITE / page["slug"]
        path.write_text(render(page), encoding="utf-8")
        print(f"écrit : {path.name}")


if __name__ == "__main__":
    main()
