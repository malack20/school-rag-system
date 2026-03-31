def _truncate(s, limit=3000):
    if len(s) <= limit:
        return s
    return s[:limit]

def build_prompt(query, chunks):
    context = "\n".join(chunks[:3])
    context = _truncate(context, 3000)
    return f"Answer the question using the context.\nContext:\n{context}\nQuestion:\n{query}\nAnswer:"

def build_analysis_prompt(text):
    return (
        "You are an assistant reviewing a school document.\n"
        "Provide a concise analysis with:\n"
        "- Summary (3-5 bullets)\n"
        "- Key sections detected\n"
        "- Potential gaps or issues\n"
        "- Suggestions for improvement\n\n"
        "Document Content:\n"
        f"{text}\n\n"
        "Structured Feedback:"
    )
