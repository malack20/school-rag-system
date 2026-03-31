from apps.chatbot.rag.response_generator import generate_answer
from apps.chatbot.rag.prompt_template import build_analysis_prompt

def _truncate(text: str, limit: int = 8000) -> str:
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit]

def _heuristic_feedback(text: str) -> str:
    t = (text or "")[:2000]
    lines = [l.strip() for l in t.splitlines() if l.strip()]
    keys = []
    for k in ["admission", "fee", "policy", "schedule", "map", "procurement", "handbook", "regulation"]:
        if k in t.lower():
            keys.append(k)
    summary = "• " + "\n• ".join(lines[:5])
    detected = ", ".join(keys) if keys else "general information"
    return (
        "Summary:\n"
        f"{summary}\n\n"
        f"Key sections detected: {detected}\n"
        "Potential gaps: Requires deeper review for completeness and dates.\n"
        "Suggestions: Add clear headings, dates, contacts, and quick reference links."
    )

def analyze_text(text: str) -> str:
    truncated = _truncate(text or "")
    prompt = build_analysis_prompt(truncated)
    ans = generate_answer(prompt)
    if ans:
        return ans
    return _heuristic_feedback(text or "")
