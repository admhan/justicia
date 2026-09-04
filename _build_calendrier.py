# -*- coding: utf-8 -*-
"""Attribue à chaque fiche sa date de mise à disposition, dans
_fiches_metadata.json.

Chaque matière est étalée sur la totalité du semestre : la première fiche
tombe le jour de la rentrée, la dernière le jour de clôture, les autres à
intervalle régulier entre les deux. Une matière de cinq fiches avance donc
deux fois moins vite qu'une matière de dix, et les quatre matières
progressent en parallèle — comme à la faculté.

Les dates obtenues tombent toutes le même jour de la semaine que la
rentrée, pour que l'élève sache quel jour regarder.

Pour décaler le semestre : changer DEBUT et FIN ci-dessous, puis relancer.
Pour ajuster une seule fiche : éditer sa date à la main dans
_fiches_metadata.json (ce script écrase tout, ne le relancez pas ensuite).

Usage : python3 _build_calendrier.py && python3 _build_fiches_index.py
"""
import json
from datetime import date, timedelta
from pathlib import Path

SITE = Path(__file__).parent
FICHIER = SITE / "_fiches_metadata.json"

DEBUT = date(2026, 9, 1)
FIN = date(2026, 12, 1)


def dates_pour(n):
    """n dates régulières de DEBUT à FIN, alignées sur le jour de la rentrée."""
    if n == 1:
        return [DEBUT]
    total = (FIN - DEBUT).days
    jours = []
    for i in range(n):
        brut = DEBUT + timedelta(days=round(total * i / (n - 1)))
        # Ramené au même jour de semaine que la rentrée, sans jamais
        # dépasser FIN ni repasser avant la fiche précédente.
        recul = (brut.weekday() - DEBUT.weekday()) % 7
        jours.append(brut - timedelta(days=recul))
    return jours


def main():
    data = json.loads(FICHIER.read_text(encoding="utf-8"))

    for slug, matiere in data.items():
        items = matiere["items"]
        for item, jour in zip(items, dates_pour(len(items))):
            item["date"] = jour.isoformat()

    FICHIER.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    total = sum(len(m["items"]) for m in data.values())
    print(f"écrit : _fiches_metadata.json ({total} fiches datées)")
    for slug, matiere in data.items():
        jours = [it["date"] for it in matiere["items"]]
        print(f"  {matiere['label']} : {jours[0]} → {jours[-1]}")


if __name__ == "__main__":
    main()
