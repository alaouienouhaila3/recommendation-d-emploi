"""
evaluation.py — Evaluation Precision@K du systeme de recommandation
Semaine 4 - Membre 1

Teste l'algorithme recommender.calculer_scores() sur 10 profils varies,
en utilisant des offres reelles recuperees via JSearch (jsearch.fetch_jobs).

Regle de pertinence : une offre recommandee est consideree "pertinente"
si son titre ou sa description contient au moins un des mots-cles
principaux du profil de test (comparaison insensible a la casse).

Usage :
    python evaluation.py
"""

import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from jsearch import fetch_jobs
from recommender import calculer_scores


# ---------------------------------------------------------------------------
# 10 profils de test varies (competences techniques realistes, marche marocain)
# "mots_cles_pertinence" = mots utilises pour juger si une offre est pertinente
# ---------------------------------------------------------------------------
PROFILS_TEST = [
    {
        "nom": "Développeur Python Junior",
        "competences": "python",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["python", "django", "flask"],
    },
    {
        "nom": "Développeur Fullstack JS",
        "competences": "javascript",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["javascript", "react", "node"],
    },
    {
        "nom": "Data Scientist",
        "competences": "data science",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["data", "machine learning", "ml"],
    },
    {
        "nom": "Ingénieur DevOps",
        "competences": "devops",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["devops", "docker", "kubernetes"],
    },
    {
        "nom": "Développeur Java",
        "competences": "java",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["java", "spring"],
    },
    {
        "nom": "Administrateur Réseaux",
        "competences": "reseau",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["reseau", "network", "cisco"],
    },
    {
        "nom": "Développeur PHP",
        "competences": "php",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["php", "symfony", "laravel"],
    },
    {
        "nom": "Data Analyst",
        "competences": "data analyst",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["data", "sql", "analyst"],
    },
    {
        "nom": "Ingénieur QA / Testeur",
        "competences": "testeur",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["test", "qa", "selenium"],
    },
    {
        "nom": "Développeur Mobile",
        "competences": "mobile",
        "experience": "",
        "formation": "",
        "mots_cles_pertinence": ["android", "mobile", "kotlin"],
    },
]


def est_pertinente(offre: dict, mots_cles: list) -> bool:
    """Une offre est pertinente si au moins un mot-cle apparait dans
    son titre ou sa description (insensible a la casse)."""
    texte = f"{offre.get('job_title', '')} {offre.get('job_description', '')}".lower()
    return any(mot.lower() in texte for mot in mots_cles)


def precision_at_k(offres_triees: list, mots_cles: list, k: int) -> float:
    """Calcule Precision@K sur les K premieres offres triees par score.
    Important : le denominateur est toujours K (pas le nombre d'offres
    disponibles), pour eviter de surestimer la precision quand peu
    d'offres ont ete recuperees."""
    if not offres_triees:
        return 0.0
    top_k = offres_triees[:k]
    pertinentes = sum(1 for o in top_k if est_pertinente(o, mots_cles))
    return pertinentes / k


def evaluer_profil(profil: dict) -> dict:
    """Recupere des offres reelles via JSearch, calcule les scores TF-IDF,
    puis Precision@5 et Precision@10 pour un profil donne."""
    try:
        offres = fetch_jobs(query=profil["competences"], location="Morocco", num_pages=3)
    except Exception as e:
        print(f"  Erreur JSearch pour '{profil['nom']}': {e}")
        offres = []

    if not offres:
        return {
            "nom": profil["nom"],
            "nb_offres_recuperees": 0,
            "precision_5": 0.0,
            "precision_10": 0.0,
            "alerte": "Aucune offre - profil exclu de la moyenne",
        }

    profil_dict = {
        "competences": profil["competences"],
        "experience": profil["experience"],
        "formation": profil["formation"],
    }
    top10 = calculer_scores(profil=profil_dict, offres=offres)

    p5 = precision_at_k(top10, profil["mots_cles_pertinence"], k=5)
    p10 = precision_at_k(top10, profil["mots_cles_pertinence"], k=10)

    alerte = ""
    if len(offres) < 10:
        alerte = f"Seulement {len(offres)} offre(s) disponible(s) (< K=10)"

    return {
        "nom": profil["nom"],
        "nb_offres_recuperees": len(offres),
        "precision_5": round(p5 * 100, 1),
        "precision_10": round(p10 * 100, 1),
        "alerte": alerte,
    }


def main():
    print("=" * 70)
    print("EVALUATION PRECISION@K — Systeme de recommandation d'emploi")
    print("=" * 70)
    print(f"Nombre de profils testes : {len(PROFILS_TEST)}")
    print()

    resultats = []
    for i, profil in enumerate(PROFILS_TEST, 1):
        print(f"[{i}/{len(PROFILS_TEST)}] Test profil : {profil['nom']} ...")
        resultat = evaluer_profil(profil)
        resultats.append(resultat)
        print(f"    -> Offres recuperees: {resultat['nb_offres_recuperees']} | "
              f"P@5: {resultat['precision_5']}% | P@10: {resultat['precision_10']}%")
        time.sleep(1)  # eviter de spammer l'API JSearch

    print()
    print("=" * 70)
    print("TABLEAU RECAPITULATIF")
    print("=" * 70)
    print(f"{'Profil':<30} {'Offres':>8} {'P@5':>8} {'P@10':>8}")
    print("-" * 70)
    for r in resultats:
        print(f"{r['nom']:<30} {r['nb_offres_recuperees']:>8} "
              f"{r['precision_5']:>7}% {r['precision_10']:>7}%")
        if r.get("alerte"):
            print(f"    ⚠ {r['alerte']}")

    moyenne_p5 = sum(r["precision_5"] for r in resultats) / len(resultats)
    moyenne_p10 = sum(r["precision_10"] for r in resultats) / len(resultats)
    print("-" * 70)
    print(f"{'MOYENNE (sur 10 profils)':<30} {'':>8} {moyenne_p5:>7.1f}% {moyenne_p10:>7.1f}%")
    print("=" * 70)

    nb_insuffisants = sum(1 for r in resultats if r["nb_offres_recuperees"] < 10)
    if nb_insuffisants:
        print(f"\n⚠ Attention : {nb_insuffisants}/10 profils ont recupere moins de 10 offres.")
        print("  Cela penalise mecaniquement leur Precision@10 (denominateur = K = 10")
        print("  meme si moins d'offres etaient disponibles). C'est une limite de")
        print("  couverture JSearch sur le marche marocain, pas un defaut de l'algorithme")
        print("  TF-IDF lui-meme. A mentionner explicitement dans le rapport.")

    if moyenne_p10 < 60:
        print("\n⚠ Precision@10 moyenne < 60% — optimisation des hyperparametres")
        print("  TF-IDF recommandee (voir recommender.py).")
    else:
        print("\n✓ Precision@10 moyenne >= 60% — performance jugee satisfaisante.")

    # Sauvegarde des resultats dans un fichier texte pour le rapport
    out_path = Path(__file__).resolve().parent / "resultats_precision_k.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("RESULTATS PRECISION@K\n")
        f.write("=" * 70 + "\n")
        f.write(f"{'Profil':<30} {'Offres':>8} {'P@5':>8} {'P@10':>8}\n")
        f.write("-" * 70 + "\n")
        for r in resultats:
            f.write(f"{r['nom']:<30} {r['nb_offres_recuperees']:>8} "
                     f"{r['precision_5']:>7}% {r['precision_10']:>7}%\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'MOYENNE':<30} {'':>8} {moyenne_p5:>7.1f}% {moyenne_p10:>7.1f}%\n")
    print(f"\nResultats sauvegardes dans : {out_path}")


if __name__ == "__main__":
    main()