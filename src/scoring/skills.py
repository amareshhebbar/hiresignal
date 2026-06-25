from src.jd import REQUIRED_SKILLS, PREFERRED_SKILLS, PROFICIENCY_WEIGHT


def normalize(name: str) -> str:
    return name.lower().strip().replace("-", " ").replace("_", " ")


def run(candidate: dict) -> tuple[float, dict]:
    skills = candidate.get("skills", [])
    assessments = candidate.get("redrob_signals", {}).get("skill_assessment_scores", {})

    required_hits = 0.0
    preferred_hits = 0.0
    matched_required = []
    matched_preferred = []

    for skill in skills:
        raw = skill["name"]
        norm = normalize(raw)
        prof_w = PROFICIENCY_WEIGHT.get(skill.get("proficiency", "beginner"), 0.2)
        dur = skill.get("duration_months", 0)
        endorsements = skill.get("endorsements", 0)

        dur_factor = min(1.0, 0.5 + dur / 48.0)
        endorse_factor = min(1.2, 1.0 + endorsements / 100.0)

        if raw in assessments:
            effective = 0.6 * (assessments[raw] / 100.0) + 0.4 * prof_w
        else:
            effective = prof_w

        combined = effective * dur_factor * endorse_factor

        is_req = any(req in norm or norm in req for req in REQUIRED_SKILLS)
        is_pref = any(p in norm or norm in p for p in PREFERRED_SKILLS)

        if is_req:
            required_hits += combined
            matched_required.append(raw)
        elif is_pref:
            preferred_hits += combined * 0.5
            matched_preferred.append(raw)

    req_coverage = min(1.0, required_hits / 6.0)
    pref_coverage = min(0.3, preferred_hits / 5.0) * 0.3
    final = req_coverage * 0.85 + pref_coverage * 0.15

    return min(1.0, final), {
        "matched_required": matched_required[:5],
        "matched_preferred": matched_preferred[:3],
        "required_coverage": round(req_coverage, 3),
    }
