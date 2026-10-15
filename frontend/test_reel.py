from jsearch import fetch_jobs
from recommender import calculer_scores

# Profil réel
profil = {
    "competences": "python django sql",
    "experience": "1 an",
    "formation": "master informatique"
}

# Récupérer vraies offres JSearch
print("Fetching jobs from JSearch...")
offres = fetch_jobs(query="python developer", location="Morocco", num_pages=1)

print(f"Offres récupérées : {len(offres)}")

# Calculer les scores
resultats = calculer_scores(profil, offres)

# Afficher le Top-10
print("\n=== Top 10 Recommandations ===")
for offre in resultats:
    print(f"{offre['score_matching']}% — {offre['job_title']} chez {offre['employer_name']}")