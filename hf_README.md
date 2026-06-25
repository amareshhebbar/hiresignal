---
title: HireSignal
emoji: 🎯
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
license: mit
short_description: Rank candidates against the Redrob AI Senior Engineer JD
---

# HireSignal

Candidate ranking system built for the **INDIA RUNS Hackathon Track 1** by Redrob AI × Hack2Skill.

Paste up to 50 lines of JSONL from `candidates.jsonl` — or click **Load sample** — and the ranker scores and ranks them against the Senior AI Engineer JD in seconds.

## How it works

**Skill match (40%)** — each skill is weighted by proficiency level, months of use, endorsements, and platform assessment scores.

**Career trajectory (35%)** — title quality, company type (consulting firms penalized per JD), YoE band (sweet spot 6-8 years), production AI evidence in role descriptions, location.

**Behavioral signals (25%)** — last active date, recruiter response rate, notice period, GitHub activity. Inactive candidates are down-weighted even with perfect skills.

**Semantic similarity (+20% blend on top-500)** — `paraphrase-MiniLM-L6-v2` cosine similarity between JD text and candidate profile.

Honeypot detection flags ~85 impossible profiles before scoring.

## GitHub

[github.com/amareshhebbar/hiresignal](https://github.com/amareshhebbar/hiresignal)