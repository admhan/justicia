# Prompt de reprise — sécurité et authentification Justicia Académie

Ce fichier sert à reprendre ce chantier dans une future conversation, avec
tout le contexte nécessaire déjà posé. Copier-coller le bloc « Prompt » ci-dessous
tel quel, ou l'adapter selon l'avancement réel au moment de la reprise.

## État des décisions (déjà tranché, ne pas redemander)

- **Fournisseur** : Supabase (Postgres + Auth + Row Level Security + Storage).
- **Protection des fiches** : option **robuste**. Les fiches de cours ne
  restent pas des fichiers publics sur GitHub Pages ; elles sont servies
  depuis un bucket Supabase Storage privé, livrées seulement si
  `profiles.subscription_status = 'active'`.
- **Hébergement du site** : GitHub Pages (`admhan/justicia`), conservé —
  compatible avec Supabase car l'authentification et les données passent
  par des appels HTTPS externes, pas par du code serveur local.
- **Public** : inclut des mineurs → vigilance RGPD renforcée obligatoire.

## Fichiers déjà préparés (à vérifier avant de redemander leur création)

- `supabase/schema.sql` — table `profiles`, RLS, déclencheur de création de
  profil à l'inscription, politique de stockage pour le bucket `fiches`.
- `AUTH-SETUP.md` — guide pas à pas, sépare la part utilisateur et la part
  technique.
- Ce fichier (`PROMPT-SECURITE-AUTH.md`).

## Ce qui restait bloquant à la dernière session

- Le compte Supabase n'était pas encore créé.
- L'URL du projet et la clé publique (« anon key ») n'avaient pas été
  transmises.
- Le mode d'activation de l'abonnement (manuel vs paiement automatisé type
  Stripe) n'était pas tranché.
- Aucun connecteur Supabase MCP n'était disponible dans la session Claude
  Code (à vérifier à nouveau : un connecteur ajouté dans claude.ai ne
  s'attache pas automatiquement à une session Claude Code, il faut le
  configurer via `.mcp.json` ou `claude mcp add` avec un jeton Supabase).

---

## Prompt à coller

Je reprends le chantier sécurité et authentification du site Justicia
Académie (dépôt GitHub `admhan/justicia`, hébergé sur GitHub Pages à
`https://admhan.github.io/justicia/`).

Contexte à relire avant d'agir : `AUTH-SETUP.md` et `supabase/schema.sql`
à la racine du site contiennent déjà le plan et le schéma validés.
Décisions déjà prises, ne pas les remettre en question sans raison
nouvelle : fournisseur Supabase, protection des fiches en mode robuste
(Storage privé + RLS), hébergement GitHub Pages conservé.

Avant de commencer, vérifie l'état d'avancement réel :
1. Le compte et le projet Supabase existent-ils déjà ? Ai-je transmis
   l'URL du projet et la clé publique (anon key) ?
2. Le schéma `supabase/schema.sql` a-t-il déjà été exécuté dans Supabase ?
3. Le bucket Storage `fiches` existe-t-il, les fichiers y ont-ils déjà été
   déposés ?
4. Un connecteur MCP Supabase est-il disponible dans cette session
   (vérifier via la recherche de connecteurs) ? Si oui, l'utiliser pour
   accélérer ; si non, me redonner la liste des actions qui restent de
   mon ressort (compte, clés, décisions).

Puis, selon ce que tu trouves :
- Si le projet Supabase et les clés existent déjà : branche
  `espace-eleve.html` et `script.js` sur de vrais appels Supabase Auth
  (inscription, connexion, session, mot de passe oublié), remplace la
  connexion de démonstration, et sers les fiches depuis le bucket privé
  au lieu des fichiers publics actuels de `fiches/`.
- Sinon : redonne-moi la liste à jour de ce qui est bloquant de mon côté,
  sans redemander ce qui est déjà décidé ci-dessus.

Dans tous les cas :
- N'ajoute aucune clé secrète (service_role) dans le dépôt Git.
- Ajoute les en-têtes de sécurité compatibles avec l'hébergeur en place.
- Rédige un brouillon de politique de confidentialité et de mentions
  légales tenant compte du public mineur, à me faire valider avant
  publication.
- Ne pousse rien sur GitHub sans me le signaler d'abord.
- Termine par une checklist claire de ce qui reste, classé par qui doit
  agir (moi ou toi).
