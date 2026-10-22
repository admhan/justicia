-- Justicia Académie — traçabilité des paiements Stripe
--
-- À exécuter dans Supabase après supabase/schema.sql. Chaque paiement
-- confirmé par Stripe (webhook supabase/functions/stripe-webhook) est
-- enregistré ici. Tant que l'inscription reste manuelle (voir
-- AUTH-SETUP.md), cette table sert de preuve de paiement à rapprocher d'un
-- compte élève ; elle ne déclenche pas encore l'activation automatique de
-- l'abonnement.

create table public.payments (
  id uuid primary key default gen_random_uuid(),
  stripe_session_id text not null unique,
  customer_email text,
  amount_total integer,            -- en centimes, ex. 25000 pour 250 €
  currency text,
  status text not null default 'paye',
  created_at timestamptz not null default now()
);

alter table public.payments enable row level security;

-- Aucune politique d'accès : la table n'est lisible et modifiable que par
-- la clé de service, utilisée uniquement dans la fonction Edge
-- stripe-webhook. Un élève ou un visiteur ne doit jamais pouvoir lire les
-- paiements des autres.
