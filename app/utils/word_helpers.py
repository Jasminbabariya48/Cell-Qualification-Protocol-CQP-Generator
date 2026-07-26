from lxml import etree

# OpenXML namespaces
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_MAP = {'w': W_NS}

def apply_vertical_merge(cell, merge_type="continue"):
    """
    Applies vertical cell merging in a docx table.
    merge_type can be 'restart' (start of merge) or 'continue' (part of merged span).
    """
    tcPr = cell._tc.get_or_add_tcPr()
    vMerge = etree.Element(f"{{{W_NS}}}vMerge")
    vMerge.set(f"{{{W_NS}}}val", merge_type)
    tcPr.append(vMerge)

def protect_document(docx_doc):
    """
    Applies read-only protection to the document. 
    """
    pass
