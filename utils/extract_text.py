from langchain_community.document_loaders import PyPDFLoader


def _clean(text):
  
    text = text.replace("\x00", "")
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned_lines = []
    blank_run = 0
    for line in lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run > 1:
                continue
        else:
            blank_run = 0
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


def extract_text(pdf_path):
 
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    pages_text = []
    for i, doc in enumerate(docs):
        pages_text.append(f"--- Page {i + 1} ---\n{_clean(doc.page_content)}")

    return "\n\n".join(pages_text)
