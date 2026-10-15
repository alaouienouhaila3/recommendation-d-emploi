from recommender import calculer_scores

# Profil fictif du candidat
profil = {
    "competences": "python django rest api sql postgresql",
    "experience": "2 ans développeur backend",
    "formation": "master informatique"
}

# Offres fictives (simulant JSearch)
offres = [
    {
        "job_title": "Python Django Developer",
        "job_description": "We need a python developer with django rest api and sql skills",
        "employer_name": "TechCorp"
    },
    {
        "job_title": "Java Spring Developer",
        "job_description": "Java spring boot microservices developer needed",
        "employer_name": "JavaCorp"
    },
    {
        "job_title": "Data Scientist Python",
        "job_description": "Python machine learning pandas numpy scikit-learn sql",
        "employer_name": "DataCorp"
    },
    {
        "job_title": "Frontend React Developer",
        "job_description": "React javascript html css frontend developer",
        "employer_name": "WebCorp"
    }
]

# Lancer le test
resultats = calculer_scores(profil, offres)

print("=== Résultats de matching ===")
for offre in resultats:
    print(f"{offre['score_matching']}% — {offre['job_title']} chez {offre['employer_name']}")