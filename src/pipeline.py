import time

from src.loader import load
from src.filters import tag_all
from src.scoring import score_skills, score_career
from src.signals import score_behavioral
from src.embed import refine_scores
from src.output import write_csv


def run(candidates_path: str, output_path: str) -> None:
    t0 = time.time()

    print(f"[1/6] loading {candidates_path}")
    candidates = load(candidates_path)
    print(f"      {len(candidates):,} candidates loaded  ({time.time()-t0:.1f}s)")

    t = time.time()
    print(f"[2/6] honeypot detection")
    honeypots = tag_all(candidates)
    print(f"      {len(honeypots)} flagged  ({time.time()-t:.1f}s)")

    t = time.time()
    print(f"[3/6] scoring all candidates")
    scored = []
    for c in candidates:
        cid = c["candidate_id"]
        if cid in honeypots:
            scored.append({"candidate_id": cid, "score": 0.001, "is_honeypot": True, "c": c, "components": {}})
            continue
        ss, sd = score_skills(c)
        cs, cd = score_career(c)
        bs, bd = score_behavioral(c)
        pre = ss * 0.40 + cs * 0.35 + bs * 0.25
        scored.append({
            "candidate_id": cid,
            "score": pre,
            "is_honeypot": False,
            "c": c,
            "components": {
                "skill_score": ss,
                "career_score": cs,
                "behavioral_score": bs,
                "skill_debug": sd,
                "career_debug": cd,
                "behavioral_debug": bd,
            },
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    print(f"      done  ({time.time()-t:.1f}s)")

    t = time.time()
    valid = [s for s in scored if not s["is_honeypot"]]
    top_n = min(100, len(valid))
    top_for_embed = valid[:min(500, len(valid))]
    print(f"[4/6] semantic refinement on top {len(top_for_embed)}")
    refine_scores(top_for_embed)
    scored.sort(key=lambda x: x["score"], reverse=True)
    print(f"      done  ({time.time()-t:.1f}s)")

    print(f"[5/6] selecting top {top_n}")
    valid = [s for s in scored if not s["is_honeypot"]]
    top_candidates = valid[:top_n]

    t = time.time()
    print(f"[6/6] writing {output_path}")
    write_csv(top_candidates, output_path)
    print(f"      done  ({time.time()-t:.1f}s)")

    print(f"\ndone  total={time.time()-t0:.1f}s")
    for entry in top_candidates[:5]:
        print(f"  [{top_candidates.index(entry)+1:3d}] {entry['candidate_id']}  {entry['c']['profile']['current_title']}  {entry['c']['profile']['years_of_experience']}yrs")
