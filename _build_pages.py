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
      <a class="btn" href="index.html#abonnement">S'abonner</a>
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
      <p>Préparer les lycéens de première et de terminale à réussir leur entrée en licence de droit, et soutenir les étudiants de L1 qui en ont besoin. Centre à Paris, et à distance partout ailleurs.</p>
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
      <h4>Contact</h4>
      <ul>
        <li><a href="mailto:contact@justicia-academie.com">contact@justicia-academie.com</a></li>
        <li>Paris</li>
        <li><a href="index.html#abonnement">S'abonner</a></li>
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
        <article class="article-card reveal">
          <p class="a-theme">Méthode</p>
          <h2><a href="dissertation-juridique-methode.html">La dissertation juridique : construire un plan en deux parties</a></h2>
          <p>Le premier exercice noté d'un étudiant de L1, et le plus déroutant pour qui vient du lycée : trouver la problématique, construire un plan en deux parties, éviter les pièges classiques.</p>
          <p class="a-meta">L1 · Lecture 6 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Méthode</p>
          <h2><a href="fiche-arret-methode.html">La fiche d'arrêt, étape par étape</a></h2>
          <p>Avant de commenter un arrêt, il faut savoir le lire : faits, procédure, problème de droit, solution. Le premier réflexe méthodologique à acquérir en L1.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Méthode</p>
          <h2><a href="cas-pratique-methode-syllogisme.html">Le cas pratique en droit : la méthode du syllogisme juridique</a></h2>
          <p>Qualifier les faits, identifier la règle, l'appliquer, conclure : la logique en trois temps qui structure l'exercice le plus proche du métier de juriste.</p>
          <p class="a-meta">L1 · Lecture 6 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Méthode</p>
          <h2><a href="vocabulaire-juridique-debutant.html">Le vocabulaire juridique à connaître avant la rentrée</a></h2>
          <p>Doctrine, arrêt, pourvoi, revirement : dix mots à maîtriser pour ne pas être perdu dès la première semaine de cours.</p>
          <p class="a-meta">Terminale et L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Méthode</p>
          <h2><a href="lire-un-code-civil-efficacement.html">Comment lire un code (civil, pénal) efficacement</a></h2>
          <p>Un code civil compte plus de deux mille articles. Savoir s'y repérer fait une vraie différence dès les premiers TD.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Introduction générale au droit</p>
          <h2><a href="sources-du-droit-francais.html">Les sources du droit français expliquées simplement</a></h2>
          <p>Constitution, lois, règlements, jurisprudence, coutume : d'où vient une règle de droit, et pourquoi cette question structure toute l'introduction générale au droit.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Introduction générale au droit</p>
          <h2><a href="hierarchie-des-normes.html">Comprendre la hiérarchie des normes</a></h2>
          <p>La pyramide qui dit quel texte l'emporte sur un autre : un schéma mental indispensable, utile en dissertation comme en cas pratique.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Introduction générale au droit</p>
          <h2><a href="introduction-generale-au-droit-programme.html">Introduction générale au droit : les notions à maîtriser avant la rentrée</a></h2>
          <p>La matière fondatrice du premier semestre, qui pose le vocabulaire et les concepts que toutes les autres matières présupposeront acquis.</p>
          <p class="a-meta">L1 · Lecture 6 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Matières de L1</p>
          <h2><a href="droit-civil-droit-penal-differences.html">Droit civil, droit pénal : ce qui les distingue vraiment</a></h2>
          <p>Deux branches que l'on confond souvent avant la faculté, et qui reposent pourtant sur des logiques et des finalités radicalement différentes.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Matières de L1</p>
          <h2><a href="jurisprudence-explication.html">Qu'est-ce que la jurisprudence, et pourquoi structure-t-elle la L1 ?</a></h2>
          <p>Le mot revient dans chaque cours et chaque copie. Comprendre ce qu'elle est réellement évite bien des contresens dès les premiers mois.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Matières de L1</p>
          <h2><a href="histoire-du-droit-pourquoi-deroute.html">Histoire du droit : pourquoi cette matière déroute les étudiants de L1</a></h2>
          <p>Beaucoup de futurs étudiants ne s'y attendent pas. Pourquoi elle occupe une telle place dès le premier semestre, et comment l'aborder.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Matières de L1</p>
          <h2><a href="droit-constitutionnel-l1-bases.html">Droit constitutionnel en L1 : les bases avant le premier cours</a></h2>
          <p>Séparation des pouvoirs, Ve République, contrôle de constitutionnalité : les repères qui facilitent grandement l'entrée en matière.</p>
          <p class="a-meta">Terminale et L1 · Lecture 6 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Vie universitaire</p>
          <h2><a href="cours-magistral-suivre-efficacement.html">Le cours magistral en droit : comment le suivre efficacement</a></h2>
          <p>Un amphithéâtre bondé, aucun contrôle de présence : ce qui change vraiment, et les habitudes qui font la différence semaine après semaine.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Vie universitaire</p>
          <h2><a href="travaux-diriges-td-droit.html">Les travaux dirigés (TD) en L1 de droit : à quoi s'attendre</a></h2>
          <p>Un format qui se prépare à l'avance et pèse souvent autant que l'examen final. Ce qui compte vraiment dans la notation.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Vie universitaire</p>
          <h2><a href="heures-travail-personnel-l1-droit.html">Combien d'heures de travail personnel en L1 de droit ?</a></h2>
          <p>L'emploi du temps affiché ne dit presque rien de la charge réelle. Des repères concrets pour ne pas se faire surprendre.</p>
          <p class="a-meta">Terminale et L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Vie universitaire</p>
          <h2><a href="prise-de-notes-amphi-droit.html">Prendre des notes efficacement en amphithéâtre</a></h2>
          <p>Structurer plutôt que tout transcrire, repérer les références juridiques, relire à temps : une méthode qui change les révisions.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Orientation au lycée</p>
          <h2><a href="droit-ou-science-politique.html">Droit ou science politique : comment choisir</a></h2>
          <p>Deux formations que l'on confond souvent au lycée, et qui reposent sur des méthodes et des débouchés très différents.</p>
          <p class="a-meta">Première et terminale · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Orientation au lycée</p>
          <h2><a href="debouches-licence-droit.html">Les débouchés après une licence de droit</a></h2>
          <p>Avocat, magistrat, notaire, mais pas seulement : panorama réaliste des parcours ouverts après une licence de droit.</p>
          <p class="a-meta">Terminale · Lecture 6 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">Orientation au lycée</p>
          <h2><a href="comment-choisir-sa-faculte-de-droit.html">Comment choisir sa faculté de droit ?</a></h2>
          <p>Au-delà du classement : les critères qui comptent vraiment pour la réussite en L1, à vérifier avant de formuler ses vœux.</p>
          <p class="a-meta">Terminale · Lecture 5 min</p>
        </article>
        <article class="article-card reveal">
          <p class="a-theme">La première année</p>
          <h2><a href="erreurs-frequentes-premiere-annee-droit.html">Les erreurs les plus fréquentes en première année de droit</a></h2>
          <p>Certaines erreurs reviennent chaque année chez des étudiants pourtant sérieux. Les connaître à l'avance permet souvent de les éviter.</p>
          <p class="a-meta">L1 · Lecture 5 min</p>
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


# ---------------------------------------------------------------- conseils : nouveaux articles (méthode)

PAGES.append({
    "slug": "dissertation-juridique-methode.html",
    "title": "La dissertation juridique : construire un plan en deux parties — Justicia Académie",
    "description": "Comment construire une dissertation juridique en L1 : trouver la problématique, bâtir un plan en deux parties et deux sous-parties, éviter les erreurs qui coûtent le plus de points.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("dissertation-juridique-methode.html", "La dissertation juridique : construire un plan en deux parties",
                       "La méthode de la dissertation juridique : trouver la problématique, construire un plan en deux parties, éviter les erreurs classiques des débutants."),
        breadcrumb_jsonld("dissertation-juridique-methode.html", "La dissertation juridique", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'La dissertation juridique, ou l\'art du <span class="accent-italic">plan en deux parties</span>.',
        "C'est le premier exercice noté d'un étudiant de L1, et le plus déroutant pour qui n'a connu que la dissertation de philosophie ou d'histoire. Voici ce qui change, et comment s'y prendre.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Un exercice qui n'a rien d'une dissertation classique.", """
        <p>Contrairement à la dissertation littéraire, la dissertation juridique ne discute pas une opinion : elle expose et articule un état du droit sur une question donnée. Pas de thèse personnelle à défendre pour elle-même, mais une démonstration rigoureuse de la manière dont les règles, les principes et la jurisprudence répondent à la question posée.</p>
        <p>Premier réflexe à acquérir : ne jamais réciter un cours dans l'ordre où il a été donné. Le sujet impose son propre angle, et le plan doit répondre à ce sujet précis, pas au chapitre entier dont il est tiré.</p>""")
    + sec("II.", "Construire le plan en deux parties.", """
        <p>La forme attendue est un plan en deux parties (I et II), chacune divisée en deux sous-parties (A et B), avec des titres qui annoncent le contenu plutôt que de le résumer vaguement. Ce plan n'est pas un carcan arbitraire : il vient de la nature binaire du raisonnement juridique, qui oppose souvent un principe à ses limites, une règle à son application, un état du droit à son évolution.</p>
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Trouver la problématique</h3>
          <p>Une bonne problématique reformule le sujet en une question à laquelle le plan tout entier va répondre. Elle ne doit ni élargir le sujet, ni le réduire à une partie seulement.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Équilibrer les deux parties</h3>
          <p>Un I trois fois plus long que le II trahit un plan mal pensé. Chaque partie doit avoir un poids et un intérêt comparables aux yeux du correcteur.</p></div>
        </div>""")
    + sec("III.", "Les erreurs qui coûtent le plus de points.", """
        <ul>
          <li>Le plan « bateau » en I. Principe / II. Exception, plaqué sur n'importe quel sujet sans être justifié par son contenu réel.</li>
          <li>L'introduction bâclée, qui doit pourtant définir les termes du sujet, poser la problématique et annoncer le plan : c'est souvent elle qui donne le ton de la note.</li>
          <li>L'absence totale de jurisprudence ou de références précises, qui transforme la dissertation en propos général sans ancrage juridique.</li>
        </ul>
        <p class="pull-aside">Une dissertation juridique ne se réussit pas en révisant plus, mais en s'entraînant à construire des plans, sujet après sujet.</p>
        <p>C'est un exercice qui s'apprend par la pratique répétée et la correction individuelle, au cœur du <a href="formule-l1-stage-prerentree.html">stage de pré-rentrée</a> et de l'<a href="formule-l1-accompagnement-annuel.html">accompagnement annuel</a>.</p>""")
    + cta("Entraînez-vous avant la première dissertation notée.",
          "Un rendez-vous de trente minutes pour construire un entraînement adapté au niveau réel de l'élève."),
})

PAGES.append({
    "slug": "fiche-arret-methode.html",
    "title": "La fiche d'arrêt, étape par étape — Justicia Académie",
    "description": "Comment rédiger une fiche d'arrêt en droit : identifier les faits, la procédure, le problème de droit et la solution. La méthode complète, avec les pièges à éviter.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("fiche-arret-methode.html", "La fiche d'arrêt, étape par étape",
                       "La méthode de la fiche d'arrêt : faits, procédure, problème de droit, solution. Les étapes et les pièges classiques des étudiants de L1."),
        breadcrumb_jsonld("fiche-arret-methode.html", "La fiche d'arrêt", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'La fiche d\'arrêt, <span class="accent-italic">étape par étape</span>.',
        "Avant de commenter un arrêt, il faut savoir le lire. La fiche d'arrêt est le premier réflexe méthodologique qu'un étudiant de L1 doit acquérir, et il conditionne tous les exercices qui suivent.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Pourquoi cet exercice précède tous les autres.", """
        <p>Une fiche d'arrêt reprend, dans un ordre fixe, les éléments essentiels d'une décision de justice : les faits, la procédure suivie, la question de droit posée à la juridiction, et la solution qu'elle y apporte. C'est un exercice de lecture avant d'être un exercice de rédaction.</p>
        <p>Sa maîtrise conditionne tout le reste : on ne peut pas commenter correctement un arrêt qu'on a mal lu. La plupart des erreurs en commentaire viennent en réalité d'une fiche d'arrêt bâclée ou approximative.</p>""")
    + sec("II.", "Les quatre rubriques à maîtriser.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Les faits</h3>
          <p>Résumés dans l'ordre chronologique, en langage neutre, sans reprendre le style parfois alambiqué de l'arrêt lui-même.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>La procédure</h3>
          <p>Qui a saisi quelle juridiction, avec quel résultat, jusqu'au pourvoi éventuel : la chronologie judiciaire de l'affaire, souvent négligée à tort.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>Le problème de droit</h3>
          <p>La question juridique précise à laquelle la cour doit répondre, formulée de façon abstraite et générale, pas comme un résumé des faits de l'espèce.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">4.</span>
          <div><h3>La solution</h3>
          <p>La réponse apportée par la juridiction, avec le raisonnement qui la justifie : c'est elle qui deviendra la matière du commentaire.</p></div>
        </div>""")
    + cta("La fiche d'arrêt se travaille, elle ne s'improvise pas.",
          "Un rendez-vous de trente minutes pour évaluer le niveau de l'élève et construire un entraînement progressif."),
})

PAGES.append({
    "slug": "cas-pratique-methode-syllogisme.html",
    "title": "Le cas pratique en droit : la méthode du syllogisme juridique — Justicia Académie",
    "description": "Comment résoudre un cas pratique en droit avec la méthode du syllogisme juridique : qualifier les faits, identifier la règle applicable, l'appliquer au cas, conclure.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("cas-pratique-methode-syllogisme.html", "Le cas pratique en droit : la méthode du syllogisme juridique",
                       "La méthode du cas pratique en droit : qualification des faits, identification de la règle, application au cas, conclusion argumentée."),
        breadcrumb_jsonld("cas-pratique-methode-syllogisme.html", "Le cas pratique", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Le cas pratique, ou la logique du <span class="accent-italic">syllogisme juridique</span>.',
        "Un cas pratique raconte une situation concrète et demande une réponse juridique argumentée. C'est l'exercice le plus proche du métier de juriste, et il obéit à une logique précise qu'il suffit d'acquérir.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Le syllogisme juridique, en trois temps.", """
        <p>Le raisonnement attendu suit toujours la même structure logique : une règle générale (la majeure), des faits qualifiés juridiquement (la mineure), et une conclusion qui applique la règle aux faits. Cette structure, empruntée à la logique formelle, est la colonne vertébrale de tout raisonnement juridique.</p>
        <p>L'erreur la plus fréquente consiste à sauter directement à la conclusion, sans expliciter la règle ni la qualification des faits qui y mènent : la copie donne alors une impression de réponse « à l'instinct », sans démonstration.</p>""")
    + sec("II.", "Les étapes concrètes de la résolution.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Qualifier les faits</h3>
          <p>Traduire une situation racontée en langage courant dans les catégories du droit : un « prêt entre amis » devient un contrat de prêt, un « accident » devient potentiellement une responsabilité civile délictuelle.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Identifier la règle applicable</h3>
          <p>Retrouver le texte, le principe ou la jurisprudence qui gouverne la qualification retenue, en écartant les règles voisines mais non pertinentes.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>Appliquer et conclure</h3>
          <p>Confronter la règle aux faits de l'espèce pour en tirer une conclusion précise : qui peut agir, contre qui, sur quel fondement, avec quelles chances de succès.</p></div>
        </div>
        <p class="pull-aside">Un cas pratique bien résolu ressemble à une démonstration mathématique : chaque étape découle logiquement de la précédente.</p>""")
    + cta("Le cas pratique s'apprend en le pratiquant.",
          "Un rendez-vous de trente minutes pour évaluer où en est l'élève sur cet exercice central de la L1."),
})

# ---------------------------------------------------------------- conseils : nouveaux articles (matières de L1)

PAGES.append({
    "slug": "sources-du-droit-francais.html",
    "title": "Les sources du droit français expliquées simplement — Justicia Académie",
    "description": "Constitution, lois, règlements, jurisprudence, coutume : les sources du droit français expliquées simplement, pour aborder l'introduction générale au droit sans se perdre.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("sources-du-droit-francais.html", "Les sources du droit français expliquées simplement",
                       "Les sources du droit français — Constitution, lois, règlements, jurisprudence, coutume — expliquées simplement pour la L1."),
        breadcrumb_jsonld("sources-du-droit-francais.html", "Les sources du droit", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Les sources du droit français, <span class="accent-italic">expliquées simplement</span>.',
        "D'où vient une règle de droit ? C'est l'une des toutes premières questions de l'introduction générale au droit, et elle structure la compréhension de tout le reste de la matière.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Deux grandes familles de sources.", """
        <p>Les sources écrites, d'abord : la Constitution, les traités internationaux, les lois votées par le Parlement, les règlements pris par le pouvoir exécutif. Chacune occupe une place précise dans la hiérarchie des normes, et aucune ne peut contredire celle qui lui est supérieure.</p>
        <p>Les sources non écrites, ensuite : la jurisprudence, qui naît de l'interprétation des textes par les juges, et la coutume, pratique ancienne et constante reconnue comme obligatoire dans certains domaines. Longtemps secondaires en théorie, elles jouent en pratique un rôle considérable.</p>""")
    + sec("II.", "Ce qu'il faut vraiment retenir pour la L1.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>La loi ne suffit jamais seule</h3>
          <p>Un texte de loi s'interprète, se complète et parfois se corrige par la jurisprudence : lire uniquement le code sans la jurisprudence associée donne une vision incomplète du droit en vigueur.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Chaque source a sa place</h3>
          <p>Savoir situer une source dans la hiérarchie des normes — <a href="hierarchie-des-normes.html">détaillée dans un autre article</a> — évite l'erreur classique consistant à citer un règlement contre une loi comme s'ils avaient la même valeur.</p></div>
        </div>
        <p>C'est un vocabulaire et une architecture qui se travaillent avant la rentrée : nos <a href="formule-l1-stage-prerentree.html">stages de pré-rentrée</a> consacrent une séance entière à ces bases.</p>""")
    + cta("Posez les bases avant le premier cours d'introduction au droit.",
          "Trente minutes pour évaluer le niveau de départ de l'élève et construire un programme de pré-rentrée adapté."),
})

PAGES.append({
    "slug": "hierarchie-des-normes.html",
    "title": "Comprendre la hiérarchie des normes — Justicia Académie",
    "description": "La hiérarchie des normes expliquée simplement : Constitution, traités, lois, règlements. Un schéma mental indispensable pour aborder l'introduction générale au droit en L1.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("hierarchie-des-normes.html", "Comprendre la hiérarchie des normes",
                       "La hiérarchie des normes en droit français : Constitution, traités, lois, règlements. Un schéma mental clé pour la L1."),
        breadcrumb_jsonld("hierarchie-des-normes.html", "La hiérarchie des normes", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Comprendre la <span class="accent-italic">hiérarchie des normes</span>.',
        "C'est l'un des premiers schémas mentaux qu'un étudiant de droit doit intégrer, et il sert toute l'année : savoir quel texte l'emporte sur un autre en cas de contradiction.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "La pyramide, du sommet à la base.", """
        <p>Au sommet, la Constitution et le bloc de constitutionnalité, qui s'imposent à toutes les autres normes. Viennent ensuite les traités et le droit de l'Union européenne, puis les lois votées par le Parlement, puis les règlements pris par le gouvernement ou les autorités administratives, et enfin les actes individuels qui appliquent ces textes à des situations précises.</p>
        <p>Chaque norme doit être conforme à celle qui lui est immédiatement supérieure. C'est ce principe qui permet, par exemple, de faire annuler un règlement contraire à une loi, ou une loi contraire à la Constitution.</p>""")
    + sec("II.", "Pourquoi ce schéma évite tant d'erreurs.", """
        <p>En cas pratique comme en dissertation, situer correctement une norme dans cette hiérarchie permet d'identifier immédiatement si elle peut être valablement invoquée, ou si elle doit céder devant un texte supérieur. C'est aussi ce qui explique les mécanismes de contrôle étudiés en droit constitutionnel : contrôle de constitutionnalité des lois, contrôle de conventionnalité, contrôle de légalité des actes administratifs.</p>
        <p class="pull-aside">Une bonne copie de droit ne se contente jamais de citer un texte : elle sait toujours dire pourquoi ce texte s'impose face à un autre.</p>
        <p>Cette architecture, abstraite sur le papier, devient vite intuitive avec quelques exemples concrets travaillés en amont — c'est le cœur de nos séances de <a href="introduction-generale-au-droit-programme.html">révision d'introduction générale au droit</a>.</p>""")
    + cta("Un schéma mental qui se construit avant la rentrée.",
          "Un rendez-vous de trente minutes pour évaluer les bases de l'élève sur ces notions fondatrices."),
})

PAGES.append({
    "slug": "droit-civil-droit-penal-differences.html",
    "title": "Droit civil, droit pénal : ce qui les distingue vraiment — Justicia Académie",
    "description": "Droit civil et droit pénal : deux logiques différentes, deux objectifs différents. Les distinctions essentielles à connaître avant d'entrer en L1 de droit.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("droit-civil-droit-penal-differences.html", "Droit civil, droit pénal : ce qui les distingue vraiment",
                       "Les différences essentielles entre droit civil et droit pénal : logique, finalité, sanctions, parties au procès."),
        breadcrumb_jsonld("droit-civil-droit-penal-differences.html", "Droit civil et droit pénal", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Droit civil, droit pénal : ce qui les <span class="accent-italic">distingue vraiment</span>.',
        "Deux branches que l'on confond souvent avant la faculté, et qui reposent pourtant sur des logiques radicalement différentes. Les comprendre tôt évite bien des malentendus en première année.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Deux finalités opposées.", """
        <p>Le droit civil règle les rapports entre particuliers : contrats, responsabilité, famille, biens. Son objectif est de réparer un préjudice ou de faire respecter un engagement, souvent par des dommages et intérêts. Le procès civil oppose un demandeur à un défendeur, sur un pied d'égalité théorique.</p>
        <p>Le droit pénal, lui, sanctionne des comportements jugés inacceptables par la société tout entière : c'est l'État qui poursuit, au nom de l'intérêt général, indépendamment de la volonté de la victime. Sa finalité n'est pas la réparation mais la sanction, et parfois la prévention.</p>""")
    + sec("II.", "Des conséquences très concrètes en L1.", """
        <ul>
          <li>Le vocabulaire diffère entièrement : « responsabilité civile » et « responsabilité pénale » ne désignent pas la même chose, et un même fait peut engager les deux séparément.</li>
          <li>Les principes directeurs changent : présomption d'innocence et légalité des délits et des peines en droit pénal, liberté contractuelle et réparation intégrale en droit civil.</li>
          <li>Les enseignants et les exercices sont distincts dès le premier semestre, avec des méthodes de raisonnement qui, bien qu'apparentées, s'appliquent différemment selon la matière.</li>
        </ul>
        <p>Confondre ces deux logiques est l'une des erreurs les plus fréquentes en cas pratique de première année, et l'une des plus faciles à éviter avec un minimum de préparation.</p>""")
    + cta("Poser ces distinctions avant le premier semestre.",
          "Trente minutes pour construire un programme de pré-rentrée qui couvre les bases de chaque matière fondamentale."),
})

PAGES.append({
    "slug": "jurisprudence-explication.html",
    "title": "Qu'est-ce que la jurisprudence, et pourquoi structure-t-elle la L1 ? — Justicia Académie",
    "description": "La jurisprudence expliquée simplement : comment les décisions de justice complètent la loi, pourquoi elle occupe une telle place dans les exercices de première année de droit.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("jurisprudence-explication.html", "Qu'est-ce que la jurisprudence, et pourquoi structure-t-elle la L1 ?",
                       "La jurisprudence expliquée simplement : rôle, formation, place centrale dans les exercices de première année de droit."),
        breadcrumb_jsonld("jurisprudence-explication.html", "Comprendre la jurisprudence", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Qu\'est-ce que la jurisprudence, et pourquoi structure-t-elle <span class="accent-italic">toute la L1</span> ?',
        "Le mot revient dans chaque cours, chaque TD, chaque copie. Comprendre ce qu'est réellement la jurisprudence évite bien des contresens dans les premiers mois de faculté.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Une source de droit qui naît des tribunaux.", """
        <p>La jurisprudence désigne l'ensemble des décisions rendues par les juridictions, et surtout la manière dont elles interprètent et précisent les textes de loi. Une loi rédigée en termes généraux laisse toujours une marge d'interprétation : c'est la jurisprudence qui, affaire après affaire, en fixe le sens concret.</p>
        <p>Elle peut confirmer une interprétation constante, l'affiner progressivement, ou opérer un revirement complet lorsque la Cour de cassation ou le Conseil d'État change de position. Suivre ces évolutions fait partie du travail ordinaire d'un juriste, et donc d'un étudiant en droit.</p>""")
    + sec("II.", "Pourquoi elle occupe une telle place dans les exercices.", """
        <p>Le commentaire d'arrêt, le cas pratique, la dissertation : les trois grands exercices de la L1 demandent tous de manier la jurisprudence, soit pour la commenter directement, soit pour l'invoquer à l'appui d'un raisonnement. Un étudiant qui se contente du texte de loi, sans connaître la jurisprudence qui l'accompagne, répond toujours à côté.</p>
        <p class="pull-aside">Le code donne la règle ; la jurisprudence dit comment elle s'applique réellement.</p>
        <p>Notre article sur <a href="methode-commentaire-arret.html">la méthode du commentaire d'arrêt</a> détaille comment exploiter concrètement une décision de justice.</p>""")
    + cta("Apprendre à lire et à citer la jurisprudence avant la rentrée.",
          "Un rendez-vous de trente minutes pour évaluer les acquis de l'élève sur cette notion centrale."),
})

PAGES.append({
    "slug": "introduction-generale-au-droit-programme.html",
    "title": "Introduction générale au droit : les notions à maîtriser avant la rentrée — Justicia Académie",
    "description": "Le programme d'introduction générale au droit en L1 : les notions incontournables du premier semestre, et comment les aborder avant la rentrée sans se sentir dépassé.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("introduction-generale-au-droit-programme.html", "Introduction générale au droit : les notions à maîtriser avant la rentrée",
                       "Les notions incontournables du programme d'introduction générale au droit en L1, et comment les aborder avant la rentrée."),
        breadcrumb_jsonld("introduction-generale-au-droit-programme.html", "Introduction générale au droit", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Introduction générale au droit : les notions à <span class="accent-italic">maîtriser avant la rentrée</span>.',
        "C'est la matière fondatrice du premier semestre : elle pose le vocabulaire et les concepts que toutes les autres matières présupposeront acquis. La découvrir en septembre plutôt qu'avant, c'est prendre du retard dès la première semaine.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Ce que recouvre vraiment cette matière.", """
        <p>Contrairement à ce que son nom suggère, l'introduction générale au droit n'est pas un survol superficiel : c'est une matière dense qui pose les fondations conceptuelles de toutes les études de droit. Elle traite de la règle de droit elle-même, de ses sources, de son organisation, et des grandes notions qui structurent tout raisonnement juridique.</p>""")
    + sec("II.", "Les notions à connaître avant le premier cours.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>La règle de droit et ses caractères</h3>
          <p>Générale, impersonnelle, obligatoire, sanctionnée par l'État : ce qui distingue une règle de droit d'une règle morale ou d'une norme sociale.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Les sources du droit</h3>
          <p>Loi, jurisprudence, coutume : voir notre article dédié sur <a href="sources-du-droit-francais.html">les sources du droit français</a>.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>Les personnes et les biens</h3>
          <p>Personnes physiques et morales, patrimoine, classification des biens : le socle conceptuel qui sera repris toute l'année en droit civil.</p></div>
        </div>
        <p>C'est précisément le contenu que couvrent nos fiches de méthodologie et d'introduction générale au droit, accessibles aux élèves inscrits dans l'<a href="espace-eleve.html">espace élève</a>.</p>""")
    + cta("Abordez cette matière fondatrice avec de l'avance.",
          "Un rendez-vous de trente minutes pour construire un programme de révision adapté avant la rentrée."),
})

PAGES.append({
    "slug": "histoire-du-droit-pourquoi-deroute.html",
    "title": "Histoire du droit : pourquoi cette matière déroute les étudiants de L1 — Justicia Académie",
    "description": "L'histoire du droit surprend souvent les étudiants de première année, qui ne l'attendaient pas dans un cursus juridique. Pourquoi cette matière compte, et comment l'aborder.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("histoire-du-droit-pourquoi-deroute.html", "Histoire du droit : pourquoi cette matière déroute les étudiants de L1",
                       "Pourquoi l'histoire du droit surprend les étudiants de première année, ce qu'elle recouvre réellement et comment l'aborder efficacement."),
        breadcrumb_jsonld("histoire-du-droit-pourquoi-deroute.html", "Histoire du droit", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Histoire du droit : pourquoi cette matière <span class="accent-italic">déroute tant d\'étudiants</span>.',
        "Beaucoup de futurs étudiants ne s'attendent pas à faire de l'histoire en licence de droit. Elle occupe pourtant une place importante dès le premier semestre, pour des raisons précises.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Une matière mal anticipée.", """
        <p>Beaucoup d'élèves de terminale imaginent la L1 de droit comme un enchaînement de matières exclusivement juridiques. La découverte de l'histoire du droit, souvent dès le premier semestre, surprend et parfois déstabilise : elle demande une rigueur de mémorisation de dates et de régimes, différente du raisonnement attendu en droit civil ou constitutionnel.</p>
        <p>Cette matière retrace la formation du droit français à travers les grandes périodes : droit romain, droit coutumier, Ancien Régime, Révolution, codification napoléonienne. Elle n'est pas un hors-sujet : c'est la clé pour comprendre pourquoi le droit actuel est construit comme il l'est.</p>""")
    + sec("II.", "Pourquoi elle compte réellement.", """
        <p>Beaucoup de notions de droit civil actuel ne s'expliquent qu'à la lumière de leur histoire : la propriété, le contrat, la famille portent la trace de siècles d'évolutions juridiques. Comprendre cette généalogie aide à mémoriser les règles contemporaines en leur donnant du sens, plutôt que de les apprendre comme une liste arbitraire.</p>
        <p class="pull-aside">On comprend mieux une règle quand on sait pourquoi elle a fini par exister.</p>
        <p>C'est une matière qui se prépare bien en amont : nos fiches d'histoire du droit, disponibles dans l'<a href="espace-eleve.html">espace élève</a>, couvrent les grandes périodes attendues au premier semestre.</p>""")
    + cta("Une matière surprenante, mais loin d'être insurmontable.",
          "Trente minutes pour comprendre comment aborder cette matière avec méthode dès la pré-rentrée."),
})

PAGES.append({
    "slug": "droit-constitutionnel-l1-bases.html",
    "title": "Droit constitutionnel en L1 : les bases avant le premier cours — Justicia Académie",
    "description": "Séparation des pouvoirs, régime de la Ve République, contrôle de constitutionnalité : les bases de droit constitutionnel à connaître avant le premier cours de L1.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("droit-constitutionnel-l1-bases.html", "Droit constitutionnel en L1 : les bases avant le premier cours",
                       "Les bases de droit constitutionnel à connaître avant le premier cours de L1 : séparation des pouvoirs, Ve République, contrôle de constitutionnalité."),
        breadcrumb_jsonld("droit-constitutionnel-l1-bases.html", "Droit constitutionnel en L1", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Droit constitutionnel en L1 : les bases avant le <span class="accent-italic">premier cours</span>.',
        "C'est souvent la matière la plus attendue par les futurs étudiants, celle qui donne à voir concrètement les institutions dont parlent les journaux. Quelques repères avant la rentrée en facilitent grandement l'entrée en matière.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Les notions qui reviennent sans cesse.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>La séparation des pouvoirs</h3>
          <p>Législatif, exécutif, judiciaire : le principe hérité de Montesquieu qui structure encore aujourd'hui l'organisation de l'État, et que l'on retrouve appliqué, nuancé ou contourné dans chaque régime étudié.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>La Ve République</h3>
          <p>Née en 1958, elle organise des rapports particuliers entre un président fort, un gouvernement responsable devant le Parlement et une Assemblée nationale qui peut le renverser : un équilibre singulier à bien comprendre dès les premières semaines.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>Le contrôle de constitutionnalité</h3>
          <p>Le mécanisme par lequel le Conseil constitutionnel vérifie qu'une loi respecte la Constitution, y compris après son entrée en vigueur, via la question prioritaire de constitutionnalité.</p></div>
        </div>""")
    + sec("II.", "Une matière qui récompense la préparation.", """
        <p>Le droit constitutionnel s'appuie sur une actualité institutionnelle suivie tout au long de l'année : motions de censure, nominations, décisions du Conseil constitutionnel. Un étudiant qui arrive avec quelques repères sur les institutions de la Ve République gagne un temps précieux sur ses camarades qui les découvrent en même temps que le cours.</p>
        <p>Nos capsules vidéo, comme celle sur <a href="index.html#videos">la motion de censure</a>, et nos fiches de droit constitutionnel couvrent précisément ces bases avant la rentrée.</p>""")
    + cta("Arriver au premier cours de droit constitutionnel déjà à l'aise.",
          "Un rendez-vous de trente minutes pour construire un programme de pré-rentrée sur cette matière."),
})

# ---------------------------------------------------------------- conseils : nouveaux articles (vie universitaire)

PAGES.append({
    "slug": "cours-magistral-suivre-efficacement.html",
    "title": "Le cours magistral en droit : comment le suivre efficacement — Justicia Académie",
    "description": "Amphithéâtre bondé, débit soutenu, aucune vérification de présence : comment suivre efficacement un cours magistral de droit dès les premières semaines de L1.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("cours-magistral-suivre-efficacement.html", "Le cours magistral en droit : comment le suivre efficacement",
                       "Comment suivre efficacement un cours magistral de droit en L1 : prise de notes, organisation, autonomie."),
        breadcrumb_jsonld("cours-magistral-suivre-efficacement.html", "Suivre un cours magistral", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Le cours magistral en droit : comment le suivre <span class="accent-italic">efficacement</span>.',
        "Un amphithéâtre de plusieurs centaines d'étudiants, un enseignant qui parle sans s'interrompre pendant deux heures, aucun contrôle de présence : le cours magistral est une rupture nette avec le lycée.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Une rupture avec les habitudes du lycée.", """
        <p>Au lycée, un professeur s'adresse à trente élèves, vérifie la compréhension, ralentit si besoin. En amphithéâtre, l'enseignant délivre un cours dense à un auditoire nombreux, sans interaction directe : personne ne vérifiera si l'étudiant a compris, ni même s'il est présent.</p>
        <p>Cette autonomie nouvelle est déstabilisante pour beaucoup d'étudiants de première année, qui découvrent en même temps qu'il faut désormais organiser soi-même sa présence, sa concentration et son travail de reprise.</p>""")
    + sec("II.", "Ce qui fait la différence, semaine après semaine.", """
        <ul>
          <li>Prendre des notes structurées plutôt que de tout transcrire : voir notre article sur <a href="prise-de-notes-amphi-droit.html">la prise de notes en amphithéâtre</a>.</li>
          <li>Relire et compléter ses notes dans les 48 heures, tant que le cours est encore frais, plutôt qu'à l'approche des examens.</li>
          <li>Repérer activement les articles de loi et les arrêts cités, pour pouvoir y revenir facilement au moment de réviser ou de traiter un exercice.</li>
        </ul>
        <p class="pull-aside">Personne ne vérifie la présence en amphithéâtre ; c'est justement pour cela qu'elle fait la différence sur l'année.</p>""")
    + cta("Apprendre à s'organiser avant le premier amphi.",
          "Un rendez-vous de trente minutes pour aborder ces méthodes de travail avant la rentrée universitaire."),
})

PAGES.append({
    "slug": "travaux-diriges-td-droit.html",
    "title": "Les travaux dirigés (TD) en L1 de droit : à quoi s'attendre — Justicia Académie",
    "description": "Préparation exigée, participation orale, exercices notés : à quoi ressemblent vraiment les travaux dirigés de L1 en droit, et comment s'y présenter chaque semaine.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("travaux-diriges-td-droit.html", "Les travaux dirigés (TD) en L1 de droit : à quoi s'attendre",
                       "À quoi ressemblent les travaux dirigés de L1 en droit : préparation exigée, participation orale, exercices notés."),
        breadcrumb_jsonld("travaux-diriges-td-droit.html", "Les travaux dirigés en L1", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Les travaux dirigés en L1 de droit : <span class="accent-italic">à quoi s\'attendre</span>.',
        "Contrairement au cours magistral, le TD se prépare à l'avance et se joue en petit groupe. C'est souvent lui qui fait la moyenne du semestre, et pourtant il reste mal anticipé par les nouveaux étudiants.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Un format qui demande d'arriver déjà prêt.", """
        <p>Le travail dirigé regroupe un nombre réduit d'étudiants autour d'un chargé de TD, sur des exercices à préparer avant la séance : fiche d'arrêt, cas pratique, dissertation, à rendre ou à présenter à l'oral. Contrairement au cours magistral, la présence y est généralement obligatoire, et la préparation est vérifiée directement.</p>
        <p>Arriver sans avoir préparé la fiche de travaux dirigés se voit immédiatement : les questions posées supposent une lecture préalable des documents et une première tentative de résolution des exercices.</p>""")
    + sec("II.", "Ce qui compte dans la notation.", """
        <p>La participation orale, la qualité des exercices préparés et parfois un ou plusieurs galops d'essai en cours de semestre composent la note de contrôle continu, qui pèse souvent autant que l'examen final. Un semestre de TD sérieusement suivi peut ainsi compenser un examen plus difficile.</p>
        <p>C'est aussi en TD que se construit, semaine après semaine, la maîtrise réelle des exercices juridiques : le cours magistral donne la matière, le TD apprend à la mobiliser.</p>""")
    + cta("Se présenter en TD déjà à l'aise avec les exercices attendus.",
          "Un rendez-vous de trente minutes pour construire un entraînement qui anticipe ce format exigeant."),
})

PAGES.append({
    "slug": "heures-travail-personnel-l1-droit.html",
    "title": "Combien d'heures de travail personnel en L1 de droit ? — Justicia Académie",
    "description": "Combien d'heures de travail personnel une L1 de droit demande-t-elle réellement, en dehors des cours et des TD ? Des repères concrets pour anticiper la charge de travail.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("heures-travail-personnel-l1-droit.html", "Combien d'heures de travail personnel en L1 de droit ?",
                       "Des repères concrets sur la charge de travail personnel réellement demandée en première année de licence de droit."),
        breadcrumb_jsonld("heures-travail-personnel-l1-droit.html", "Charge de travail en L1", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Combien d\'heures de travail personnel en <span class="accent-italic">L1 de droit</span> ?',
        "C'est une question que se posent presque tous les futurs étudiants, et la réponse honnête surprend souvent : le nombre d'heures de cours affiché à l'emploi du temps ne dit presque rien de la charge réelle.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Ce que l'emploi du temps ne montre pas.", """
        <p>Une semaine de L1 de droit compte généralement entre quinze et vingt heures de cours et de TD. À première vue, cela ressemble à un emploi du temps de lycée allégé. C'est une illusion : le travail personnel attendu en dehors des cours dépasse très largement ce volume, et c'est précisément ce que le lycée n'a pas appris à mesurer.</p>
        <p>Préparer un TD, relire et compléter ses notes de cours magistral, lire les arrêts et les textes indiqués, réviser en continu plutôt qu'à l'approche des examens : additionnées, ces tâches représentent souvent autant d'heures que les cours eux-mêmes, parfois davantage à l'approche des examens.</p>""")
    + sec("II.", "Pourquoi ce décalage surprend tant.", """
        <p>Au lycée, le travail personnel est en grande partie balisé par les professeurs : devoirs précis, dates de contrôle annoncées, relances régulières. En L1, cette structure disparaît : personne ne réclame la préparation d'un TD, mais son absence se voit et se paie dès la première séance.</p>
        <p class="pull-aside">Ce n'est pas la difficulté des exercices qui surprend le plus les nouveaux étudiants, c'est le temps qu'il faut leur consacrer chaque semaine pour rester à niveau.</p>
        <p>Cette organisation du travail personnel, sans filet ni rappel extérieur, est justement ce que nos préparations travaillent en amont, avant que la première semaine de cours ne l'impose brutalement.</p>""")
    + cta("Anticiper la charge de travail réelle de la L1.",
          "Trente minutes pour évaluer les habitudes de travail de l'élève et l'aider à construire une organisation tenable."),
})

PAGES.append({
    "slug": "prise-de-notes-amphi-droit.html",
    "title": "Prendre des notes efficacement en amphithéâtre — Justicia Académie",
    "description": "Comment prendre des notes efficacement pendant un cours magistral de droit : structurer plutôt que transcrire, repérer les articles et la jurisprudence, relire à temps.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("prise-de-notes-amphi-droit.html", "Prendre des notes efficacement en amphithéâtre",
                       "Méthode de prise de notes en amphithéâtre de droit : structurer, repérer les références juridiques, relire à temps."),
        breadcrumb_jsonld("prise-de-notes-amphi-droit.html", "Prendre des notes en amphi", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Prendre des notes efficacement en <span class="accent-italic">amphithéâtre</span>.',
        "Deux heures de cours à débit soutenu, sans pause ni pédagogie de répétition : la prise de notes en amphithéâtre de droit s'apprend, et elle change tout pour les révisions qui suivent.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "L'erreur la plus répandue : tout transcrire.", """
        <p>Face au débit d'un cours magistral, le réflexe naturel consiste à essayer de tout noter, mot pour mot. C'est une stratégie perdante : elle épuise l'attention, empêche de suivre le raisonnement d'ensemble, et produit des notes illisibles une fois relues à froid.</p>
        <p>Le bon réflexe est inverse : identifier la structure du cours au fur et à mesure — les titres, les articulations, les définitions clés — et noter en priorité ce qui structure le raisonnement, pas chaque phrase prononcée.</p>""")
    + sec("II.", "Trois habitudes qui changent tout.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Repérer systématiquement les références</h3>
          <p>Articles de loi, arrêts cités, dates clés : les encadrer ou les surligner à la volée pour pouvoir les retrouver instantanément au moment de réviser ou de traiter un exercice.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Laisser de la place pour compléter</h3>
          <p>Des marges larges et des sauts de ligne permettent d'ajouter, dans les jours qui suivent, ce qui n'a pas pu être noté en direct.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>Relire dans les 48 heures</h3>
          <p>Reprendre ses notes rapidement après le cours, tant que le raisonnement de l'enseignant est encore en mémoire, pour combler les trous et clarifier les abréviations prises à la hâte.</p></div>
        </div>""")
    + cta("S'entraîner à la prise de notes avant la rentrée.",
          "Un rendez-vous de trente minutes pour travailler cette méthode en conditions proches du réel."),
})

# ---------------------------------------------------------------- conseils : nouveaux articles (orientation et débouchés)

PAGES.append({
    "slug": "droit-ou-science-politique.html",
    "title": "Droit ou science politique : comment choisir — Justicia Académie",
    "description": "Licence de droit ou licence de science politique : deux formations souvent confondues par les lycéens. Les différences de contenu, de méthode et de débouchés.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("droit-ou-science-politique.html", "Droit ou science politique : comment choisir",
                       "Les différences entre licence de droit et licence de science politique : contenu, méthode, débouchés."),
        breadcrumb_jsonld("droit-ou-science-politique.html", "Droit ou science politique", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Droit ou science politique : <span class="accent-italic">comment choisir</span> ?',
        "Deux formations que l'on confond souvent au lycée, tant leurs objets se croisent, et qui pourtant reposent sur des méthodes et des débouchés très différents.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Deux disciplines, deux méthodes.", """
        <p>Le droit étudie les règles elles-mêmes : leur contenu, leur interprétation, leur application à des situations concrètes. Le raisonnement y est déductif et technique, structuré par les exercices que sont la dissertation, le commentaire d'arrêt et le cas pratique.</p>
        <p>La science politique étudie le pouvoir, les institutions et les phénomènes politiques dans une perspective plus large, empruntant à la sociologie, à l'histoire et à l'économie. Les exercices y sont proches de ceux de sciences humaines : dissertations d'analyse, études de cas, moins centrées sur la technique juridique.</p>""")
    + sec("II.", "Un critère de choix simple.", """
        <p>Un élève attiré par le fonctionnement concret des institutions, l'actualité politique et les grands débats de société trouvera davantage sa place en science politique. Un élève intéressé par la résolution de situations concrètes selon des règles précises, par la rigueur du raisonnement juridique, se sentira mieux en licence de droit.</p>
        <p class="pull-aside">Les deux parcours se recoupent souvent en première année dans certaines universités : la première session permet parfois d'affiner ce choix sans le figer trop tôt.</p>
        <p>En cas de doute persistant, un échange avec des juristes qui connaissent les deux parcours reste le moyen le plus rapide d'y voir clair.</p>""")
    + cta("Un doute entre droit et science politique ?",
          "Trente minutes pour en discuter avec l'équipe pédagogique, en fonction du profil réel de l'élève."),
})

PAGES.append({
    "slug": "debouches-licence-droit.html",
    "title": "Les débouchés après une licence de droit — Justicia Académie",
    "description": "Avocat, magistrat, notaire, mais pas seulement : panorama réaliste des débouchés après une licence de droit, et des parcours qui y mènent après la L3.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("debouches-licence-droit.html", "Les débouchés après une licence de droit",
                       "Panorama des débouchés après une licence de droit : professions juridiques classiques et parcours moins connus."),
        breadcrumb_jsonld("debouches-licence-droit.html", "Les débouchés du droit", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Les débouchés après une <span class="accent-italic">licence de droit</span>.',
        "Avocat, magistrat, notaire : ce sont les métiers auxquels on pense en premier. Ils ne représentent pourtant qu'une partie des parcours réellement ouverts après une licence de droit.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Les voies les plus connues.", """
        <p>Avocat, magistrat et notaire restent les débouchés les plus identifiés, mais aucun n'est accessible directement après la licence : chacun suppose un master, puis un concours ou un examen d'entrée spécifique — CRFPA pour l'avocature, concours de l'École nationale de la magistrature, examen d'accès au CFPN pour le notariat.</p>
        <p>Ces parcours exigeants se préparent dès la licence : choix des options, stages, qualité du dossier académique pèsent déjà sur les admissions ultérieures.</p>""")
    + sec("II.", "Des parcours moins connus, tout aussi réels.", """
        <ul>
          <li>Juriste d'entreprise, dans des directions juridiques de toutes tailles d'entreprises, un débouché majoritaire en nombre de diplômés.</li>
          <li>Métiers de l'administration publique, accessibles par concours, où une formation juridique est un atout constant.</li>
          <li>Ressources humaines, compliance, gestion des risques : des fonctions qui recrutent largement des profils juridiques sans être des « métiers du droit » au sens strict.</li>
          <li>Poursuite vers des doubles cursus ou des écoles spécialisées après la licence, pour des profils qui affinent leur projet en cours de route.</li>
        </ul>
        <p>La licence de droit n'enferme donc pas dans un seul métier : elle ouvre un socle de compétences — rigueur, argumentation, culture des règles — recherché bien au-delà des professions juridiques classiques.</p>""")
    + cta("Construire un projet d'orientation réaliste, pas seulement rêvé.",
          "Un rendez-vous de trente minutes pour explorer les débouchés compatibles avec le profil de l'élève."),
})

PAGES.append({
    "slug": "comment-choisir-sa-faculte-de-droit.html",
    "title": "Comment choisir sa faculté de droit ? — Justicia Académie",
    "description": "Réputation, taille des promotions, spécialisations, proximité : les critères qui comptent vraiment pour choisir sa faculté de droit sur Parcoursup, au-delà du classement.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("comment-choisir-sa-faculte-de-droit.html", "Comment choisir sa faculté de droit ?",
                       "Les critères qui comptent vraiment pour choisir sa faculté de droit : taille des promotions, spécialisations, encadrement, proximité."),
        breadcrumb_jsonld("comment-choisir-sa-faculte-de-droit.html", "Choisir sa faculté de droit", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Comment choisir sa <span class="accent-italic">faculté de droit</span> ?',
        "Face à la multiplication des vœux possibles sur Parcoursup, la tentation est grande de se fier uniquement à la réputation. D'autres critères, moins visibles, pèsent pourtant davantage sur la réussite en L1.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Au-delà de la réputation.", """
        <p>La réputation d'une faculté joue un rôle réel, notamment pour certains concours ou recrutements ultérieurs. Elle ne dit cependant presque rien de l'expérience concrète d'un étudiant de L1 : taille des amphithéâtres, effectifs des groupes de TD, qualité de l'encadrement varient fortement d'un établissement à l'autre, indépendamment du classement.</p>
        <p>Un étudiant qui a besoin d'un cadre pour progresser gagnera parfois davantage dans une faculté moins prestigieuse mais mieux structurée, que dans un établissement réputé où il se retrouve anonyme parmi des centaines d'autres.</p>""")
    + sec("II.", "Les critères à vérifier concrètement.", """
        <ul>
          <li>La taille des promotions de L1 et des groupes de TD, qui conditionne directement le suivi individuel possible.</li>
          <li>Les doubles licences et parcours renforcés proposés, pour les élèves qui envisagent déjà une spécialisation ou une poursuite exigeante.</li>
          <li>La proximité géographique et le mode de vie qu'elle implique, un facteur souvent sous-estimé alors qu'il pèse sur la capacité à tenir un rythme de travail exigeant.</li>
          <li>Les statistiques de réussite en L1 et de passage en L2, quand l'université les publie, plus parlantes qu'un classement général.</li>
        </ul>
        <p class="pull-aside">La meilleure faculté n'est pas la plus prestigieuse : c'est celle où l'élève aura les meilleures conditions pour réussir sa première année.</p>""")
    + cta("Faire les bons vœux, avec les bons critères.",
          "Trente minutes pour passer en revue les options réalistes du dossier avec l'équipe pédagogique."),
})

# ---------------------------------------------------------------- conseils : nouveaux articles (première année, vocabulaire)

PAGES.append({
    "slug": "vocabulaire-juridique-debutant.html",
    "title": "Le vocabulaire juridique à connaître avant la rentrée — Justicia Académie",
    "description": "Doctrine, arrêt, pourvoi, revirement, qualification : le vocabulaire juridique de base à maîtriser avant la rentrée en L1, pour ne pas être perdu dès la première semaine.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("vocabulaire-juridique-debutant.html", "Le vocabulaire juridique à connaître avant la rentrée",
                       "Le vocabulaire juridique de base à connaître avant la rentrée en L1 : doctrine, arrêt, pourvoi, revirement, qualification."),
        breadcrumb_jsonld("vocabulaire-juridique-debutant.html", "Le vocabulaire juridique de base", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Le vocabulaire juridique à connaître <span class="accent-italic">avant la rentrée</span>.',
        "Un cours de droit utilise dès la première semaine un vocabulaire précis, jamais expliqué en détail car supposé acquis. En connaître les bases avant la rentrée change immédiatement la façon de suivre les cours.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Dix mots à maîtriser avant le premier cours.", """
        <ul>
          <li><strong>Doctrine</strong> : l'ensemble des analyses et commentaires produits par les universitaires et juristes sur le droit en vigueur.</li>
          <li><strong>Arrêt</strong> : une décision rendue par une cour d'appel ou une haute juridiction, comme la Cour de cassation ou le Conseil d'État.</li>
          <li><strong>Jugement</strong> : une décision rendue en première instance, par un tribunal.</li>
          <li><strong>Pourvoi</strong> : le recours formé devant la Cour de cassation contre un arrêt rendu en appel.</li>
          <li><strong>Revirement de jurisprudence</strong> : un changement d'interprétation opéré par une juridiction sur une question qu'elle tranchait jusque-là dans un autre sens.</li>
          <li><strong>Qualification juridique</strong> : l'opération consistant à faire entrer une situation de fait dans une catégorie du droit.</li>
          <li><strong>Moyen</strong> : un argument juridique invoqué à l'appui d'une prétention devant une juridiction.</li>
          <li><strong>Espèce</strong> : l'affaire précise jugée, par opposition à la règle générale qu'elle applique.</li>
          <li><strong>Visa</strong> : le ou les textes que la Cour de cassation cite en tête de son arrêt pour fonder sa décision.</li>
          <li><strong>Attendu</strong> : les paragraphes de motivation d'un arrêt, qui exposent le raisonnement suivi.</li>
        </ul>""")
    + sec("II.", "Pourquoi ce socle change tout.", """
        <p>Sans ces repères, chaque phrase d'un cours magistral demande un effort de décodage supplémentaire, en plus de la compréhension du fond. Avec eux, l'attention se porte directement sur le raisonnement juridique, là où elle doit être dès la première semaine.</p>
        <p class="pull-aside">Le vocabulaire juridique n'est pas un détail technique : c'est la grammaire sans laquelle le raisonnement reste inaccessible.</p>""")
    + cta("Arriver à la rentrée avec ce socle déjà acquis.",
          "Un rendez-vous de trente minutes pour évaluer le niveau de départ et construire un programme de pré-rentrée."),
})

PAGES.append({
    "slug": "lire-un-code-civil-efficacement.html",
    "title": "Comment lire un code (civil, pénal) efficacement — Justicia Académie",
    "description": "Numérotation des articles, table des matières, annotations de jurisprudence : comment se repérer et lire efficacement un code civil ou pénal dès la première année.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("lire-un-code-civil-efficacement.html", "Comment lire un code (civil, pénal) efficacement",
                       "Comment se repérer et lire efficacement un code civil ou pénal en L1 : numérotation, plan, jurisprudence annotée."),
        breadcrumb_jsonld("lire-un-code-civil-efficacement.html", "Lire un code efficacement", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Comment lire un code efficacement, <span class="accent-italic">sans se perdre</span>.',
        "Un code civil compte plus de deux mille articles. Savoir s'y repérer, et pas seulement le posséder, fait une vraie différence dès les premiers travaux dirigés.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Se repérer dans la structure avant de chercher un article.", """
        <p>Un code est organisé en livres, titres, chapitres et sections, annoncés dans une table des matières détaillée en début d'ouvrage. Avant de chercher un article précis, il faut d'abord identifier dans quelle partie du code la question posée se situe : cette étape, souvent négligée, fait gagner un temps considérable en TD comme en examen.</p>
        <p>La numérotation elle-même donne des indices : des articles consécutifs traitent généralement d'un même sous-thème, ce qui permet, en lisant les articles voisins d'une disposition, de mieux comprendre son sens et sa portée.</p>""")
    + sec("II.", "Exploiter les annotations de jurisprudence.", """
        <p>Les codes utilisés à l'université sont annotés : sous chaque article figurent des résumés de décisions de justice qui l'ont appliqué ou interprété. C'est une ressource précieuse, à condition de savoir la lire : elle permet de vérifier rapidement comment un texte est réellement appliqué, au-delà de sa lettre.</p>
        <p class="pull-aside">Un code annoté bien maîtrisé vaut, en examen, presque autant qu'un cours appris par cœur.</p>
        <p>C'est un outil que nos élèves apprennent à manier dès le <a href="formule-l1-stage-prerentree.html">stage de pré-rentrée</a>, code en main, sur des exercices concrets.</p>""")
    + cta("Manier le code avant d'en avoir besoin en examen.",
          "Un rendez-vous de trente minutes pour évaluer les habitudes de travail de l'élève sur les textes juridiques."),
})

PAGES.append({
    "slug": "erreurs-frequentes-premiere-annee-droit.html",
    "title": "Les erreurs les plus fréquentes en première année de droit — Justicia Académie",
    "description": "Retard pris en octobre, révisions repoussées, méthode négligée : les erreurs les plus fréquentes des étudiants de première année de droit, et comment les éviter.",
    "active": "conseils",
    "jsonld": [
        article_jsonld("erreurs-frequentes-premiere-annee-droit.html", "Les erreurs les plus fréquentes en première année de droit",
                       "Les erreurs les plus fréquentes des étudiants de première année de droit, identifiées et expliquées pour être évitées."),
        breadcrumb_jsonld("erreurs-frequentes-premiere-annee-droit.html", "Erreurs fréquentes en L1", ("Conseils", "conseils.html")),
    ],
    "body": page_hero(
        CRUMB_CONSEILS,
        'Les erreurs les plus fréquentes en <span class="accent-italic">première année de droit</span>.',
        "Certaines erreurs reviennent chaque année, chez des étudiants pourtant sérieux et travailleurs. Les connaître à l'avance permet souvent de les éviter entièrement.",
        meta="Par l'équipe pédagogique de Justicia Académie · Mis à jour en septembre 2026")
    + sec("I.", "Les pièges du premier trimestre.", """
        <div class="sub-block" style="margin-top: 0;">
          <span class="sub-num" aria-hidden="true">1.</span>
          <div><h3>Sous-estimer les premières semaines</h3>
          <p>Le rythme de septembre paraît léger : les notions posées alors sont pourtant le socle de tout le semestre. Un retard pris en octobre se rattrape difficilement en décembre.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">2.</span>
          <div><h3>Réviser uniquement avant les examens</h3>
          <p>Le volume de connaissances d'un semestre de droit ne se mémorise pas efficacement en deux semaines. Les étudiants qui réussissent le mieux relisent leurs cours au fil de l'eau, pas à la dernière minute.</p></div>
        </div>
        <div class="sub-block">
          <span class="sub-num" aria-hidden="true">3.</span>
          <div><h3>Négliger la méthode au profit du seul contenu</h3>
          <p>Connaître son cours ne suffit pas si l'on ne sait pas construire un plan de dissertation ou résoudre un cas pratique : la méthode se travaille séparément du contenu, et tout aussi sérieusement.</p></div>
        </div>""")
    + sec("II.", "Ce qui protège le mieux contre ces erreurs.", """
        <p>Une préparation en amont — sur la méthode des exercices, sur les matières fondamentales, sur l'organisation du travail — désamorce la plupart de ces pièges avant même qu'ils ne se présentent. C'est précisément ce que couvrent nos articles sur <a href="dissertation-juridique-methode.html">la dissertation juridique</a> et sur <a href="heures-travail-personnel-l1-droit.html">la charge de travail réelle en L1</a>.</p>
        <p class="pull-aside">La plupart des échecs en L1 ne viennent pas d'un manque d'intelligence, mais d'un manque d'anticipation.</p>""")
    + cta("Éviter ces erreurs avant qu'elles ne coûtent un semestre.",
          "Un rendez-vous de trente minutes pour construire une préparation qui anticipe ces pièges classiques."),
})


def main():
    for page in PAGES:
        path = SITE / page["slug"]
        path.write_text(render(page), encoding="utf-8")
        print(f"écrit : {path.name}")


if __name__ == "__main__":
    main()
