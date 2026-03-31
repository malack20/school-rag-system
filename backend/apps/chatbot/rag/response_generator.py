import os
from apps.documents.models import Document

def _openai_generate(prompt: str) -> str:
    try:
        use_openai = os.getenv("USE_OPENAI", "0") == "1"
        api_key = os.getenv("OPENAI_API_KEY")
        if not use_openai or not api_key:
            return ""
        try:
            from openai import OpenAI
            timeout = int(os.getenv("OPENAI_TIMEOUT", "10"))
            client = OpenAI(api_key=api_key, timeout=timeout)
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for a school knowledge base."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )
            return resp.choices[0].message.content or ""
        except Exception:
            return ""
    except Exception:
        return ""

def _extract_question(prompt: str) -> str:
    try:
        q = prompt.split("Question:\n", 1)[1]
        q = q.split("\nAnswer", 1)[0]
        return q.strip()
    except Exception:
        return ""

def _heuristic_answer(prompt: str) -> str:
    q = _extract_question(prompt).lower()
    docs = Document.objects.all()[:20]
    def find_specific_sections(keywords, max_sections=10):
        res = []
        for d in docs:
            t = (d.text or "").lower()
            if any(k in t for k in keywords):
                # Split into paragraphs and find relevant ones
                parts = [p.strip() for p in (d.text or "").split("\n\n") if p.strip()]
                for part in parts:
                    part_lower = part.lower()
                    if any(k in part_lower for k in keywords):
                        res.append(part[:500])  # Limit length
                        if len(res) >= max_sections:
                            break
                if len(res) >= max_sections:
                    break
        return res

    def extract_details(category_keywords, detail_keywords):
        details = {}
        for cat in category_keywords:
            sections = find_specific_sections([cat])
            for section in sections:
                section_lower = section.lower()
                for detail in detail_keywords:
                    if detail in section_lower:
                        if cat not in details:
                            details[cat] = []
                        # Extract sentences containing the detail
                        sentences = [s.strip() for s in section.split('.') if detail in s.lower()]
                        details[cat].extend(sentences[:3])  # Up to 3 sentences per category
        return details

    if any(k in q for k in ["tender", "procurement", "bid", "rfp"]):
        # Define categories and their detail keywords
        categories = {
            "Eligibility": ["eligibility", "qualifications", "requirements"],
            "Required Documents": ["required documents", "documents needed", "submission documents"],
            "Deadlines": ["deadline", "submission date", "closing date", "due date"],
            "Format": ["format", "submission format", "how to submit", "application format"],
            "Portal/Office": ["portal", "office", "submit to", "submission address"],
            "Evaluation": ["evaluation", "compliance", "criteria"],
            "Contact": ["contact", "procurement office", "clarifications"]
        }
        
        details = extract_details(categories.keys(), [item for sublist in categories.values() for item in sublist])
        
        response = "Detailed Tender Guidance:\n\n"
        for cat, info in categories.items():
            response += f"**{cat}:**\n"
            if cat in details and details[cat]:
                for item in details[cat][:3]:  # Limit to 3 items per category
                    response += f"• {item}\n"
            else:
                # Fallback generic
                if cat == "Eligibility":
                    response += "• Check eligibility criteria in the tender document.\n"
                elif cat == "Required Documents":
                    response += "• Refer to the tender notice for required documents.\n"
                elif cat == "Deadlines":
                    response += "• Note the submission deadline specified in the tender.\n"
                elif cat == "Format":
                    response += "• Follow the specified submission format.\n"
                elif cat == "Portal/Office":
                    response += "• Submit to the designated portal or office.\n"
                elif cat == "Evaluation":
                    response += "• Ensure compliance with evaluation criteria.\n"
                elif cat == "Contact":
                    response += "• Contact the procurement office for clarifications.\n"
            response += "\n"
        
        # Add general sections from docs
        general_sections = find_specific_sections(["tender", "procurement", "bid", "rfp"])
        if general_sections:
            response += "**Additional Information from Documents:**\n"
            for sec in general_sections[:3]:
                response += f"• {sec[:300]}...\n"
        
        return response

    # Similar for admission and fees, but simplified for now
    if any(k in q for k in ["admission", "enroll", "apply"]):
        categories = {
            "Eligibility": ["eligibility", "requirements"],
            "Required Documents": ["required documents", "credentials"],
            "Deadlines": ["deadline", "application date"],
            "Process": ["how to apply", "steps"],
            "Fees": ["fee", "payment"],
            "Contact": ["contact", "admissions office"]
        }
        details = extract_details(categories.keys(), [item for sublist in categories.values() for item in sublist])
        
        response = "Detailed Admission Guidance:\n\n"
        for cat, info in categories.items():
            response += f"**{cat}:**\n"
            if cat in details and details[cat]:
                for item in details[cat][:3]:
                    response += f"• {item}\n"
            else:
                response += f"• Refer to the admission policy for {cat.lower()}.\n"
            response += "\n"
        
        general_sections = find_specific_sections(["admission", "apply", "enroll"])
        if general_sections:
            response += "**Additional Information:**\n"
            for sec in general_sections[:3]:
                response += f"• {sec[:300]}...\n"
        
        return response

    if any(k in q for k in ["fee", "tuition", "payment"]):
        categories = {
            "Fee Structure": ["fee structure", "breakdown", "amounts"],
            "Due Dates": ["due date", "payment date", "deadline"],
            "Payment Methods": ["payment method", "how to pay", "channels"],
            "Receipts": ["receipt", "confirmation"],
            "Contact": ["contact", "finance office"]
        }
        details = extract_details(categories.keys(), [item for sublist in categories.values() for item in sublist])
        
        response = "Detailed Fee Guidance:\n\n"
        for cat, info in categories.items():
            response += f"**{cat}:**\n"
            if cat in details and details[cat]:
                for item in details[cat][:3]:
                    response += f"• {item}\n"
            else:
                response += f"• Refer to the fee policy for {cat.lower()}.\n"
            response += "\n"
        
        general_sections = find_specific_sections(["fee", "tuition", "payment"])
        if general_sections:
            response += "**Additional Information:**\n"
            for sec in general_sections[:3]:
                response += f"• {sec[:300]}...\n"
        
        return response

    return "A detailed answer is unavailable. Please refine your question or check the relevant policy documents."

def _context_fallback(prompt: str) -> str:
    # If OpenAI isn't available, return relevant text excerpts from the retrieved context.
    if "Context:" in prompt:
        try:
            context = prompt.split("Context:\n", 1)[1].split("\nQuestion:", 1)[0].strip()
            if context:
                return (
                    "Here are the most relevant excerpts from the documents (based on your question):\n\n"
                    + context
                )
        except Exception:
            pass
    # Default heuristic fallback (still uses document contents when possible)
    return _heuristic_answer(prompt)


def generate_answer(prompt: str) -> str:
    answer = _openai_generate(prompt)
    if answer:
        return answer
    return _context_fallback(prompt)
