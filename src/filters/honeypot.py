def check(candidate: dict) -> tuple[bool, str]:
    profile = candidate["profile"]
    skills = candidate.get("skills", [])
    career = candidate.get("career_history", [])
    yoe = profile.get("years_of_experience", 0)

    expert_zero = [
        s for s in skills
        if s["proficiency"] == "expert" and s.get("duration_months", 1) == 0
    ]
    if len(expert_zero) >= 2:
        return True, f"expert+0months on {len(expert_zero)} skills"

    total_months = sum(j.get("duration_months", 0) for j in career)
    if total_months > yoe * 12 * 1.6 and total_months > 36:
        return True, f"career_months={total_months} vs claimed={yoe*12:.0f}"

    n_expert = sum(1 for s in skills if s["proficiency"] == "expert")
    if n_expert >= 9:
        return True, f"{n_expert} expert skills"

    if yoe < 20:
        for job in career:
            try:
                if int(job["start_date"][:4]) < 2005:
                    return True, f"start_date {job['start_date']} too early for yoe={yoe}"
            except (ValueError, KeyError):
                pass

    for job in career:
        if job.get("is_current") and job.get("end_date") is not None:
            return True, "is_current=True but end_date set"

    return False, ""


def tag_all(candidates: list[dict]) -> set[str]:
    flagged = set()
    for c in candidates:
        hp, _ = check(c)
        if hp:
            flagged.add(c["candidate_id"])
    return flagged