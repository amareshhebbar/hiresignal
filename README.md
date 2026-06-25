# hiresignal

Candidate ranking system for the Redrob AI hackathon (INDIA RUNS, Track 1).

Ranks 100K candidates against a Senior AI Engineer JD using skill match, career trajectory, behavioral signals from the Redrob platform, and semantic embeddings. Runs in ~35 seconds on CPU with no network calls.

---

## Setup

```bash
git clone https://github.com/amareshhebbar/hiresignal
cd hiresignal

make setup
source .venv/bin/activate

make model        # one-time: downloads ~90MB model to .model_cache/
```

---

## Run

```bash
make rank CANDIDATES=./candidates.jsonl OUT=./submission.csv
make validate
```

Or directly:

```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
python validate_submission.py submission.csv
```

---

## How it works

Four scoring components, each explained below.

**Skill match (40%)**

Checks each candidate's skills against what the JD actually needs: vector DBs (FAISS, Pinecone, Qdrant, Weaviate, etc.), embeddings, NLP, retrieval, LLM fine-tuning, Python. Each skill is weighted by proficiency level, how many months they've actually used it, endorsements, and any platform assessment scores. Not a keyword count — a weighted credibility score.

**Career trajectory (35%)**

Looks at title, company type, years of experience, production AI evidence in role descriptions, and location. The JD explicitly rules out pure consulting careers (TCS, Infosys, Wipro, etc.) and non-AI titles, so those get penalized here. The sweet spot is 6-8 years at a product company with evidence of actually shipping AI systems. Titles like "Marketing Manager" or "Civil Engineer" with AI keywords in their skills list don't pass this.

**Behavioral signals (25%)**

The Redrob platform gives 23 signals per candidate — last active date, recruiter response rate, notice period, GitHub activity, application activity, etc. The JD specifically says a perfect-on-paper candidate who hasn't logged in for 6 months is "not actually available." This component treats inactivity as a hard downweight, not just a soft penalty.

**Semantic similarity (top-500 only, +20% blend)**

After the first three components narrow the field to a top-500, we run a sentence-transformer model (paraphrase-MiniLM-L6-v2) to compute cosine similarity between the JD text and each candidate's headline + summary + career descriptions. This catches good fits that the rule-based scoring might have slightly underweighted. Only runs on top-500 to stay within the 5-minute budget.

**Honeypot detection**

The dataset has ~80 impossible profiles: expert proficiency with 0 months of use, career duration that exceeds claimed years of experience by 60%+, 9+ expert skills (keyword stuffer pattern), jobs that started before 2005 for candidates with <20 years experience, `is_current=True` with an `end_date` set. All of these get score 0.001 and never appear in the top 100.

---

## Project layout

```
hiresignal/
├── rank.py                        entry point
├── Makefile
├── requirements.txt
├── validate_submission.py         provided by organizers
├── submission_metadata.yaml
│
├── hiresignal/
│   ├── pipeline.py                orchestrates all steps
│   ├── loader.py                  reads candidates.jsonl
│   ├── jd.py                      JD constants and skill lists
│   │
│   ├── filters/
│   │   └── honeypot.py            impossible profile detection
│   │
│   ├── scoring/
│   │   ├── skills.py              skill match scorer
│   │   └── career.py              career trajectory scorer
│   │
│   ├── signals/
│   │   └── behavioral.py          redrob platform signal scorer
│   │
│   ├── embed/
│   │   └── encoder.py             sentence-transformer refinement
│   │
│   └── output/
│       ├── writer.py              CSV output
│       └── reasoning.py           per-candidate reasoning strings
│
├── scripts/
│   ├── download_model.py          pre-computation step
│   └── check_output.py            inspect top-10 with profile details
│
└── tests/
    ├── test_honeypot.py
    └── test_scoring.py
```

---

## Compute profile

| | |
|---|---|
| Runtime | ~35s (no embeddings) / ~90s (with cached model) |
| Memory | ~2.5 GB peak |
| Network | none during ranking |
| GPU | not used |

Pre-computation (`make model`) downloads ~90MB once and caches it locally. The ranking step itself has no network dependency.

---

## Constraints compliance

The submission spec requires: ≤5 min, ≤16GB RAM, CPU only, no network calls during ranking. All four are satisfied. The reproduce command is:

```
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

---

## Tests

```bash
make test
```
