import re
from pypdf import PdfReader

def extract_profile_from_cv(pdf_path: str) -> str:
    """
    Extrait le texte d'un fichier PDF (CV).
    
    Args:
        pdf_path (str): Chemin vers le fichier PDF
    
    Returns:
        str: Texte extrait et nettoyé
    """
    try:
        reader = PdfReader(pdf_path)
        texte = ""

        # Extraire le texte de chaque page
        for page in reader.pages:
            texte += page.extract_text() or ""

        # Nettoyer le texte
        texte = re.sub(r'\s+', ' ', texte)       # espaces multiples
        texte = re.sub(r'[^\w\s\-\+\#\.]', ' ', texte)  # caractères spéciaux
        texte = texte.strip()

        print(f"✅ Texte extrait : {len(texte)} caractères")
        return texte

    except Exception as e:
        print(f"❌ Erreur extraction PDF : {e}")
        return ""