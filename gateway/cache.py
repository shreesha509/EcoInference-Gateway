import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.92

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = PROJECT_ROOT / "data" / "sample_cache.json"

_model = SentenceTransformer(MODEL_NAME)


def load_cache() -> list[dict]:
    """Load cached prompts and metadata from the local JSON file."""

    if not CACHE_FILE.exists():
        return []

    with open(CACHE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def find_similar_prompt(prompt: str) -> dict:
    """
    Compare the incoming prompt against cached prompts.

    Returns a cache HIT when cosine similarity >= threshold.
    Otherwise returns a cache MISS.
    """

    cache = load_cache()

    if not cache:
        return {
            "cache_hit": False,
            "similarity": 0.0,
            "matched_prompt": None,
            "asset": None,
        }

    query_embedding = _model.encode([prompt])

    best_match = None
    best_similarity = -1.0

    for item in cache:
        cached_embedding = item["embedding"]

        similarity = cosine_similarity(
            query_embedding,
            [cached_embedding],
        )[0][0]

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = item

    cache_hit = best_similarity >= SIMILARITY_THRESHOLD

    return {
        "cache_hit": cache_hit,
        "similarity": round(float(best_similarity), 4),
        "matched_prompt": (
            best_match["prompt"] if cache_hit else None
        ),
        "asset": best_match["asset"] if cache_hit else None,
    }