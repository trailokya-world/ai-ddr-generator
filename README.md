# AI DDR Generator

An AI-powered Detailed Diagnostic Report (DDR) generation system that analyzes Property Inspection Reports and Thermal Inspection Reports, extracts observations and images, and generates a structured professional DDR automatically.

---

## Overview

This project automates the process of generating Detailed Diagnostic Reports (DDR) from multiple inspection documents.

The system:

- Extracts text from Inspection Reports and Thermal Reports
- Extracts inspection and thermal images
- Uses Google Gemini to analyze findings
- Merges related observations
- Identifies missing information and conflicts
- Generates a structured client-friendly DDR PDF

---

## Features

- PDF Text Extraction
- Inspection Image Extraction
- Thermal Image Extraction
- AI-Powered Observation Analysis
- Duplicate Observation Merging
- Missing Information Detection
- Conflict Detection
- Structured JSON Generation
- Professional DDR PDF Generation
- Streamlit Web Interface

---

## Workflow

```text
Inspection Report PDF
          +
Thermal Report PDF
          │
          ▼
PDF Parsing
          │
          ▼
Text & Image Extraction
          │
          ▼
Gemini AI Analysis
          │
          ▼
Structured JSON
          │
          ▼
DDR PDF Generation
```

---

## Tech Stack

### Programming Language

- Python

### AI / LLM

- Google Gemini 2.5 Flash

### PDF Processing

- PyMuPDF

### PDF Generation

- ReportLab

### Frontend

- Streamlit

### Utilities

- Pillow
- Pydantic
- Python Dotenv

---

## Project Structure

```text
ai-ddr-generator/

│
├── app.py
│
├── utils/
│   ├── extract_text.py
│   ├── extract_images.py
│   ├── generate_ddr.py
│   ├── create_pdf.py
|   └── thermal_parser.py
│
├── extracted_images/
│
├── output/
│
├── requirements.txt
│
├── .gitignore
│
├── .env
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-ddr-generator.git

cd ai-ddr-generator
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Input

The system accepts:

1. Property Inspection Report (PDF)
2. Thermal Inspection Report (PDF)

---

## Output

The system generates:

- Detailed Diagnostic Report (PDF)
- Property Issue Summary
- Area-wise Observations
- Root Cause Analysis
- Severity Assessment
- Recommendations
- Missing Information Summary
- Supporting Inspection Images
- Thermal Analysis Summary

---

## Key Design Principles

The system follows the following rules:

- Uses only information present in the source reports
- Does not invent facts
- Reports conflicts when detected
- Uses "Not Available" for missing information
- Uses simple client-friendly language
- Avoids unnecessary technical jargon
- Designed to work on similar inspection reports, not only sample files

---

## Screenshots

### Application Interface

Add screenshot here:

```text
screenshots/ui.png
```

### Generated DDR Report

Add screenshot here:

```text
screenshots/output_report.png
```

---

## Future Improvements

- OCR support for scanned PDFs
- Better thermal image-to-location mapping
- Multi-property report processing
- Interactive dashboard
- Historical report database
- Advanced report analytics

---

## Author

**Trailokya Dhotre**

Final Year B.Tech CSE (AIML)

Machine Learning | Deep Learning | Generative AI | LLM Applications