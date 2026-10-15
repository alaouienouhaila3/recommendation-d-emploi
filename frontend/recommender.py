from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculer_scores(profil: dict, offres: list) -> list:
    """
    Calcule le score de matching entre le profil candidat
    et chaque offre JSearch.

    Args:
        profil (dict): {
            "competences": "python django sql",
            "experience": "2 ans backend",
            "formation": "master informatique"
        }
        offres (list): liste d'offres retournées par jsearch.py

    Returns:
        list: Top-10 offres triées par score décroissant
    """

    # 1. Construire le texte du profil candidat
    texte_profil = (
        f"{profil.get('competences', '')} "
        f"{profil.get('experience', '')} "
        f"{profil.get('formation', '')}"
    )

    # 2. Construire le texte de chaque offre JSearch
    textes_offres = []
    for offre in offres:
        texte = (
            f"{offre.get('job_title', '')} "
            f"{offre.get('job_description', '')} "
            f"{offre.get('employer_name', '')}"
        )
        textes_offres.append(texte)

    # 3. Si aucune offre → retourner liste vide
    if not textes_offres:
        return []

    # 4. TF-IDF : vectoriser le profil + toutes les offres
    tous_les_textes = [texte_profil] + textes_offres
    vectorizer = TfidfVectorizer(stop_words="english")
    matrice = vectorizer.fit_transform(tous_les_textes)

    # 5. Calculer la similarité cosinus
    # entre le profil (index 0) et chaque offre
    vecteur_profil = matrice[0]
    vecteurs_offres = matrice[1:]
    scores = cosine_similarity(vecteur_profil, vecteurs_offres)[0]

    # 6. Ajouter le score à chaque offre
    for i, offre in enumerate(offres):
        offre["score_matching"] = round(float(scores[i]) * 100, 1)

    # 7. Trier par score décroissant → Top-10
    offres_triees = sorted(
        offres,
        key=lambda x: x["score_matching"],
        reverse=True
    )
    return offres_triees[:10]