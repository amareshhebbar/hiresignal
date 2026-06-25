# Video Description

## Title
HireSignal — AI Candidate Ranking for Redrob | INDIA RUNS Hackathon Track 1

## Short description (for YouTube / Loom)

Built a candidate ranking system for the Redrob AI hackathon that ranks 100,000 candidates against a Senior AI Engineer JD in ~35 seconds on CPU.

The system uses four components: skill match weighted by proficiency and duration, career trajectory analysis (title quality, company type, production AI evidence), behavioral signals from the Redrob platform (response rate, activity recency, notice period), and semantic embeddings on the top-500 to refine the ranking.

It also detects the ~80 honeypot candidates the organizers put in the dataset — profiles with impossible experience timelines, expert skills with zero months of use, and other inconsistencies.

GitHub: https://github.com/amareshhebbar/hiresignal

---

## Long description (for submission portal / HuggingFace Spaces)

This is my submission for INDIA RUNS Hackathon Track 1 (Data & AI Challenge) by Redrob AI × Hack2Skill.

**The problem:** rank 100,000 candidate profiles for a Senior AI Engineer role, going beyond keyword filters to find candidates who actually fit — by experience, skills, company background, and genuine availability.

**What I built:**

The ranker has four components. Skill scoring weights each skill by proficiency level, how many months the candidate has actually used it, endorsements received, and any Redrob platform assessment scores — so a candidate who lists "FAISS" as a 2-month beginner skill ranks much lower than one who's used it for 3 years at advanced level.

Career scoring looks at the title (Marketing Managers with AI keywords don't pass), company type (the JD explicitly says pure consulting careers are a bad fit), years of experience against the JD's 5-9 year band, evidence in role descriptions of actually shipping retrieval/ranking systems, and location.

Behavioral signals are treated as an availability gate, not just a quality signal. The Redrob platform tracks 23 signals per candidate — last active date, recruiter response rate, notice period, GitHub activity, applications in the last 30 days, and more. A candidate who hasn't logged in for 6 months gets significantly down-weighted even if their skills are perfect.

For the top-500 candidates after rule-based scoring, I run a sentence-transformer (paraphrase-MiniLM-L6-v2) to compute semantic similarity between the JD and each candidate's profile text. This is blended in at 20% weight and runs on CPU in about a minute.

The dataset has ~80 honeypot candidates — profiles that look good on paper but have subtle impossibilities (expert proficiency with 0 months of use, career history that exceeds claimed years of experience by 60%+, etc.). These get detected and scored near zero.

Total runtime: ~35s without embeddings, ~90s with the cached model. No network calls during ranking.

**Stack:** Python, sentence-transformers, FAISS (for the embedding cache), numpy. No external LLM APIs.

Repo: https://github.com/amareshhebbar/hiresignal

---

## Timestamps (fill in after recording)

0:00 — intro and problem statement
0:45 — architecture walkthrough
2:00 — live demo: running rank.py on the 100K dataset
3:15 — top-10 results inspection
4:00 — honeypot detection explanation
4:45 — code walkthrough: scoring modules
6:00 — behavioral signals deep dive
7:00 — closing
