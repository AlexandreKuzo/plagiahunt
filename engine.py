import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer # Permet de calculer la fréquence d'apparition de mots proportionnellement au nombre de documents comparés 
from sklearn.metrics.pairwise import cosine_similarity # On importe le comparateur cosine similarity

sample_files = [doc for doc in os.listdir(sys.argv[1]) if doc .endswith("."+sys.argv[2])] # On indique l'extension des documents comparés et le dossier dans lequel on va chercher
sample_contents = [open(sys.argv[1]+'/'+file).read() for file in sample_files] # on créé une boucle pour lire chaque documents

# La fréquence d'apparition des mots est passée en argument Text ; argument converti en tableau ensuite.
vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray() 

# Comparaison entre un doc 1 et un doc 2 avec cosine
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2]) 

vectors = vectorize(sample_contents) # on applique la méthode vectorize sur le contenu des documents 
s_vectors = list(zip(sample_files, vectors)) # on créé un tuple avec les documents et les vecteurs respectifs

def check_plagiarism():
    results = set()
    global s_vectors # on créé une variable globale s_vectors
    for sample_a, text_vector_a in s_vectors:
        # fonction récursive pour créer les comparaisons entre documents, avec une boucle
        new_vectors = s_vectors.copy() # on "reproduit" s_vectors
        current_index = new_vectors.index((sample_a, text_vector_a)) # on identifie le rang avant de le retirer
        del new_vectors[current_index]
        for sample_b, text_vector_b in new_vectors: # on remplace le vecteur effacé par le nouveau vecteur pour la comparaison
            sim_score = similarity(text_vector_a, text_vector_b)[0][1] # on applique le résultat du calcul
            sample_pair = sorted((sample_a, sample_b))
            score = sample_pair[0], sample_pair[1], sim_score
            results.add(score)
    return results


for data in check_plagiarism():
    print(data)
