-- Justicia Académie — migration : verrou réel des fiches par date
--
-- À exécuter UNE FOIS dans Supabase : Project > SQL Editor > New query,
-- puis coller ce fichier entier et lancer.
--
-- Ce que cela change : jusqu'ici, le compartiment "fiches" s'ouvrait sur le
-- seul critère de l'abonnement actif, et le calendrier n'existait que dans la
-- page (contournable depuis la console du navigateur). Après cette migration,
-- c'est le serveur qui refuse une fiche non échue.
--
-- IMPORTANT — enchaîner immédiatement avec supabase/fiches_calendrier.sql.
-- Entre les deux, la table des dates est vide et la règle étant volontairement
-- « fermée par défaut », AUCUNE fiche ne s'ouvrira. C'est le bon sens de
-- l'erreur, mais ne laissez pas traîner l'entre-deux.
--
-- Ordre complet :
--   1. ce fichier
--   2. supabase/fiches_calendrier.sql   (les 30 dates)
--   3. la requête de contrôle en fin de fichier, pour vérifier

begin;

-- 1. La table des dates -----------------------------------------------------

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

-- 2. La nouvelle règle de lecture du compartiment ---------------------------

drop policy if exists "un abonné actif lit les fiches" on storage.objects;

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

commit;


-- 3. Contrôle, à lancer APRÈS supabase/fiches_calendrier.sql ----------------
--
-- Doit renvoyer : 30 fiches au calendrier, 30 objets, 0 orphelin de chaque
-- côté. Un orphelin signale un chemin qui ne correspond à rien — donc une
-- fiche qui ne s'ouvrira jamais, ou un fichier hors calendrier.
--
-- select
--   (select count(*) from public.fiche_releases)                    as au_calendrier,
--   (select count(*) from storage.objects where bucket_id='fiches') as dans_le_compartiment,
--   (select count(*) from public.fiche_releases r
--      where not exists (select 1 from storage.objects o
--                        where o.bucket_id='fiches' and o.name = r.path)) as dates_sans_fichier,
--   (select count(*) from storage.objects o where o.bucket_id='fiches'
--      and not exists (select 1 from public.fiche_releases r
--                      where r.path = o.name))                      as fichiers_sans_date,
--   (select count(*) from public.fiche_releases
--      where available_from <= (now() at time zone 'Europe/Paris')::date) as deja_ouvertes;
