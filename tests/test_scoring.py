from src.scoring.skills import run as score_skills
from src.scoring.career import run as score_career


def _candidate(title="ML Engineer", yoe=7.0, country="India", location="Bangalore", skills=None):
    return {
        "candidate_id": "CAND_0000001",
        "profile": {
            "current_title": title,
            "headline": f"{title} at AI startup",
            "summary": "built retrieval systems",
            "years_of_experience": yoe,
            "location": location,
            "country": country,
        },
        "career_history": [
            {"company": "AI Corp", "title": title, "start_date": "2018-01-01",
             "end_date": None, "duration_months": int(yoe * 12), "is_current": True,
             "industry": "AI/ML", "company_size": "51-200",
             "description": "built embedding retrieval ranking nlp systems in production"}
        ],
        "skills": skills or [
            {"name": "FAISS", "proficiency": "advanced", "duration_months": 24, "endorsements": 20},
            {"name": "Python", "proficiency": "expert", "duration_months": 60, "endorsements": 50},
            {"name": "NLP", "proficiency": "advanced", "duration_months": 36, "endorsements": 30},
        ],
        "redrob_signals": {
            "willing_to_relocate": True,
            "skill_assessment_scores": {},
        },
    }


def test_ai_engineer_scores_above_zero():
    c = _candidate()
    score, _ = score_skills(c)
    assert score > 0.3


def test_more_skills_scores_higher():
    c_few = _candidate(skills=[
        {"name": "FAISS", "proficiency": "advanced", "duration_months": 24, "endorsements": 20},
    ])
    c_many = _candidate(skills=[
        {"name": "FAISS", "proficiency": "expert", "duration_months": 48, "endorsements": 40},
        {"name": "Python", "proficiency": "expert", "duration_months": 60, "endorsements": 50},
        {"name": "NLP", "proficiency": "expert", "duration_months": 36, "endorsements": 30},
        {"name": "Pinecone", "proficiency": "advanced", "duration_months": 24, "endorsements": 15},
        {"name": "Weaviate", "proficiency": "advanced", "duration_months": 18, "endorsements": 10},
        {"name": "Qdrant", "proficiency": "advanced", "duration_months": 12, "endorsements": 8},
    ])
    s_few, _ = score_skills(c_few)
    s_many, _ = score_skills(c_many)
    assert s_many > s_few


def test_disqualifying_title_gets_very_low_title_score():
    c = _candidate(title="Marketing Manager")
    _, debug = score_career(c)
    assert debug["title_score"] <= 0.05


def test_ideal_yoe_band_boosts_career():
    c_good = _candidate(yoe=7.0)
    c_low = _candidate(yoe=2.0)
    s_good, _ = score_career(c_good)
    s_low, _ = score_career(c_low)
    assert s_good > s_low


def test_india_location_preferred():
    c_india = _candidate(location="Bangalore", country="India")
    c_abroad = _candidate(location="Toronto", country="Canada")
    s_india, _ = score_career(c_india)
    s_abroad, _ = score_career(c_abroad)
    assert s_india > s_abroad
