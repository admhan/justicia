-- Justicia Académie — verrou réel des fiches par date
--
-- UN SEUL COPIER-COLLER, dans Supabase > SQL Editor > New query.
-- Tout est dans une transaction : soit l'ensemble passe, soit rien ne change.
-- Il n'existe donc aucun instant où les fiches seraient fermées à tort.
--
-- Après coup, pour changer les dates : éditer _fiches_metadata.json, relancer
--   python3 _build_calendrier.py && python3 _build_fiches_index.py
-- puis rejouer supabase/fiches_calendrier.sql (qui recharge la table seule).

begin;

-- 1. La table des dates -----------------------------------------------------

create table public.fiche_releases (
  path text primary key,           -- nom exact de l'objet dans le compartiment
  available_from date not null
);

alter table public.fiche_releases enable row level security;

-- Le calendrier n'est pas un secret : les dates sont déjà affichées sur la
-- page. Il doit surtout rester lisible par l'élève, car la politique de
-- lecture ci-dessous interroge cette table *en son nom* : sans ce droit, la
-- sous-requête ne verrait rien et refuserait tout.
create policy "un élève lit le calendrier"
  on public.fiche_releases for select
  to authenticated
  using (true);

-- 2. Les 30 dates -----------------------------------------------------------

insert into public.fiche_releases (path, available_from) values
('introduction-generale-au-droit/fiche1_introduction_generale_au_droit.html', date '2026-09-01'),
  ('introduction-generale-au-droit/fiche2_introduction_generale_au_droit.html', date '2026-09-08'),
  ('introduction-generale-au-droit/fiche3_introduction_generale_au_droit.html', date '2026-09-15'),
  ('introduction-generale-au-droit/fiche4_introduction_generale_au_droit.html', date '2026-09-29'),
  ('introduction-generale-au-droit/fiche5_introduction_generale_au_droit.html', date '2026-10-06'),
  ('introduction-generale-au-droit/fiche6_introduction_generale_au_droit.html', date '2026-10-20'),
  ('introduction-generale-au-droit/fiche7_introduction_generale_au_droit.html', date '2026-10-27'),
  ('introduction-generale-au-droit/fiche8_introduction_generale_au_droit.html', date '2026-11-10'),
  ('introduction-generale-au-droit/fiche9_introduction_generale_au_droit.html', date '2026-11-17'),
  ('introduction-generale-au-droit/fiche10_introduction_generale_au_droit.html', date '2026-12-01'),
  ('methodologie-universitaire/fiche1_methodologie_universitaire.html', date '2026-09-01'),
  ('methodologie-universitaire/fiche2_methodologie_universitaire.html', date '2026-09-08'),
  ('methodologie-universitaire/fiche3_methodologie_universitaire.html', date '2026-09-15'),
  ('methodologie-universitaire/fiche4_methodologie_universitaire.html', date '2026-09-29'),
  ('methodologie-universitaire/fiche5_methodologie_universitaire.html', date '2026-10-06'),
  ('methodologie-universitaire/fiche6_methodologie_universitaire.html', date '2026-10-20'),
  ('methodologie-universitaire/fiche7_methodologie_universitaire.html', date '2026-10-27'),
  ('methodologie-universitaire/fiche8_methodologie_universitaire.html', date '2026-11-10'),
  ('methodologie-universitaire/fiche9_methodologie_universitaire.html', date '2026-11-17'),
  ('methodologie-universitaire/fiche10_methodologie_universitaire.html', date '2026-12-01'),
  ('droit-constitutionnel/fiche1_droit_constitutionnel.html', date '2026-09-01'),
  ('droit-constitutionnel/fiche2_droit_constitutionnel.html', date '2026-09-22'),
  ('droit-constitutionnel/fiche3_droit_constitutionnel.html', date '2026-10-13'),
  ('droit-constitutionnel/fiche4_droit_constitutionnel.html', date '2026-11-03'),
  ('droit-constitutionnel/fiche5_droit_constitutionnel.html', date '2026-12-01'),
  ('histoire-du-droit/fiche1_histoire_du_droit.html', date '2026-09-01'),
  ('histoire-du-droit/fiche2_histoire_du_droit.html', date '2026-09-22'),
  ('histoire-du-droit/fiche3_histoire_du_droit.html', date '2026-10-13'),
  ('histoire-du-droit/fiche4_histoire_du_droit.html', date '2026-11-03'),
  ('histoire-du-droit/fiche5_histoire_du_droit.html', date '2026-12-01');

-- 3. La nouvelle règle de lecture du compartiment ---------------------------

drop policy if exists "un abonné actif lit les fiches" on storage.objects;

-- Deux conditions cumulatives : abonnement actif ET date échue. Une fiche
-- absente du calendrier reste fermée — le silence vaut refus, de sorte qu'un
-- fichier déposé sans être inscrit ne s'ouvre pas par inadvertance.
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

commit;

-- 4. Contrôle ---------------------------------------------------------------
-- Attendu aujourd'hui : 30 | 30 | 0 | 0 | 4

select
  (select count(*) from public.fiche_releases)                     as au_calendrier,
  (select count(*) from storage.objects where bucket_id='fiches')  as dans_le_compartiment,
  (select count(*) from public.fiche_releases r
     where not exists (select 1 from storage.objects o
                       where o.bucket_id='fiches' and o.name = r.path)) as dates_sans_fichier,
  (select count(*) from storage.objects o where o.bucket_id='fiches'
     and not exists (select 1 from public.fiche_releases r
                     where r.path = o.name))                       as fichiers_sans_date,
  (select count(*) from public.fiche_releases
     where available_from <= (now() at time zone 'Europe/Paris')::date) as deja_ouvertes;
