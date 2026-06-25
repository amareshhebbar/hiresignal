import os
import numpy as np
from src.jd import JD_TEXT, PROFICIENCY_WEIGHT

MODEL_NAME = "paraphrase-MiniLM-L6-v2"
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".model_cache")


def _build_text(candidate: dict) -> str:
    p = candidate["profile"]
    parts = [
        p.get("headline", ""),
        p.get("summary", ""),
        p.get("current_title", ""),
    ]
    for job in candidate.get("career_history", [])[:2]:
        parts.append(job.get("description", ""))
    skills_text = " ".join(
        s["name"] for s in sorted(
            candidate.get("skills", []),
            key=lambda x: PROFICIENCY_WEIGHT.get(x["proficiency"], 0),
            reverse=True,
        )[:15]
    )
    parts.append(skills_text)
    return " ".join(filter(None, parts))[:1000]


def refine_scores(scored_batch: list[dict]) -> None:
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(MODEL_NAME, cache_folder=CACHE_DIR)

        jd_vec = model.encode([JD_TEXT], convert_to_numpy=True, show_progress_bar=False)[0]
        jd_norm = jd_vec / (np.linalg.norm(jd_vec) + 1e-9)

        texts = [_build_text(s["c"]) for s in scored_batch]
        vecs = model.encode(texts, convert_to_numpy=True, show_progress_bar=False, batch_size=64)

        for i, s in enumerate(scored_batch):
            v = vecs[i] / (np.linalg.norm(vecs[i]) + 1e-9)
            sim = float(np.dot(jd_norm, v))
            sem = (sim + 1) / 2.0
            s["score"] = s["score"] * 0.80 + sem * 0.20
            s["components"]["semantic_score"] = round(sem, 3)

    except Exception as e:
        print(f"      embed step skipped: {e}")
