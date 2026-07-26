import re
import logging

def extract_ratings(pdf_path: str) -> dict:
    data = {
        "nominal_voltage": "",
        "v_max": "",
        "v_min": "",
        "rated_capacity": "",
        "grading_low": "",
        "grading_high": "",
        "format_from_datasheet": "",
        "manufacturer_from_datasheet": "",
        "storage_from_datasheet": "",
        "supplied_as_from_datasheet": "",
        "datasheet_title": "",
        "cell_model": "",
        "chemistry": ""
    }
    
    full_text_lines = []
    
    # Try native Apple Vision OCR first for high resolution text extraction
    try:
        import fitz
        import Vision
        from Cocoa import NSData, CIImage
        
        doc = fitz.open(pdf_path)
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            ns_data = NSData.dataWithBytes_length_(img_bytes, len(img_bytes))
            ci_img = CIImage.imageWithData_(ns_data)
            
            handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(ci_img, None)
            request = Vision.VNRecognizeTextRequest.alloc().init()
            request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
            
            handler.performRequests_error_([request], None)
            results = request.results()
            if results:
                for obs in results:
                    full_text_lines.append(obs.topCandidates_(1)[0].string().strip())
    except Exception as e:
        logging.warning(f"Vision OCR unavailable: {e}. Falling back to pdfplumber...")

    # Fallback to pdfplumber if text extraction lines are empty
    if not full_text_lines:
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text() or ""
                    full_text_lines.extend([line.strip() for line in t.split("\n") if line.strip()])
        except Exception as e:
            logging.error(f"pdfplumber extraction failed: {e}")

    text_full = "\n".join(full_text_lines)
    
    # Extract manufacturer
    m_mfg = re.search(r"Manufactured by:\s*([^.\n]+)", text_full)
    if m_mfg:
        data["manufacturer_from_datasheet"] = m_mfg.group(1).strip()
        
    # Extract cell model, format, and chemistry
    m_model = re.search(r"Model\s+([A-Z0-9-]+)\s*\(([^,]+),\s*([^)]+)\)", text_full)
    if m_model:
        data["cell_model"] = m_model.group(1).strip()
        data["format_from_datasheet"] = m_model.group(2).strip()
        data["chemistry"] = m_model.group(3).strip()
    else:
        m_model_only = re.search(r"Model\s+([A-Z0-9-]+)", text_full)
        if m_model_only:
            data["cell_model"] = m_model_only.group(1).strip()
            
    if data["manufacturer_from_datasheet"] and data["cell_model"]:
        data["datasheet_title"] = f"{data['manufacturer_from_datasheet']} datasheet — {data['cell_model']}"
        
    # Extract supplied as packaging info
    m_sup = re.search(r"((?:Supplied|Delivered|Provided) as[^.\n]+)", text_full)
    if m_sup:
        sup_str = m_sup.group(1).strip()
        if not sup_str.endswith("."): sup_str += "."
        data["supplied_as_from_datasheet"] = sup_str
        
    # Extract storage condition
    m_stor = re.search(r"((?:Store at|Storage condition:|Keep at)[^.\n]+)", text_full)
    if m_stor:
        stor_str = m_stor.group(1).strip()
        if not stor_str.endswith("."): stor_str += "."
        data["storage_from_datasheet"] = stor_str
        
    # Extract electrical ratings table values
    for idx, line in enumerate(full_text_lines):
        if line == "Value" and idx + 4 < len(full_text_lines):
            v1, v2, v3, v4 = full_text_lines[idx+1], full_text_lines[idx+2], full_text_lines[idx+3], full_text_lines[idx+4]
            if "V" in v1: data["nominal_voltage"] = v1
            if "V" in v2: data["v_max"] = v2
            if "V" in v3: data["v_min"] = v3
            if "Ah" in v4: data["rated_capacity"] = v4
            
    # Fallbacks for plain text datasheets
    if not data["nominal_voltage"]:
        m = re.search(r"Nominal voltage\s*(\d+\.?\d*)\s*V", text_full, re.IGNORECASE)
        if m: data["nominal_voltage"] = f"{m.group(1)} V"
    if not data["v_max"]:
        m = re.search(r"Charge voltage\s*(?:\([^)]*\))?\s*(\d+\.?\d*)\s*V", text_full, re.IGNORECASE)
        if m: data["v_max"] = f"{m.group(1)} V"
    if not data["v_min"]:
        m = re.search(r"Discharge cut-off\s*(?:\([^)]*\))?\s*(\d+\.?\d*)\s*V", text_full, re.IGNORECASE)
        if m: data["v_min"] = f"{m.group(1)} V"
    if not data["rated_capacity"]:
        m = re.search(r"Rated capacity\s*(\d+\.?\d*)\s*Ah", text_full, re.IGNORECASE)
        if m: data["rated_capacity"] = f"{m.group(1)} Ah"
            
    # Extract low and high capacity grading bounds
    for idx, line in enumerate(full_text_lines):
        if "Capacity band (Ah)" in line or "Capacity band" in line:
            for j in range(idx + 1, min(idx + 12, len(full_text_lines))):
                cleaned = full_text_lines[j].replace(".", "")
                if cleaned.isdigit():
                    if not data["grading_low"]:
                        data["grading_low"] = f"{full_text_lines[j]} Ah"
                    elif not data["grading_high"]:
                        data["grading_high"] = f"{full_text_lines[j]} Ah"
                        break
                        
    return data
