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

-- 3. Calendrier d'ouverture des fiches --------------------------------------
--
-- Les fiches s'ouvrent au fil du semestre. Cette table dit à quelle date
-- chaque fichier du compartiment devient lisible ; la politique de lecture
-- ci-dessous la consulte. Le verrou est donc tranché par le serveur, et pas
-- seulement affiché par la page : masquer un lien dans le navigateur
-- n'empêche personne de demander l'URL signée à la main.
--
-- La table est peuplée par supabase/fiches_calendrier.sql, lui-même généré
-- depuis _fiches_metadata.json : mêmes dates à l'écran et dans la base.

create table public.fiche_releases (
  path text primary key,           -- nom exact de l'objet dans le compartiment
  available_from date not null
);

alter table public.fiche_releases enable row level security;

-- Le calendrier n'est pas un secret : les dates sont déjà affichées sur la
-- page des fiches. Il doit surtout rester lisible par l'élève, car la
-- politique de lecture ci-dessous interroge cette table *en son nom* : sans
-- ce droit de lecture, la sous-requête ne verrait rien et refuserait tout.
create policy "un élève lit le calendrier"
  on public.fiche_releases for select
  to authenticated
  using (true);

-- 4. Stockage des fiches de cours (option "robuste") -----------------------
--
-- Ne pas exécuter cette section si vous choisissez l'option légère
-- (fiches laissées en fichiers publics sur GitHub Pages).
--
-- Étapes manuelles associées, dans le tableau de bord Supabase :
--   Storage > Create bucket > nom "fiches" > Public bucket = NON (privé).
-- Puis uploader les fichiers de site/fiches/ dans ce bucket, en conservant
-- la même arborescence (ex. introduction-generale-au-droit/fiche1_....html).
--
-- Deux conditions cumulatives : un abonnement actif, et une date d'ouverture
-- échue. Une fiche absente de fiche_releases reste fermée — le silence vaut
-- refus, de sorte qu'un fichier déposé dans le compartiment sans être inscrit
-- au calendrier ne s'ouvre pas par accident.

create policy "un abonné actif lit les fiches échues"
  on storage.objects for select
  using (
    bucket_id = 'fiches'
    and exists (
      select 1 from public.profiles
      where profiles.id = auth.uid()
        and profiles.subscription_status = 'active'
    )
    and exists (
      select 1 from public.fiche_releases
      where fiche_releases.path = objects.name
        -- Heure de Paris, et non UTC : une fiche du 8 septembre s'ouvre à
        -- minuit pour l'élève, pas à deux heures du matin.
        and fiche_releases.available_from <= (now() at time zone 'Europe/Paris')::date
    )
  );
