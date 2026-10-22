# Authentification et stockage des fiches — état du chantier

## Mise à jour du 22/10/2026 : nouveau projet Supabase

Le site pointe désormais vers le projet `nmgpdirswamnkxexutvu`
(`https://nmgpdirswamnkxexutvu.supabase.co`, compte justiciaacademie@gmail.com).
Tout ce qui suit mentionnant `ybpgwhmfxxsugiyevylj` est l'ancien projet.

- Schéma, calendrier des 30 fiches, compartiment privé `fiches`, table
  `payments` et politiques RLS : appliqués (migration `justicia_schema_initial`).
  L'élève ne peut plus modifier son propre profil (sinon il aurait pu s'activer
  lui-même) : seul le webhook écrit `subscription_status`.
- Fonctions Edge déployées : `create-checkout-session`, `stripe-webhook`.
- Stripe (mode test) : produit « Formule Justicia Académie » 250 € unique
  (`price_1UTGR9QtGUTsMKkWDJWCIzdX`), webhook `we_1UTGT6QtGUTsMKkWEvYz1UlH` sur
  `checkout.session.completed`.
- **Activation automatique** : après paiement, le webhook envoie une invitation
  par e-mail (l'élève choisit son mot de passe) et passe le profil à `active`
  pour un an. Plus d'activation manuelle.

À faire de votre côté :
1. Secrets des fonctions Edge (Supabase → Edge Functions → Secrets) :
   `STRIPE_SECRET_KEY` (clé `sk_test_...`) et `STRIPE_WEBHOOK_SECRET`
   (`whsec_...`, visible dans Stripe → Developers → Webhooks → ce endpoint).
2. Supabase → Authentication → URL Configuration : Site URL
   `https://www.justicia-academie.com` et ajouter
   `https://www.justicia-academie.com/espace-eleve.html` aux Redirect URLs.
3. Déposer les 30 fiches HTML dans le compartiment `fiches`
   (`matiere/fichen_matiere.html`), car le nouveau projet est vide.
4. Passage en live : clés live, nouveau webhook live, `STRIPE_PRICE_ID`
   du prix live.

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

## Paiement Stripe (déployé, inactif tant que les clés manquent)

Le prix (250 €, paiement unique) est affiché sur `index.html` (#formules),
avec un bouton « Réserver ma place ». Côté Supabase, c'est déjà en place :

- Table `payments` créée (migration `create_payments_table`, RLS activée,
  aucune politique d'accès public — voir [`supabase/paiements.sql`](supabase/paiements.sql)).
- Fonction Edge `create-checkout-session` déployée, JWT non requis (le
  paiement doit rester accessible à un visiteur non connecté, il n'y a pas
  encore d'inscription en ligne).
- Fonction Edge `stripe-webhook` déployée, JWT non requis (Stripe ne peut
  pas en fournir un ; l'authenticité est vérifiée par la signature Stripe).

Tant que les secrets ci-dessous ne sont pas renseignés, le bouton affiche un
message d'indisponibilité — rien à casser en attendant. Il reste de votre
côté, et uniquement du vôtre (clés API à ne jamais transmettre) :

1. **Créer un compte Stripe** (stripe.com), en mode test pour commencer.
2. **Renseigner les secrets** dans Supabase (tableau de bord → Edge
   Functions → Secrets, ou `supabase secrets set`), sans jamais les coller
   ailleurs (ni dans le dépôt, ni dans une conversation) :
   - `STRIPE_SECRET_KEY` : clé secrète Stripe (Developers → API keys).
   - `STRIPE_WEBHOOK_SECRET` : générée à l'étape suivante.
3. **Créer le webhook côté Stripe** (Developers → Webhooks → Add endpoint),
   avec cette URL exacte :
   ```
   https://ybpgwhmfxxsugiyevylj.supabase.co/functions/v1/stripe-webhook
   ```
   Événement à écouter : `checkout.session.completed`. Stripe fournit alors
   le secret de signature à reporter dans `STRIPE_WEBHOOK_SECRET`.
4. **Activation du compte après paiement** : reste manuelle pour l'instant.
   La table `payments` donne la preuve du paiement (e-mail, montant, date) ;
   à vous de créer le compte élève et de passer `subscription_status` à
   `active` comme aujourd'hui. Une automatisation complète (création de
   compte + activation depuis le webhook) est possible plus tard, une fois
   qu'une inscription en ligne existera sur le site.
5. **Passer en mode live** une fois les tests concluants : remplacer les
   clés de test par les clés live (étapes 2 et 3 à refaire avec les clés
   live).

## Ce qui reste de votre côté

1. **Double authentification** : activer sur vos comptes GitHub et
   Supabase (réglages personnels, je n'y ai pas accès).
2. **Contenu légal** : compléter les champs entre crochets de
   [`mentions-legales.html`](mentions-legales.html) et
   [`politique-de-confidentialite.html`](politique-de-confidentialite.html)
   (raison sociale, SIRET, adresse, durées de conservation), puis faire
   valider avant publication.
3. **Site URL Supabase** (`Authentication` → `URL Configuration`) : toujours
   à régler sur `https://www.justicia-academie.com`, sinon les liens de
   confirmation par e-mail des futurs élèves redirigent vers une adresse
   morte après une inscription réussie.
4. **En-têtes de sécurité** : à ajouter selon l'hébergeur final si vous
   voulez un contrôle plus fin que ce que permet GitHub Pages.

## Notes techniques

- La clé publique (`sb_publishable_...`) présente dans `script.js` est sans
  risque : elle est conçue pour être visible côté client, l'accès réel est
  tranché par les règles RLS côté serveur, pas par cette clé.
- Une fonction Edge temporaire (`admin-upload-fiche`) a servi à la migration
  initiale des 30 fichiers ; elle a été neutralisée après usage (renvoie
  410 et exige un jeton valide) plutôt que supprimée, faute d'outil de
  suppression disponible.
