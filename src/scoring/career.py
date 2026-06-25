from src.jd import (
    YOE_SWEET_MIN, YOE_SWEET_MAX, YOE_IDEAL_MIN, YOE_IDEAL_MAX,
    DISQUALIFYING_TITLES, STRONG_TITLES, CONSULTING_FIRMS,
    TARGET_CITIES, PRODUCTION_AI_TERMS,
)


def run(candidate: dict) -> tuple[float, dict]:
    profile = candidate["profile"]
    career = candidate.get("career_history", [])
    yoe = profile.get("years_of_experience", 0.0)
    signals = candidate.get("redrob_signals", {})

    if YOE_SWEET_MIN <= yoe <= YOE_SWEET_MAX:
        yoe_score = 1.0
    elif YOE_IDEAL_MIN <= yoe <= YOE_IDEAL_MAX:
        yoe_score = 0.8
    elif 3.0 <= yoe < YOE_IDEAL_MIN:
        yoe_score = 0.5
    elif yoe > YOE_IDEAL_MAX:
        yoe_score = max(0.4, 1.0 - (yoe - YOE_IDEAL_MAX) * 0.08)
    else:
        yoe_score = 0.2

    title_lower = profile.get("current_title", "").lower()
    headline_lower = profile.get("headline", "").lower()

    if any(kw in title_lower for kw in DISQUALIFYING_TITLES):
        title_score = 0.05
    elif any(kw in title_lower for kw in STRONG_TITLES):
        title_score = 1.0
    elif any(kw in headline_lower for kw in STRONG_TITLES):
        title_score = 0.7
    elif "engineer" in title_lower or "developer" in title_lower:
        title_score = 0.5
    elif "scientist" in title_lower or "analyst" in title_lower:
        title_score = 0.4
    else:
        title_score = 0.2

    companies_lower = [j["company"].lower() for j in career]
    industries = [j.get("industry", "").lower() for j in career]

    all_consulting = (
        len(companies_lower) > 0 and
        all(any(f in co for f in CONSULTING_FIRMS) for co in companies_lower)
    )

    if all_consulting:
        company_score = 0.2
        company_type = "pure_consulting"
    else:
        has_small = any(
            j.get("company_size", "") in ["11-50", "51-200", "201-500"]
            for j in career
        )
        has_tech = any(
            any(w in ind for w in ["ai", "tech", "saas", "software"])
            for ind in industries
        )
        company_score = 0.6 + (0.2 if has_small else 0) + (0.2 if has_tech else 0)
        company_type = "product_or_mixed"

    prod_score = 0.0
    for job in career:
        desc = job.get("description", "").lower()
        hits = sum(1 for kw in PRODUCTION_AI_TERMS if kw in desc)
        weight = 1.5 if job.get("is_current") else 1.0
        prod_score += min(1.0, hits / 4.0) * weight
    prod_score = min(1.0, prod_score / 2.0)

    location = profile.get("location", "").lower()
    country = profile.get("country", "").lower()
    relocate = signals.get("willing_to_relocate", False)

    if country == "india" and any(city in location for city in TARGET_CITIES):
        location_score = 1.0
    elif country == "india":
        location_score = 0.7 if relocate else 0.5
    else:
        location_score = 0.3 if relocate else 0.1

    final = (
        yoe_score     * 0.25 +
        title_score   * 0.30 +
        company_score * 0.15 +
        prod_score    * 0.20 +
        location_score * 0.10
    )

    return min(1.0, final), {
        "yoe": round(yoe, 1),
        "yoe_score": round(yoe_score, 2),
        "title_score": round(title_score, 2),
        "company_type": company_type,
        "company_score": round(company_score, 2),
        "production_ai_score": round(prod_score, 2),
        "location_score": round(location_score, 2),
    }
