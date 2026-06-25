import gradio as gr
import json
import csv
import io
import tempfile
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src import run as rank_pipeline
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False


def rank_candidates(jsonl_text: str):
    if not jsonl_text.strip():
        return _build_html([], error="Paste at least one candidate line to rank.")

    lines = [l.strip() for l in jsonl_text.strip().splitlines() if l.strip()]

    if len(lines) > 50:
        return _build_html([], error=f"Max 50 candidates per run. You pasted {len(lines)} lines.")

    try:
        candidates = [json.loads(l) for l in lines]
    except json.JSONDecodeError as e:
        return _build_html([], error=f"Invalid JSON on one of the lines: {e}")

    if not PIPELINE_AVAILABLE:
        return _build_html([], error="Pipeline not available — check that src/ is in the same directory as app.py.")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        for c in candidates:
            f.write(json.dumps(c) + "\n")
        inp = f.name

    out = inp.replace(".jsonl", "_out.csv")

    try:
        rank_pipeline(inp, out)
        rows = []
        with open(out, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        return _build_html(rows)
    except Exception as e:
        return _build_html([], error=str(e))
    finally:
        if os.path.exists(inp):
            os.unlink(inp)
        if os.path.exists(out):
            os.unlink(out)


def _score_color(score: float) -> str:
    if score >= 0.80:
        return "#10B981"
    if score >= 0.60:
        return "#6366F1"
    if score >= 0.40:
        return "#F59E0B"
    return "#EF4444"


def _build_html(rows: list, error: str = "") -> str:
    if error:
        return f"""
<div style="padding:24px 0;font-family:'Inter',system-ui,sans-serif;">
  <div style="display:flex;align-items:center;gap:10px;padding:16px 20px;background:#1a0a0a;border:1px solid #3f1a1a;border-radius:10px;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
    <span style="color:#EF4444;font-size:14px;">{error}</span>
  </div>
</div>"""

    if not rows:
        return ""

    top = rows[:100]
    cards = ""
    for r in top:
        rank = int(r.get("rank", 0))
        cid = r.get("candidate_id", "")
        score = float(r.get("score", 0))
        reasoning = r.get("reasoning", "")
        pct = round(score * 100, 1)
        color = _score_color(score)
        bar_w = round(score * 100)

        rank_badge = ""
        if rank == 1:
            rank_badge = f'<span style="font-size:11px;font-weight:600;color:#F59E0B;background:#2a1f00;padding:2px 8px;border-radius:4px;margin-left:8px;">RANK 1</span>'
        elif rank <= 3:
            rank_badge = f'<span style="font-size:11px;font-weight:600;color:#A78BFA;background:#180e2a;padding:2px 8px;border-radius:4px;margin-left:8px;">TOP 3</span>'
        elif rank <= 10:
            rank_badge = f'<span style="font-size:11px;color:#6B7280;background:#111827;padding:2px 8px;border-radius:4px;margin-left:8px;">TOP 10</span>'

        cards += f"""
<div class="card" style="background:#0f1623;border:1px solid #1e2a3a;border-radius:12px;padding:18px 20px;margin-bottom:10px;transition:border-color 0.2s;" onmouseover="this.style.borderColor='#374151'" onmouseout="this.style.borderColor='#1e2a3a'">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
    <div style="display:flex;align-items:center;gap:10px;">
      <span style="font-size:13px;color:#4B5563;font-family:'JetBrains Mono','Courier New',monospace;min-width:28px;">#{rank}</span>
      <span style="font-size:14px;font-weight:600;color:#F9FAFB;font-family:'JetBrains Mono','Courier New',monospace;">{cid}</span>
      {rank_badge}
    </div>
    <span style="font-size:22px;font-weight:700;color:{color};font-variant-numeric:tabular-nums;">{pct}%</span>
  </div>
  <div style="background:#080d14;border-radius:4px;height:4px;margin-bottom:14px;overflow:hidden;">
    <div style="height:4px;border-radius:4px;background:{color};width:{bar_w}%;transition:width 0.6s ease;"></div>
  </div>
  <p style="margin:0;font-size:13px;color:#9CA3AF;line-height:1.6;">{reasoning}</p>
</div>"""

    total = len(rows)
    return f"""
<div style="font-family:'Inter',system-ui,sans-serif;padding:4px 0 24px;">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
    <div>
      <span style="font-size:13px;color:#6B7280;">Showing </span>
      <span style="font-size:13px;font-weight:600;color:#F9FAFB;">{total}</span>
      <span style="font-size:13px;color:#6B7280;"> ranked candidates</span>
    </div>
    <div style="display:flex;align-items:center;gap:16px;font-size:12px;">
      <span style="color:#10B981;">● ≥80%</span>
      <span style="color:#6366F1;">● ≥60%</span>
      <span style="color:#F59E0B;">● ≥40%</span>
      <span style="color:#EF4444;">● &lt;40%</span>
    </div>
  </div>
  {cards}
</div>"""


SAMPLE_JSONL = ""


def _load_sample():
    sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "sample_candidates.json")
    if not os.path.exists(sample_path):
        return ""
    try:
        with open(sample_path, encoding="utf-8") as f:
            data = json.load(f)
        subset = data[:5] if isinstance(data, list) else []
        return "\n".join(json.dumps(c) for c in subset)
    except Exception:
        return ""


SAMPLE_JSONL = _load_sample()

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

body, .gradio-container {
    background: #060a13 !important;
    color: #F9FAFB !important;
}

.gradio-container {
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 0 24px !important;
}

#header {
    padding: 40px 0 32px;
    border-bottom: 1px solid #1e2a3a;
    margin-bottom: 32px;
}

#header h1 {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 28px;
    font-weight: 600;
    color: #F9FAFB;
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}

#header p {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 14px;
    color: #6B7280;
    margin: 0;
}

#header .badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 600;
    color: #818CF8;
    background: #1a1a2e;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid #2a2a4a;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.gr-form, form {
    background: transparent !important;
    border: none !important;
    gap: 0 !important;
}

label.svelte-1b6s6vi, .svelte-1b6s6vi label {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #4B5563 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 8px !important;
}

textarea, .gr-text-input {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    font-size: 12px !important;
    background: #0a1020 !important;
    border: 1px solid #1e2a3a !important;
    border-radius: 10px !important;
    color: #D1D5DB !important;
    padding: 14px !important;
    line-height: 1.7 !important;
    resize: vertical !important;
    transition: border-color 0.2s !important;
}

textarea:focus {
    border-color: #6366F1 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

button.primary {
    font-family: 'Inter', system-ui, sans-serif !important;
    background: #6366F1 !important;
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    cursor: pointer !important;
    transition: background 0.2s, transform 0.1s !important;
    letter-spacing: 0.2px !important;
}

button.primary:hover {
    background: #5558E3 !important;
}

button.primary:active {
    transform: scale(0.98) !important;
}

button.secondary {
    font-family: 'Inter', system-ui, sans-serif !important;
    background: transparent !important;
    border: 1px solid #1e2a3a !important;
    border-radius: 8px !important;
    color: #6B7280 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 18px !important;
    cursor: pointer !important;
    transition: border-color 0.2s, color 0.2s !important;
}

button.secondary:hover {
    border-color: #374151 !important;
    color: #9CA3AF !important;
}

.output-html {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

.gr-panel, .panel {
    background: transparent !important;
    border: none !important;
}

footer {
    display: none !important;
}

.stats-bar {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}

.stat {
    flex: 1;
    background: #0a1020;
    border: 1px solid #1e2a3a;
    border-radius: 10px;
    padding: 14px 16px;
}

.stat-label {
    font-size: 11px;
    color: #4B5563;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
    margin-bottom: 4px;
}

.stat-value {
    font-size: 22px;
    font-weight: 600;
    color: #F9FAFB;
    font-variant-numeric: tabular-nums;
}
"""

HEADER_HTML = """
<div id="header">
  <div class="badge">
    <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
      <circle cx="5" cy="5" r="4" fill="#818CF8"/>
    </svg>
    India RUNS · Track 1 · Redrob AI
  </div>
  <h1>HireSignal</h1>
  <p>Rank candidates against the Senior AI Engineer JD. Paste up to 50 lines of JSONL from candidates.jsonl.</p>
</div>
"""

with gr.Blocks(title="HireSignal") as demo:
    gr.HTML(HEADER_HTML)

    with gr.Row(equal_height=False):
        with gr.Column(scale=5):
            jsonl_input = gr.Textbox(
                label="CANDIDATE JSONL",
                placeholder='{"candidate_id":"CAND_0000001","profile":{...},...}\n{"candidate_id":"CAND_0000002",...}',
                lines=22,
                max_lines=30,
            )
            with gr.Row():
                run_btn = gr.Button("Run ranking", variant="primary")
                sample_btn = gr.Button("Load sample", variant="secondary")

        with gr.Column(scale=7):
            output = gr.HTML(label="RESULTS")

    run_btn.click(fn=rank_candidates, inputs=jsonl_input, outputs=output)
    sample_btn.click(fn=lambda: SAMPLE_JSONL, inputs=[], outputs=jsonl_input)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, css=CSS)