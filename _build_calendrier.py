# -*- coding: utf-8 -*-
"""Attribue à chaque fiche sa date de mise à disposition, dans
_fiches_metadata.json.

Les matières ne s'ouvrent pas toutes en même temps : elles suivent la
formule à laquelle elles appartiennent. Droit constitutionnel et histoire du
droit relèvent de la première formule et s'ouvrent dès la rentrée ;
introduction générale au droit et méthodologie relèvent de la seconde, qui
ne se lance qu'à la fin décembre. Publier ces vingt fiches plus tôt
reviendrait à livrer gratuitement le contenu d'une formule pas encore
vendue.

À l'intérieur d'une formule, chaque matière est étalée sur la totalité de sa
fenêtre : première fiche le jour d'ouverture, dernière le jour de clôture,
les autres à intervalle régulier. Une matière de cinq fiches avance donc
deux fois moins vite qu'une matière de dix, et les matières d'une même
formule progressent en parallèle — comme à la faculté.

Les dates obtenues tombent toutes le même jour de la semaine que l'ouverture
de leur fenêtre, pour que l'élève sache quel jour regarder.

Ces dates servent deux fois, et c'est voulu : elles alimentent l'affichage
(fiches/index.html, via _build_fiches_index.py) et le verrou réel côté
serveur (table public.fiche_releases, via le fichier SQL écrit ici). Une
seule source, pour que l'écran ne puisse jamais promettre autre chose que
ce que la base autorise.

Pour décaler une formule : changer ses bornes dans FORMULES, puis relancer.
Pour ajuster une seule fiche : éditer sa date à la main dans
_fiches_metadata.json (ce script écrase tout, ne le relancez pas ensuite).

Usage : python3 _build_calendrier.py && python3 _build_fiches_index.py
        puis rejouer supabase/fiches_calendrier.sql dans Supabase.
"""
import json
from datetime import date, timedelta
from pathlib import Path

SITE = Path(__file__).parent
FICHIER = SITE / "_fiches_metadata.json"
SQL = SITE / "supabase" / "fiches_calendrier.sql"

FORMULES = [
    {
        "nom": "Formule 1 — première et terminale",
        "matieres": ["droit-constitutionnel", "histoire-du-droit"],
        "debut": date(2026, 9, 1),
        "fin": date(2026, 12, 1),
    },
    {
        # Inscriptions à la mi-novembre, lancement effectif fin décembre.
        "nom": "Formule 2 — méthodologie et introduction au droit",
        "matieres": ["introduction-generale-au-droit", "methodologie-universitaire"],
        "debut": date(2026, 12, 29),
        "fin": date(2027, 3, 30),
    },
]


def dates_pour(n, debut, fin):
    """n dates régulières de debut à fin, alignées sur le jour d'ouverture."""
    if n == 1:
        return [debut]
    total = (fin - debut).days
    jours = []
    for i in range(n):
        brut = debut + timedelta(days=round(total * i / (n - 1)))
        # Ramené au même jour de semaine que l'ouverture, sans jamais
        # dépasser la clôture ni repasser avant la fiche précédente.
        recul = (brut.weekday() - debut.weekday()) % 7
        jours.append(brut - timedelta(days=recul))
    return jours


def render_sql(data):
    """Recharge intégralement la table des dates, dans une transaction.

    Un delete suivi d'un insert plutôt qu'un upsert : ainsi une fiche retirée
    du JSON disparaît aussi de la table, et ne reste pas ouverte par oubli.
    """
    lignes = ",\n".join(
        f"  ('{slug}/{it['file']}', date '{it['date']}')"
        for slug, matiere in data.items()
        for it in matiere["items"]
    )
    return f"""-- Justicia Académie — calendrier d'ouverture des fiches
--
-- FICHIER GÉNÉRÉ par _build_calendrier.py : ne pas éditer à la main, vos
-- modifications seraient écrasées. La source des dates est
-- _fiches_metadata.json.
--
-- À rejouer dans Supabase (SQL Editor) après chaque changement de dates.
-- Le chemin de chaque ligne doit correspondre exactement au nom de l'objet
-- dans le compartiment "fiches" : c'est sur cette égalité que repose le
-- verrou (voir schema.sql, section 4).

begin;

delete from public.fiche_releases;

insert into public.fiche_releases (path, available_from) values
{lignes};

commit;
"""


def main():
    data = json.loads(FICHIER.read_text(encoding="utf-8"))

    connues = {slug for f in FORMULES for slug in f["matieres"]}
    orphelines = set(data) - connues
    if orphelines:
        raise SystemExit(
            "Ces matières n'appartiennent à aucune formule, leurs dates "
            f"seraient indéterminées : {', '.join(sorted(orphelines))}"
        )

    for formule in FORMULES:
        for slug in formule["matieres"]:
            items = data[slug]["items"]
            jours = dates_pour(len(items), formule["debut"], formule["fin"])
            for item, jour in zip(items, jours):
                item["date"] = jour.isoformat()

    FICHIER.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    SQL.write_text(render_sql(data), encoding="utf-8")

    total = sum(len(m["items"]) for m in data.values())
    print(f"écrit : _fiches_metadata.json ({total} fiches datées)")
    print(f"écrit : supabase/fiches_calendrier.sql ({total} lignes)")
    for formule in FORMULES:
        print(f"\n{formule['nom']}")
        for slug in formule["matieres"]:
            jours = [it["date"] for it in data[slug]["items"]]
            print(f"  {data[slug]['label']} : {jours[0]} → {jours[-1]}")


if __name__ == "__main__":
    main()
