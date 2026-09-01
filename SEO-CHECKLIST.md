# SEO Justicia Académie — état des lieux et actions restantes

## Fait dans le code (rien à refaire)

- Balises title et meta description uniques sur les 11 pages
- Canoniques, Open Graph et Twitter Card partout
- Données structurées JSON-LD : EducationalOrganization + FAQPage (accueil),
  Article (page études + 4 articles), Course + BreadcrumbList (4 pages formule),
  CollectionPage (index Conseils)
- robots.txt et sitemap.xml (11 URL)
- Maillage interne : nav, footer 4 colonnes, liens croisés articles ↔ formules
- 4 pages formule = 1 URL par requête cible (« stage pré-rentrée droit », etc.)
- Section Conseils avec 4 articles piliers rédigés
- HTML sémantique, lang="fr", alt/aria sur les éléments visuels

## À faire à la mise en ligne (ne peut pas être fait dans le code)

1. **Domaine et HTTPS** : déployer sur justicia-academie.com (les canoniques et
   le sitemap pointent déjà dessus). Rediriger en 301 les anciennes URL du site
   actuel vers les nouvelles pages équivalentes.
2. **Google Search Console** : valider le domaine, soumettre sitemap.xml,
   surveiller la couverture d'indexation les premières semaines.
3. **Google Business Profile** : créer la fiche du centre parisien (adresse
   exacte, horaires, photos, catégorie « centre de soutien scolaire » ou
   équivalent). C'est le levier n°1 pour « prépa droit Paris ».
4. **Avis clients réels** : collecter des avis Google sur la fiche. Le jour où
   la note vient d'une source vérifiable, on pourra l'ajouter au balisage
   AggregateRating (volontairement omis tant que la note affichée est déclarative).
5. **Remplacer le contenu fictif** : témoignages, note 4,8, prénoms. Les faux
   avis sont sanctionnables (DGCCRF) et fragilisent le référencement.
6. **Mentions légales et politique de confidentialité** : pages à créer avant
   mise en ligne (obligation légale, et signal de confiance pour Google).
7. **Formulaire** : brancher le formulaire de rendez-vous sur un vrai backend
   ou un service (Formspree, Tally, HubSpot...) au lieu du mailto actuel.
8. **Image Open Graph dédiée** : créer une image 1200×630 aux couleurs de la
   marque pour remplacer le logo dans les balises og:image.

## Rythme de contenu recommandé

1 à 2 articles par mois dans Conseils. Procédure : ajouter l'entrée dans
_build_pages.py, relancer `python3 _build_pages.py`, ajouter la carte dans
conseils.html et l'URL dans sitemap.xml.

### Calendrier éditorial — 20 sujets par grappe

Priorité immédiate (fort volume + lien direct avec les formules) : n° 6, 11, 16.

**Orientation au lycée**
1. Le droit est-il fait pour moi ? Les signes qui ne trompent pas
2. Que faire dès la première pour préparer une licence de droit
3. Droit ou Sciences Po : comment choisir
4. Faut-il être bon en français pour faire du droit ?
5. L'option DGEMC en terminale : vrai atout pour Parcoursup ?

**Parcoursup** (saisonnalité décembre-mars)
6. Lettre de motivation Parcoursup pour le droit : exemples commentés
7. Assas, Sorbonne, Nanterre, Saclay : choisir sa faculté de droit en Île-de-France
8. Double licence droit-éco, droit-langues, droit-histoire : pour qui ?
9. Refusé en licence de droit : les plans B qui mènent quand même au droit (publier en juin)
10. Les attendus Parcoursup de la licence de droit, décryptés ligne par ligne

**Réussir sa L1** (pics été et janvier)
11. La dissertation juridique : la méthode en deux parties expliquée
12. Le cas pratique en droit : méthode et exemple corrigé
13. Comment prendre des notes en cours magistral
14. Les TD de droit : comment les préparer sans y passer ses nuits
15. Réviser ses partiels de droit : planning sur six semaines (publier novembre et mars)
16. Le vocabulaire juridique à connaître avant la rentrée (format lexique)
17. Premier semestre raté : comment se rattraper au second (publier en janvier)

**Se projeter** (cible parents incluse)
18. Que faire après une licence de droit ? Masters, concours, passerelles
19. Métiers du droit : études, concours et salaires, le panorama honnête
20. Devenir magistrat : le parcours complet, de la terminale à l'ENM
    (série déclinable : avocat, notaire, commissaire de police)

Chaque article peut être décliné en capsule vidéo courte (format des deux
vidéos existantes) : même sujet, deux canaux.
