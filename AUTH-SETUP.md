# Mise en place de l'authentification réelle — guide pas à pas

Ce document sépare ce qui vous revient (compte, décisions) de ce qui revient
au code (déjà préparé ou prêt à l'être dès que vous avez les clés).

## Votre part

### 1. Créer le projet Supabase

- Aller sur [supabase.com](https://supabase.com), créer un compte, créer un
  nouveau projet (choisir une région proche, ex. Europe/Paris ou Frankfurt).
- Une fois créé : `Project Settings` → `API`. Deux valeurs à me transmettre :
  - **Project URL** (ex. `https://xxxxxxxx.supabase.co`)
  - **anon public key** (longue chaîne, commence par `eyJ...`)
  - Ne jamais transmettre la **service_role key** : elle contourne toutes
    les règles de sécurité, elle ne doit exister que dans Supabase lui-même.

### 2. Exécuter le schéma

- `SQL Editor` → coller le contenu de [`supabase/schema.sql`](supabase/schema.sql) → Run.
- Si vous voulez la protection "robuste" des fiches (recommandée), suivre
  aussi les étapes de la section 2 du fichier (création du bucket Storage).

### 3. Décider du modèle d'abonnement

- Qui passe `subscription_status` à `active` pour un élève : vous
  manuellement dans Supabase (`Table Editor` → `profiles`), ou un paiement
  automatisé (Stripe) plus tard ? Dites-le-moi, ça change le code à écrire.

### 4. Sécurité de compte

- Activer la double authentification sur votre compte GitHub
  (`Settings` → `Password and authentication`).
- Idem sur le compte Supabase une fois créé.

### 5. Contenu légal

- Brouillons déjà rédigés : [`mentions-legales.html`](mentions-legales.html)
  et [`politique-de-confidentialite.html`](politique-de-confidentialite.html),
  liés depuis le pied de page de tout le site. Les champs entre crochets
  (raison sociale, adresse, SIRET, durées de conservation) sont à compléter
  par vous, puis à faire valider avant publication — obligation renforcée
  car le site s'adresse en partie à des mineurs.

## Ma part (dès que j'ai l'URL et la clé publique)

- Remplacer la connexion de démonstration dans `espace-eleve.html` et
  `script.js` par de vrais appels Supabase Auth (inscription, connexion,
  session, mot de passe oublié) — le code cible est déjà documenté dans
  [`supabase/client.example.js`](supabase/client.example.js), il ne reste
  qu'à y mettre les vraies clés et à le brancher aux pages.
- Brancher l'affichage de l'espace élève sur `profiles.subscription_status`.
- Si option robuste choisie (retenu) : servir les fiches depuis le bucket
  privé au lieu des fichiers publics actuels, et retirer `fiches/` du
  dépôt public une fois la bascule faite.
- Ajouter les en-têtes de sécurité compatibles avec l'hébergeur choisi.
- Rien de tout cela ne sera poussé sur GitHub sans votre confirmation.

## Déjà fait, sans dépendance à vos clés

- `.gitignore` protège désormais tout fichier `.env*` et
  `supabase/client.local.js` d'un envoi accidentel sur GitHub.
- Pages légales créées et reliées dans tous les pieds de page du site.
- Schéma de base de données et exemple d'intégration prêts, à activer dès
  que le projet Supabase existe.
