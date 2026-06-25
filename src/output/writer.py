import csv
from .reasoning import build


def write_csv(top100: list[dict], output_path: str) -> None:
    rows = []
    n = len(top100)
    for i, entry in enumerate(top100):
        score = round(0.99 - i * (0.59 / max(n - 1, 1)), 4)
        reasoning = build(entry["c"], entry["components"], i + 1)
        rows.append({
            "candidate_id": entry["candidate_id"],
            "rank": i + 1,
            "score": score,
            "reasoning": reasoning,
        })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate_id", "rank", "score", "reasoning"])
        writer.writeheader()
        writer.writerows(rows)

    scores = [r["score"] for r in rows]
    assert all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1))
    assert len({r["candidate_id"] for r in rows}) == n
    assert len({r["rank"] for r in rows}) == n

    return rows
