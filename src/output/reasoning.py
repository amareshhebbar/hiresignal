from datetime import datetime
from src.jd import TODAY


def build(candidate: dict, components: dict, rank: int) -> str:
    p = candidate["profile"]
    sig = candidate.get("redrob_signals", {})

    yoe = p.get("years_of_experience", 0)
    title = p.get("current_title", "")
    location = p.get("location", "")
    country = p.get("country", "")
    response_rate = sig.get("recruiter_response_rate", 0)
    notice = sig.get("notice_period_days", 90)
    open_to_work = sig.get("open_to_work_flag", False)

    try:
        last_active = datetime.strptime(sig.get("last_active_date", "2020-01-01"), "%Y-%m-%d").date()
        days_since = (TODAY - last_active).days
    except Exception:
        days_since = 999

    skill_debug = components.get("skill_debug", {})
    career_debug = components.get("career_debug", {})
    matched_req = skill_debug.get("matched_required", [])

    positives = []
    concerns = []

    if matched_req:
        positives.append(f"{len(matched_req)} JD-required skills ({', '.join(matched_req[:3])})")
    if career_debug.get("production_ai_score", 0) >= 0.6:
        positives.append("strong production AI signals in career history")
    if response_rate >= 0.7:
        positives.append(f"high recruiter response rate ({response_rate:.0%})")
    if notice <= 30:
        positives.append(f"sub-30-day notice ({notice}d)")
    if open_to_work:
        positives.append("actively open to work")
    if days_since <= 30:
        positives.append(f"active in last {days_since} days")
    if sig.get("github_activity_score", -1) >= 60:
        positives.append(f"strong GitHub activity ({sig['github_activity_score']:.0f}/100)")

    if not matched_req:
        concerns.append("no JD core skills matched")
    if days_since > 90:
        concerns.append(f"last active {days_since} days ago")
    if 0 <= response_rate < 0.3:
        concerns.append(f"low recruiter response rate ({response_rate:.0%})")
    if notice > 90:
        concerns.append(f"long notice period ({notice}d)")
    if career_debug.get("company_type") == "pure_consulting":
        concerns.append("entire career at consulting firms")
    if country.lower() != "india":
        concerns.append(f"based in {country}, not India")
    if yoe < 5:
        concerns.append(f"only {yoe:.1f}yrs experience (JD needs 5-9)")

    pos_str = "; ".join(positives[:3]) if positives else "limited JD alignment"
    concern_str = "; ".join(concerns[:2]) if concerns else ""

    loc_str = f"{location}, {country}" if country.lower() != "india" else location
    text = f"{title} with {yoe:.1f}yrs ({loc_str}): {pos_str}."
    if concern_str:
        text += f" Concerns: {concern_str}."

    return text[:300]
