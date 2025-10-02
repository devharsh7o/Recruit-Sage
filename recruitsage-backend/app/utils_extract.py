from pathlib import Path

def extract_text_from_pdf(path: Path) -> str:
    try:
        from pdfminer.high_level import extract_text
        return extract_text(str(path)) or ""
    except Exception:
        return ""

def extract_text_from_docx(path: Path) -> str:
    try:
        import docx
        doc = docx.Document(str(path))
        return "\n".join([p.text for p in doc.paragraphs if p.text]) or ""
    except Exception:
        return ""

def extract_text(path: Path, content_type: str) -> str:
    if content_type == "application/pdf":
        return extract_text_from_pdf(path)
    if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(path)
    # For .doc or unknown types, skip for now
    return ""
