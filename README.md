<div align="center">

```
██╗  ██╗██╗██████╗ ███████╗███████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗
██║  ██║██║██╔══██╗██╔════╝██╔════╝██║██╔════╝ ████╗  ██║██╔══██╗██║
███████║██║██████╔╝█████╗  ███████╗██║██║  ███╗██╔██╗ ██║███████║██║
██╔══██║██║██╔══██╗██╔══╝  ╚════██║██║██║   ██║██║╚██╗██║██╔══██║██║
██║  ██║██║██║  ██║███████╗███████║██║╚██████╔╝██║ ╚████║██║  ██║███████╗
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
```

**Intelligent Candidate Discovery & Ranking**

*INDIA RUNS Hackathon — Track 1 (Data & AI Challenge) — Redrob AI × Hack2Skill*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-10%20passed-22c55e?style=flat-square)](tests/)
[![Runtime](https://img.shields.io/badge/Runtime-~35s%20CPU-6366f1?style=flat-square)](#compute)
[![Candidates](https://img.shields.io/badge/Dataset-100K%20candidates-f59e0b?style=flat-square)](#)
[![Demo](https://img.shields.io/badge/Live%20Demo-HuggingFace%20Spaces-ff6b35?style=flat-square&logo=huggingface)](https://huggingface.co/spaces/AmareshHebbar/hiresignal)

</div>

---

## What it does

Ranks 100,000 candidate profiles against a Senior AI Engineer job description in **~35 seconds on CPU** — no GPU, no API calls, no network during ranking.

Goes well beyond keyword matching. Scores each candidate across four dimensions, detects ~85 honeypot/fraudulent profiles, and generates a specific natural-language explanation for every ranking decision.

```
$ make rank
[1/6] loading dataset/candidates.jsonl
      100,000 candidates loaded  (7.1s)
[2/6] honeypot detection
      85 flagged  (0.4s)
[3/6] scoring all candidates
      done  (10.6s)
[4/6] semantic refinement on top 500
      done  (11.0s)
[5/6] selecting top 100
[6/6] writing submission.csv
      done  (0.0s)

done  total=29.0s
  [  1] CAND_0041669  Recommendation Systems Engineer  8.0yrs
  [  2] CAND_0011687  Senior NLP Engineer  7.8yrs
  [  3] CAND_0064326  Search Engineer  7.6yrs
  [  4] CAND_0052682  NLP Engineer  6.6yrs
  [  5] CAND_0017960  Recommendation Systems Engineer  7.7yrs

$ make validate
Submission is valid.
```

---

## Demo

> **[Try it live on HuggingFace Spaces →](https://huggingface.co/spaces/AmareshHebbar/hiresignal)**

Paste any lines from `candidates.jsonl` or click **Load sample** — see ranked results in seconds.

---

## Architecture

```
                        candidates.jsonl  (100,000 profiles)
                               │
                               ▼
              ┌────────────────────────────────┐
              │      HONEYPOT DETECTION        │
              │                                │
              │  expert skill + 0 months use   │
              │  career months > 1.6× YoE      │
              │  9+ expert skills listed       │
              │  start_date before 2005        │
              │  is_current=True + end_date    │
              │                                │
              │  → 85 flagged, score = 0.001   │
              └────────────────┬───────────────┘
                               │ 99,915 clean candidates
                               ▼
        ┌──────────────────────────────────────────────┐
        │              MULTI-SIGNAL SCORING            │
        │                                              │
        │  ┌─────────────────┐  ┌──────────────────┐  │
        │  │  SKILL MATCH    │  │ CAREER TRAJECTORY │  │
        │  │    40% weight   │  │    35% weight     │  │
        │  │                 │  │                   │  │
        │  │ proficiency ×   │  │ title quality     │  │
        │  │ duration ×      │  │ company type      │  │
        │  │ endorsements ×  │  │ YoE band (6-8yr)  │  │
        │  │ assessments     │  │ prod AI evidence  │  │
        │  └─────────────────┘  │ location          │  │
        │                       └──────────────────┘  │
        │  ┌──────────────────────────────────────┐    │
        │  │      BEHAVIORAL SIGNALS  25% weight  │    │
        │  │                                      │    │
        │  │  last_active_date    response_rate   │    │
        │  │  notice_period       github_activity │    │
        │  │  profile_completeness  verifications │    │
        │  └──────────────────────────────────────┘    │
        └─────────────────────┬────────────────────────┘
                              │ sorted, top 500
                              ▼
              ┌────────────────────────────────┐
              │    SEMANTIC REFINEMENT         │
              │    paraphrase-MiniLM-L6-v2     │
              │                                │
              │  JD text → embedding           │
              │  candidate profile → embedding │
              │  cosine similarity → +20% blend│
              └────────────────┬───────────────┘
                               │ re-sorted
                               ▼
              ┌────────────────────────────────┐
              │       TOP 100 + REASONING      │
              │                                │
              │  per-candidate explanation     │
              │  references actual facts       │
              │  honest about gaps             │
              └────────────────────────────────┘
                               │
                        submission.csv
```

---

## Scoring model

| Component | Weight | What it measures |
|---|---|---|
| Skill match | 40% | JD-required skills weighted by proficiency × duration × endorsements × assessment scores |
| Career trajectory | 35% | Title quality, company type, YoE band, production AI evidence, location |
| Behavioral signals | 25% | Availability, responsiveness, engagement — treats inactivity as an availability gate |
| Semantic similarity | +20% blend | Sentence-transformer cosine sim on top-500 only — stays within 5-min budget |

### Why behavioral signals are a gate, not a bonus

The JD explicitly says:

> *"A perfect-on-paper candidate who hasn't logged in for 6 months and has a 5% recruiter response rate is, for hiring purposes, not actually available."*

So a candidate with great skills but 200+ days inactive gets significantly down-weighted — not penalized slightly.

### Why pure consulting careers get penalized

The JD explicitly names TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini as patterns they want to move away from. A candidate whose entire career is at these firms gets a `0.2` company score regardless of their skill list.

---

## Honeypot detection

The dataset contains ~85 impossible profiles designed to catch naive rankers. We detect them with five logical impossibility checks:

```python
# 1. Expert proficiency + 0 months of actual use on 2+ skills
expert_zero = [s for s in skills
               if s["proficiency"] == "expert" and s.get("duration_months", 1) == 0]
if len(expert_zero) >= 2:
    return True

# 2. Sum of career months > 1.6× claimed years_of_experience
if total_career_months > yoe * 12 * 1.6 and total_career_months > 36:
    return True

# 3. 9+ skills listed as "expert" — keyword stuffer pattern
if sum(1 for s in skills if s["proficiency"] == "expert") >= 9:
    return True

# 4. Job start_date before 2005 for someone with < 20 YoE
if yoe < 20 and any(int(job["start_date"][:4]) < 2005 for job in career):
    return True

# 5. is_current=True but end_date is set — logical contradiction
if any(j.get("is_current") and j.get("end_date") for j in career):
    return True
```

All honeypots score `0.001` and never appear in top-100. The original code had a sixth rule (`skill.duration_months > yoe * 12`) that was incorrectly flagging 9,231 legitimate candidates — caught and fixed during development.

---

## Project structure

```
hiresignal/
│
├── rank.py                     entry point (7 lines)
├── Makefile                    make rank / validate / test / setup
├── requirements.txt
├── app.py                      Gradio demo for HuggingFace Spaces
│
├── src/
│   ├── pipeline.py             orchestrates all 6 steps
│   ├── loader.py               reads candidates.jsonl line by line
│   ├── jd.py                   JD constants — skill lists, title sets, cities
│   │
│   ├── filters/
│   │   └── honeypot.py         5 impossibility checks
│   │
│   ├── scoring/
│   │   ├── skills.py           skill match scorer
│   │   └── career.py           career trajectory scorer
│   │
│   ├── signals/
│   │   └── behavioral.py       23 Redrob platform signals
│   │
│   ├── embed/
│   │   └── encoder.py          sentence-transformer on top-500
│   │
│   └── output/
│       ├── writer.py           CSV output + validation asserts
│       └── reasoning.py        per-candidate reasoning strings
│
├── scripts/
│   ├── download_model.py       one-time model download
│   └── check_output.py         inspect top-10 with full profile details
│
├── tests/
│   ├── test_honeypot.py        5 tests
│   └── test_scoring.py         5 tests
│
└── dataset/
    ├── sample_candidates.json  first 50 candidates
    ├── sample_submission.csv   format reference
    ├── validate_submission.py  official format validator
    └── candidate_schema.json   JSON schema for candidate objects
```

---

## Quickstart

```bash
git clone https://github.com/amareshhebbar/hiresignal
cd hiresignal

make setup                    
source .venv/bin/activate

make model                    
make rank                    
make validate                
make test                    
```

Manual:

```bash
python rank.py --candidates dataset/candidates.jsonl --out submission.csv
python dataset/validate_submission.py submission.csv
```

---

## Compute profile <a name="compute"></a>

```
Platform   Fedora Linux, 8-core CPU
Memory     ~2.5 GB peak
Runtime    ~29s (rule-based only) / ~35s (with cached embeddings)
Network    none during ranking
GPU        not used
```

Pre-computation (`make model`) downloads the sentence-transformer model (~90MB) once to `.model_cache/`. The ranking step itself has zero network dependency — satisfies the submission spec constraint.

---

## Tests

```bash
make test

# ===== test session starts =====
# tests/test_honeypot.py::test_clean_passes               PASSED
# tests/test_honeypot.py::test_expert_zero_months         PASSED
# tests/test_honeypot.py::test_career_months_inflated     PASSED
# tests/test_honeypot.py::test_too_many_expert_skills     PASSED
# tests/test_honeypot.py::test_is_current_with_end_date   PASSED
# tests/test_scoring.py::test_ai_engineer_scores_above_zero         PASSED
# tests/test_scoring.py::test_more_skills_scores_higher             PASSED
# tests/test_scoring.py::test_disqualifying_title_gets_very_low     PASSED
# tests/test_scoring.py::test_ideal_yoe_band_boosts_career          PASSED
# tests/test_scoring.py::test_india_location_preferred              PASSED
# ===== 10 passed in 0.07s =====
```

---

## Submission

| Field | Value |
|---|---|
| Track | Track 1 — Data & AI Challenge |
| Hackathon | INDIA RUNS — Redrob AI × Hack2Skill |
| Deadline | July 2, 2026 |
| Reproduce | `python rank.py --candidates ./dataset/candidates.jsonl --out ./submission.csv` |
| Sandbox | [huggingface.co/spaces/AmareshHebbar/hiresignal](https://huggingface.co/spaces/AmareshHebbar/hiresignal) |

---

<div align="center">

Built by [G V Amaresh](https://linkedin.com/in/gvamaresh) &nbsp;·&nbsp; [HuggingFace](https://huggingface.co/AmareshHebbar) &nbsp;·&nbsp; [LinkedIn](https://linkedin.com/in/gvamaresh)

</div>