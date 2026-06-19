from langchain_community.document_loaders import PyPDFLoader


def _clean(text):
    """
    Some PDFs (e.g. thermal-camera export tools) embed fonts that make
    PyPDF extract text with stray NUL bytes between characters, like
    "\\x002\\x008\\x00.\\x008 °C" instead of "28.8 °C". Strip those out,
    and collapse the resulting whitespace mess.
    """
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
    """
    Extracts text from a PDF and returns a single clean string with
    page markers (so it's safe to drop straight into an LLM prompt,
    and so other modules can locate content by page number).
    """
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    pages_text = []
    for i, doc in enumerate(docs):
        pages_text.append(f"--- Page {i + 1} ---\n{_clean(doc.page_content)}")

    return "\n\n".join(pages_text)
