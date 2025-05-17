import re 
from typing import Dict, Any, List  
from dataclasses import dataclass 

@dataclass 
class ProcessedEmail:
    """Container for preprocessed email data"""
    subject: str 
    body: str 
    clean_text: str   # Combined and cleaned version for classification 
    metadata: Dict[str, Any]   # Store any extracted metadata 
    paragraphs: List[str]  # Store individual paragraphs

def preprocess_email(email_text: str) -> ProcessedEmail:
    """
    Preprocess email text to make it suitable for classification.
    Handles multi-line text and preserves paragraph structure.

    Args:
        email_text: Raw email text which may include subject, signatures, etc.

    Returns:
        ProcessedEmail object with cleaned text and extracted metadata 
    
    """
    # Initialize metadata dictionary 
    metadata = {
        "has_attachments": False,
        "has_numbered_list": False,
        "has_bullet_list": False,
        "urgent_indicators": False,
        "potential_entities": [],
        "line_count": 0,
        "paragraph_count": 0
    }

    # Normalize line endings (in case of mixed line endings)
    email_text = email_text.replace('\r\n', '\n').replace('\r', '\n')

    # Check if email is already in a standard format or needs parsing 
    email_text = email_text.strip()

    # Count lines before any processing
    lines = email_text.split('\n')
    metadata["line_count"] = len(lines)

    # Extract subject if present (looks for "Subject:" at the beginning of a line)
    subject_match = re.search(r"(?:^|\n)Subject:[ \t]*(.*?)(?:\n|$)", email_text, re.IGNORECASE | re.DOTALL)

    if subject_match:
        # Get the entire subject, which might span multiple lines until the next empty line
        subject_text = subject_match.group(1)

        # Clean up multi-line subject (replace newlines with spaces)
        subject = re.sub(r'\s+', ' ', subject_text.strip())

        # Remove subject line from the email body
        email_text = re.sub(r"(?:^|\n)Subject:.*?(?=\n\n|\n[A-Za-z]|\Z)", "", 
                           email_text, flags=re.IGNORECASE | re.DOTALL, count=1)
        
    else:
        subject = ""

    # Handle email forwarding and reply headers
    email_text = re.sub(r"(?:^|\n)[-]+\s*Forwarded.*?[-]+(?:\n|$)", "\n", 
                       email_text, flags=re.IGNORECASE | re.DOTALL)
    email_text = re.sub(r"(?:^|\n)[-]+\s*Original Message.*?[-]+(?:\n|$)", "\n", 
                       email_text, flags=re.IGNORECASE | re.DOTALL)
    email_text = re.sub(r"(?:^|\n)From:.*?(?:\n|$)", "\n", email_text, flags=re.IGNORECASE)
    email_text = re.sub(r"(?:^|\n)Sent:.*?(?:\n|$)", "\n", email_text, flags=re.IGNORECASE)
    email_text = re.sub(r"(?:^|\n)To:.*?(?:\n|$)", "\n", email_text, flags=re.IGNORECASE)
    email_text = re.sub(r"(?:^|\n)Cc:.*?(?:\n|$)", "\n", email_text, flags=re.IGNORECASE)

    # Extract the body (everything after any headers and before any signatures)
    body = email_text 

    # Remove email signatures (common patterns)
    # More comprehensive signature detection
    signature_patterns = [
        r"\n-{2,}.*?$",             # Remove "---" and everything after
        r"\nRegards,.*?$",          # Remove "Regards," and everything after
        r"\nThanks,.*?$",           # Remove "Thanks," and everything after
        r"\nThank you,.*?$",        # Remove "Thank you," and everything after
        r"\nBest,.*?$",             # Remove "Best," and everything after
        r"\nBest regards,.*?$",     # Remove "Best regards," and everything after
        r"\nSincerely,.*?$",        # Remove "Sincerely," and everything after
        r"\nCheers,.*?$",           # Remove "Cheers," and everything after
        r"\n--\s*\n.*?$"            # Common signature separator
    ]

    for pattern in signature_patterns:
        body = re.sub(pattern, "", body, flags=re.DOTALL)

    # Remove email signatures (common patterns)
    body = re.sub(r"\n-{2,}.*?$", "", body, flags=re.DOTALL)  # Remove "---" and everything after
    body = re.sub(r"\nRegards,.*?$", "", body, flags=re.DOTALL)  # Remove "Regards," and everything after
    body = re.sub(r"\nThanks,.*?$", "", body, flags=re.DOTALL)  # Remove "Thanks," and everything after
    body = re.sub(r"\nBest,.*?$", "", body, flags=re.DOTALL)  # Remove "Best," and everything after

    # Handle HTML content
    # Remove simple HTML tags (preserving content between them)
    body = re.sub(r'<(?!\/?(b|i|u|strong|em)>)[^>]*>', ' ', body)  # Replace tags with space
    body = re.sub(r'<\/?(?:b|i|u|strong|em)>', '', body)  # Remove formatting tags but keep content
    
    # Convert HTML entities
    body = re.sub(r'&nbsp;', ' ', body)
    body = re.sub(r'&lt;', '<', body)
    body = re.sub(r'&gt;', '>', body)
    body = re.sub(r'&amp;', '&', body)
    body = re.sub(r'&quot;', '"', body)

    # Check for attachments mentioned
    if re.search(r"\b(?:attach|attached|attachment|enclosed|pdf|doc|file)\b", body, re.IGNORECASE):
        metadata["has_attachments"] = True

    # Check for urgency indicators
    if re.search(r"\b(?:urgent|asap|immediately|time-sensitive|deadline|critical|today)\b", 
                body + " " + subject, re.IGNORECASE):
        metadata["urgent_indicators"] = True

    # Check for numbered lists (potential multi-intent indicator)
    if re.search(r"\n\s*\d+\.\s", body):
        metadata["has_numbered_list"] = True

    # detection for numbered lists (potential multi-intent indicator)
    # Look for patterns like "1.", "2.", "1)", "2)", etc.
    numbered_list_pattern = r"(?:^|\n)\s*(?:\d+[\.\)]) .+"
    if re.search(numbered_list_pattern, body, re.MULTILINE):
        metadata["has_numbered_list"] = True

        # Extract numbered list items
        numbered_items = re.findall(numbered_list_pattern, body, re.MULTILINE)
        metadata["numbered_items_count"] = len(numbered_items)

        # Store first few items for reference
        if numbered_items:
            metadata["numbered_items_sample"] = numbered_items[:3]

    # Detect bullet lists
    bullet_list_pattern = r"(?:^|\n)\s*(?:[\•\-\*\+]) .+"
    if re.search(bullet_list_pattern, body, re.MULTILINE):
        metadata["has_bullet_list"] = True

    # Extract potential entities (companies, properties)
    # Improved patterns for property and company detection
    property_patterns = [
        r"\b[A-Z][a-zA-Z\s\-']*(Building|Property|Tower|Plaza|Avenue|Street|St\.|Ave\.|Heights|Lofts|Office|Space|Retail|Complex|Center|Mall|Suites|Park|Campus)\b",
        r"\b\d+\s+[A-Z][a-zA-Z\s\-']*(Street|St\.|Avenue|Ave\.|Road|Rd\.|Boulevard|Blvd\.|Lane|Ln\.|Drive|Dr\.|Place|Pl\.)\b"
    ]
    
    company_patterns = [
        r"\b[A-Z][a-zA-Z\s\-&']*(LLC|Inc\.|Corp|Corporation|Holdings|Properties|Group|Partners|Trust|Associates|Company|Co\.|Ltd\.)\b",
        r"\b[A-Z][a-zA-Z\s\-&']*(?:Real Estate|Investments|Development|Management)\b"
    ]

    # Apply all patterns
    potential_entities = []
    for pattern in property_patterns:
        matches = re.findall(pattern, body, re.IGNORECASE)
        potential_entities.extend(matches)
    
    for pattern in company_patterns:
        matches = re.findall(pattern, body, re.IGNORECASE)
        potential_entities.extend(matches)

    # Clean up entities
    cleaned_entities = []
    for entity in potential_entities:
        # Remove leading/trailing whitespace and normalize internal spaces
        clean_entity = re.sub(r'\s+', ' ', entity.strip())
        if clean_entity:
            cleaned_entities.append(clean_entity)
    
    metadata["potential_entities"] = list(set(cleaned_entities))
    
    # Break the body into paragraphs (for better structure preservation)
    # A paragraph is defined as text separated by one or more blank lines
    paragraphs = re.split(r'\n\s*\n', body)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    metadata["paragraph_count"] = len(paragraphs)
    
    # Combine subject and body for classification, preserving paragraph structure
    if subject:
        clean_paragraphs = [f"Subject: {subject}"] + paragraphs
    else:
        clean_paragraphs = paragraphs
    
    # Create clean text while preserving paragraph structure
    clean_text = "\n\n".join(clean_paragraphs)
    
    # Normalize whitespace within paragraphs but preserve paragraph breaks
    clean_text = re.sub(r'[ \t]+', ' ', clean_text)  # Replace multiple spaces/tabs with single space
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)  # Replace 3+ newlines with double newline
    clean_text = clean_text.strip()
    
    return ProcessedEmail(
        subject=subject,
        body=body,
        clean_text=clean_text,
        metadata=metadata,
        paragraphs=paragraphs
    )


# Test function
if __name__ == "__main__":
    test_email = """Subject: Multiple Action Items – Urgent Review Needed
Hi team,

We have a few high-priority tasks that need immediate attention:

1. The lease amendment for the Jackson Heights retail space just came in (attached). Please abstract it and identify any changes from the original lease, especially around rent escalations and renewal clauses.
2. For the Riverfront Lofts acquisition, I need a complete schedule of critical dates (inspection period, loan contingency, and closing) by tomorrow morning. The seller is requesting to move up the closing date.
3. Someone from legal should review the draft lease for the 5th Avenue office. It's missing indemnity protections, and the assignment clause seems overly broad—please flag any red flags.
Also, loop in research to run a background check on "Evergreen Property Holdings"—we need to understand their portfolio, principals, and whether they've been involved in any litigation in the past five years.
Let me know who's taking the lead on each item.
Thanks,
Morgan"""
    
    processed = preprocess_email(test_email)
    print(f"Subject: {processed.subject}")
    print(f"Metadata: {processed.metadata}")
    print(f"Clean text for classification:\n{processed.clean_text}")


