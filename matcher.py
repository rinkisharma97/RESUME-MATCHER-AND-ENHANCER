from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .resume_parser import extract_text


def match_resumes(resume_paths, job_description):
    resumes_text = [extract_text(path) for path in resume_paths]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(resumes_text + [job_description])

    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    scores = cosine_sim.flatten()

    results = []
    for idx, path in enumerate(resume_paths):
        results.append({
            "filename": path.split("/")[-1],
            "score": round(scores[idx]*100, 2),
            "text": resumes_text[idx]
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results

