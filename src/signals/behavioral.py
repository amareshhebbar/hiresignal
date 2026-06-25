from datetime import datetime
from src.jd import TODAY


def run(candidate: dict) -> tuple[float, dict]:
    sig = candidate.get("redrob_signals", {})

    open_to_work = sig.get("open_to_work_flag", False)

    try:
        last_active = datetime.strptime(sig.get("last_active_date", "2020-01-01"), "%Y-%m-%d").date()
        days_since = (TODAY - last_active).days
    except (ValueError, TypeError):
        days_since = 365

    if days_since <= 30:
        recency = 1.0
    elif days_since <= 90:
        recency = 0.7
    elif days_since <= 180:
        recency = 0.4
    else:
        recency = 0.15

    availability = 0.5 * recency + 0.5 * (1.0 if open_to_work else 0.1)

    response_rate = sig.get("recruiter_response_rate", 0.0)
    avg_rt = sig.get("avg_response_time_hours", 999)

    if avg_rt < 4:
        rt_score = 1.0
    elif avg_rt < 24:
        rt_score = 0.8
    elif avg_rt < 72:
        rt_score = 0.6
    else:
        rt_score = 0.3

    responsiveness = 0.6 * response_rate + 0.4 * rt_score

    notice = sig.get("notice_period_days", 90)
    if notice <= 30:
        notice_score = 1.0
    elif notice <= 60:
        notice_score = 0.7
    elif notice <= 90:
        notice_score = 0.5
    else:
        notice_score = 0.3

    completeness = sig.get("profile_completeness_score", 50) / 100.0
    verification = (
        0.4 * int(sig.get("verified_email", False)) +
        0.3 * int(sig.get("verified_phone", False)) +
        0.3 * int(sig.get("linkedin_connected", False))
    )
    apps = min(1.0, sig.get("applications_submitted_30d", 0) / 5.0)
    saved = min(1.0, sig.get("saved_by_recruiters_30d", 0) / 5.0)
    interview_completion = sig.get("interview_completion_rate", 0.5)

    engagement = (
        completeness         * 0.25 +
        verification         * 0.20 +
        apps                 * 0.20 +
        saved                * 0.15 +
        interview_completion * 0.20
    )

    raw_github = sig.get("github_activity_score", -1)
    github = 0.3 if raw_github == -1 else raw_github / 100.0

    final = (
        availability  * 0.30 +
        responsiveness * 0.25 +
        notice_score   * 0.15 +
        engagement     * 0.20 +
        github         * 0.10
    )

    return min(1.0, final), {
        "days_since_active": days_since,
        "open_to_work": open_to_work,
        "response_rate": round(response_rate, 2),
        "notice_days": notice,
        "github_score": round(github, 2),
    }
