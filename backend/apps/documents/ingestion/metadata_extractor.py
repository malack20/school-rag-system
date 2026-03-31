import re

SECTION_KEYS = {
    "eligibility": ["eligibility", "qualified", "qualification", "eligible"],
    "required_documents": ["required documents", "documents required", "attachments", "supporting documents", "requirements"],
    "specifications": ["specifications", "technical", "scope", "statement of work"],
    "deadlines": ["deadline", "closing", "due date", "submission deadline"],
    "submission": ["submit", "submission", "portal", "address", "delivery"],
    "contacts": ["contact", "email", "phone", "office", "helpdesk"],
}

def classify_section(text: str) -> str:
    t = (text or "").lower()
    for sec, keys in SECTION_KEYS.items():
        for k in keys:
            if k in t:
                return sec
    return "general"

def extract_sections(text: str) -> dict:
    t = text or ""
    lines = [l.strip() for l in t.splitlines()]
    buckets = {k: [] for k in SECTION_KEYS.keys()}
    buckets["general"] = []
    current = "general"
    for l in lines:
        if not l:
            continue
        sec = classify_section(l)
        if sec != "general":
            current = sec
        buckets[current].append(l)
    # collapse to concise items
    for k in buckets:
        buckets[k] = [x for x in buckets[k] if len(x) > 3][:50]
    return buckets
