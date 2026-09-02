-- Justicia Académie — schéma d'authentification et d'abonnement
--
-- À exécuter dans Supabase : Project > SQL Editor > New query, après création
-- du projet. Supabase gère déjà la table auth.users (comptes, mots de passe
-- hachés, sessions) : ce script ne fait qu'ajouter les données propres à
-- Justicia par-dessus, reliées à chaque compte.

-- 1. Profil élève, un par compte -------------------------------------------

create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  email text not null,
  full_name text,
  formule text,                    -- ex. "Terminale hebdomadaire", "L1 annuel"
  subscription_status text not null default 'inactive'
    check (subscription_status in ('active', 'inactive', 'trial')),
  subscription_expires_at timestamptz,
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

-- Chaque élève ne voit et ne modifie que sa propre ligne.
create policy "un élève lit son propre profil"
  on public.profiles for select
  using (auth.uid() = id);

create policy "un élève met à jour son propre profil"
  on public.profiles for update
  using (auth.uid() = id);

-- Création automatique du profil à l'inscription (déclencheur).
create function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email)
  values (new.id, new.email);
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- 2. Stockage des fiches de cours (option "robuste") -----------------------
--
-- Ne pas exécuter cette section si vous choisissez l'option légère
-- (fiches laissées en fichiers publics sur GitHub Pages).
--
-- Étapes manuelles associées, dans le tableau de bord Supabase :
--   Storage > Create bucket > nom "fiches" > Public bucket = NON (privé).
-- Puis uploader les fichiers de site/fiches/ dans ce bucket, en conservant
-- la même arborescence (ex. introduction-generale-au-droit/fiche1_....html).

create policy "un abonné actif lit les fiches"
  on storage.objects for select
  using (
    bucket_id = 'fiches'
    and exists (
      select 1 from public.profiles
      where profiles.id = auth.uid()
        and profiles.subscription_status = 'active'
    )
  );
