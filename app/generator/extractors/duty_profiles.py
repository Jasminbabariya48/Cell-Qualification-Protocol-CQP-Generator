import re

def extract_profiles_from_docx(doc):
    # Scan ACL document paragraphs to extract duty profile names and C-rates
    profiles = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if "Duty Profile:" in text or "Duty Profile " in text:
            name_part = text
            if ":" in text:
                name_part = text.split(":", 1)[1].strip()
                
            rates = []
            name = name_part
            
            m_rates = re.search(r"\((.*?rates.*?)\)", text, re.IGNORECASE)
            if m_rates:
                rates_str = m_rates.group(1)
                name = name_part.split("(")[0].strip()
                rates = re.findall(r"\d+\.?\d*C", rates_str)
                if not rates:
                    if ":" in rates_str:
                        rates = [r.strip() for r in rates_str.split(":")[1].split(",")]
                        
            profiles.append({"name": name, "rates": rates})
            
    return profiles
