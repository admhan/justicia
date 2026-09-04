-- Justicia Académie — calendrier d'ouverture des fiches
--
-- FICHIER GÉNÉRÉ par _build_calendrier.py : ne pas éditer à la main, vos
-- modifications seraient écrasées. La source des dates est
-- _fiches_metadata.json.
--
-- À rejouer dans Supabase (SQL Editor) après chaque changement de dates.
-- Le chemin de chaque ligne doit correspondre exactement au nom de l'objet
-- dans le compartiment "fiches" : c'est sur cette égalité que repose le
-- verrou (voir schema.sql, section 3).

begin;

delete from public.fiche_releases;

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

commit;
