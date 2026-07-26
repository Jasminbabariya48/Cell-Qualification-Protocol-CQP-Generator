def extract_footnotes(doc):
    # Extract footnote lines at bottom of ACL document
    footnotes = []
    in_notes = False
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
            
        if text.lower() == "notes:" or text.lower() == "notes":
            in_notes = True
            continue
            
        if in_notes:
            footnotes.append(text)
            
    return footnotes
