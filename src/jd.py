from datetime import date

TODAY = date(2026, 6, 25)

JD_TEXT = """
Senior AI Engineer role at Redrob AI.
Production experience with embeddings-based retrieval systems using sentence-transformers, BGE, E5, OpenAI embeddings.
Production experience with vector databases: FAISS, Pinecone, Weaviate, Qdrant, Milvus, Elasticsearch, OpenSearch.
Strong Python programming skills.
Designing evaluation frameworks for ranking systems: NDCG, MRR, MAP, A/B testing.
NLP and information retrieval experience.
LLM fine-tuning with LoRA, QLoRA, PEFT.
Hybrid search, dense retrieval, semantic search systems.
Shipped end-to-end ranking, recommendation, or search system to real users at scale.
5-9 years experience, ideally at product companies not consulting firms.
Located in India, preferably Pune or Noida or Delhi or Mumbai or Hyderabad or Bangalore.
"""

REQUIRED_SKILLS = {
    "sentence-transformers", "embeddings", "vector database", "vector search",
    "faiss", "pinecone", "weaviate", "qdrant", "milvus", "opensearch",
    "elasticsearch", "hybrid search", "dense retrieval", "semantic search",
    "nlp", "information retrieval", "ranking", "recommendation systems",
    "machine learning", "deep learning",
    "ndcg", "mrr", "map", "a/b testing", "evaluation framework",
    "python",
    "rag", "llm", "large language models", "fine-tuning", "fine-tuning llms",
    "lora", "qlora", "peft", "transformers",
    "bge", "e5", "openai embeddings",
}

PREFERRED_SKILLS = {
    "pytorch", "tensorflow", "hugging face", "huggingface", "xgboost",
    "learning to rank", "distributed systems", "inference optimization",
    "open-source", "fastapi", "spark", "kafka", "redis", "postgresql",
    "docker", "kubernetes", "aws", "gcp", "azure",
}

PROFICIENCY_WEIGHT = {
    "expert": 1.0,
    "advanced": 0.75,
    "intermediate": 0.5,
    "beginner": 0.2,
}

YOE_SWEET_MIN = 6.0
YOE_SWEET_MAX = 8.0
YOE_IDEAL_MIN = 5.0
YOE_IDEAL_MAX = 9.0

DISQUALIFYING_TITLES = {
    "marketing manager", "content writer", "graphic designer", "hr manager",
    "hr executive", "accountant", "sales executive", "operations manager",
    "civil engineer", "mechanical engineer", "customer support",
    "legal", "finance manager", "teacher", "professor",
}

STRONG_TITLES = {
    "ai engineer", "ml engineer", "machine learning engineer",
    "nlp engineer", "research engineer", "applied scientist",
    "data scientist", "senior engineer", "staff engineer",
    "ai researcher", "deep learning", "search engineer",
    "ranking engineer", "relevance engineer", "recommendation",
}

CONSULTING_FIRMS = {
    "tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini",
    "hcl", "tech mahindra", "mphasis", "hexaware",
}

TARGET_CITIES = {
    "noida", "pune", "delhi", "gurgaon", "gurugram",
    "mumbai", "hyderabad", "bangalore", "bengaluru",
}

PRODUCTION_AI_TERMS = {
    "embedding", "retrieval", "ranking", "vector", "rag", "recommendation",
    "nlp", "search", "llm", "fine-tun", "transformer", "bert", "gpt",
    "faiss", "pinecone", "qdrant", "semantic", "inference", "deployed",
    "production", "a/b test", "evaluation",
}
