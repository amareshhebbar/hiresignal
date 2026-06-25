from src.filters.honeypot import check


def _make(yoe=6.0, skills=None, career=None):
    return {
        "candidate_id": "CAND_0000001",
        "profile": {"years_of_experience": yoe},
        "skills": skills or [],
        "career_history": career or [
            {"company": "A", "title": "SWE", "start_date": "2018-01-01",
             "end_date": None, "duration_months": int(yoe * 12),
             "is_current": True, "industry": "Tech", "company_size": "51-200",
             "description": "built stuff"}
        ],
    }


def test_clean_passes():
    c = _make()
    hp, _ = check(c)
    assert not hp


def test_expert_zero_months():
    skills = [{"name": "Python", "proficiency": "expert", "duration_months": 0, "endorsements": 0},
              {"name": "Go", "proficiency": "expert", "duration_months": 0, "endorsements": 0}]
    hp, reason = check(_make(skills=skills))
    assert hp
    assert "expert" in reason


def test_career_months_inflated():
    career = [
        {"company": "A", "title": "SWE", "start_date": "2018-01-01",
         "end_date": None, "duration_months": 200, "is_current": True,
         "industry": "Tech", "company_size": "51-200", "description": ""},
    ]
    hp, reason = check(_make(yoe=3.0, career=career))
    assert hp


def test_too_many_expert_skills():
    skills = [
        {"name": f"Skill{i}", "proficiency": "expert", "duration_months": 12, "endorsements": 5}
        for i in range(10)
    ]
    hp, reason = check(_make(skills=skills))
    assert hp


def test_is_current_with_end_date():
    career = [
        {"company": "A", "title": "SWE", "start_date": "2020-01-01",
         "end_date": "2023-01-01", "duration_months": 36, "is_current": True,
         "industry": "Tech", "company_size": "51-200", "description": ""},
    ]
    hp, reason = check(_make(career=career))
    assert hp
