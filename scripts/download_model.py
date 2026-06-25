#!/usr/bin/env python3
import os
from sentence_transformers import SentenceTransformer

CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".model_cache")

print(f"downloading model to {CACHE}")
model = SentenceTransformer("paraphrase-MiniLM-L6-v2", cache_folder=CACHE)
test = model.encode(["test"], convert_to_numpy=True)
print(f"ok  dim={test.shape[1]}")
print(f"\nnow run:  make rank")
