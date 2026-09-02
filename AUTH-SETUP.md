# Authentification et stockage des fiches — état du chantier

## Fait, en production sur le projet Supabase JusticiaSupabase (`ybpgwhmfxxsugiyevylj`)

- **Authentification réelle** : `espace-eleve.html` et `script.js` utilisent
  Supabase Auth (inscription, connexion, session, déconnexion). Plus de
  démonstration côté client.
- **Base de données** : table `profiles` (un profil par compte, créé
  automatiquement à l'inscription via déclencheur), sécurité au niveau ligne
  activée — voir [`supabase/schema.sql`](supabase/schema.sql).
- **Stockage des fiches (option robuste retenue)** : les 30 fiches ne sont
  plus des fichiers publics dans le dépôt. Elles vivent dans le compartiment
  privé Supabase Storage `fiches`, accessible uniquement via URL signée
  (validité 60 secondes), elle-même délivrée seulement si
  `profiles.subscription_status = 'active'`. Testé de bout en bout : accès
  refusé sans abonnement actif, autorisé une fois activé, contenu
  byte-identique à l'original.
- `fiches/index.html` liste les titres et génère les URL signées au clic
  (voir `.fiche-link` dans `script.js`). Ses métadonnées (titres, numéros,
  chemins) sont figées dans `_fiches_metadata.json`, plus besoin des
  fichiers sources locaux pour régénérer la page.
- Sécurité vérifiée automatiquement (`get_advisors`) : un point corrigé
  (fonction interne du déclencheur rendue non appelable depuis l'API
  publique), aucun avertissement restant.

## Comment ajouter ou modifier une fiche désormais

1. Déposer le nouveau fichier HTML dans le compartiment Storage `fiches`
   (tableau de bord Supabase → Storage → fiches), en respectant
   l'arborescence `matiere/fiche.html`.
2. Mettre à jour `_fiches_metadata.json` (numéro, nom de fichier, titre).
3. `python3 _build_fiches_index.py` pour régénérer `fiches/index.html`.

## Ce qui reste de votre côté

1. **Modèle d'abonnement** : qui passe `subscription_status` à `active` —
   vous manuellement dans Supabase (`Table Editor` → `profiles`), ou un
   paiement automatisé (Stripe) plus tard ? À trancher pour la suite.
2. **Double authentification** : activer sur vos comptes GitHub et
   Supabase (réglages personnels, je n'y ai pas accès).
3. **Contenu légal** : compléter les champs entre crochets de
   [`mentions-legales.html`](mentions-legales.html) et
   [`politique-de-confidentialite.html`](politique-de-confidentialite.html)
   (raison sociale, SIRET, adresse, durées de conservation), puis faire
   valider avant publication.
4. **Site URL Supabase** (`Authentication` → `URL Configuration`) : toujours
   à régler sur `https://admhan.github.io/justicia/`, sinon les liens de
   confirmation par e-mail des futurs élèves redirigent vers une adresse
   morte après une inscription réussie.
5. **En-têtes de sécurité** : à ajouter selon l'hébergeur final si vous
   voulez un contrôle plus fin que ce que permet GitHub Pages.

## Notes techniques

- La clé publique (`sb_publishable_...`) présente dans `script.js` est sans
  risque : elle est conçue pour être visible côté client, l'accès réel est
  tranché par les règles RLS côté serveur, pas par cette clé.
- Une fonction Edge temporaire (`admin-upload-fiche`) a servi à la migration
  initiale des 30 fichiers ; elle a été neutralisée après usage (renvoie
  410 et exige un jeton valide) plutôt que supprimée, faute d'outil de
  suppression disponible.
