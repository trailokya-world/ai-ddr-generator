import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def _clean_json(raw):
    
    raw = raw.strip()
    raw = re.sub(r"^```(json)?", "", raw)
    raw = re.sub(r"```$", "", raw)
    return raw.strip()


def generate_ddr(inspection_text, thermal_text, max_photo_number, thermal_filenames):
    prompt = f"""
You are generating a Detailed Diagnostic Report (DDR) for a property inspection,
combining a site Inspection Report and a Thermal Imaging Report.

Return ONLY valid JSON. No markdown, no code block, no explanation.

JSON schema:
{{
  "property_issue_summary": "",
  "observations": [
    {{
      "area": "",
      "observation": "",
      "root_cause": "",
      "severity": "Low | Moderate | High",
      "severity_reasoning": "",
      "recommendation": "",
      "inspection_photo_refs": [1, 2],
      "thermal_image_refs": ["RB02380X.JPG"]
    }}
  ],
  "additional_notes": "",
  "missing_information": ""
  }}

  DATA SOURCING

  Use ONLY information explicitly present in the Inspection Report and Thermal Report.
  Never invent, assume, estimate, infer, speculate, or guess any fact.
  Never add information that is not directly supported by the reports.
  If a value cannot be determined from the reports, return exactly: "Not Available".
  Do not create causes, recommendations, severities, locations, temperatures, image mappings, or conclusions that are not explicitly supported by the source documents.

  OBSERVATION MERGING

  Merge Inspection Report findings and Thermal Report findings into a single observation whenever they refer to the same physical area.
  Do not create duplicate observations for the same issue.
  If multiple findings describe the same problem, combine them into one observation.
  Preserve all relevant evidence from both reports when merging.

  CONFLICT HANDLING

  If the Inspection Report and Thermal Report provide conflicting information for the same area, explicitly describe the conflict.
  Never silently choose one source over another.
  Add the conflict description inside the observation.
  If no conflicts exist, do not create artificial conflicts.

  SEVERITY

  Assign severity only when supported by report content.
  Allowed values:
  ["Low", "Moderate", "High", "Critical", "Not Available"]
  If severity cannot be determined directly from the reports, return:
  "Not Available"
  Do not increase or decrease severity based on assumptions.

  ROOT CAUSE

  Use only root causes explicitly stated in the reports.
  Do not perform engineering analysis.
  Do not infer structural failure, waterproofing failure, settlement, material degradation, hidden defects, or similar conclusions unless explicitly mentioned.
  If the root cause is not stated in the reports, return:
  "Not Available"

  RECOMMENDATIONS

  Use only recommendations supported by the reports.
  If no recommendation exists, return:
  "Not Available"

  THERMAL DATA

  Use only thermal observations explicitly present in the Thermal Report.
  Do not infer moisture, leakage, heat loss, water ingress, insulation failure, or any other condition solely from temperature values.
  If the Thermal Report does not explicitly associate a thermal image with a location, do not create the association.
  If location mapping is unavailable, return:
  "Not Available"

  INSPECTION PHOTO REFERENCES

  inspection_photo_refs must contain ONLY photo numbers explicitly referenced near the corresponding observation.
  Allowed values are integers from 1 to {max_photo_number}.
  Do not guess photo mappings.
  Use an empty list [] if no valid photo references exist.

  THERMAL IMAGE REFERENCES

  thermal_image_refs must contain ONLY filenames copied exactly from:
  {thermal_filenames}
  Include a filename only when the Thermal Report explicitly links that thermal image to the observation area.
  Do not infer image-to-room relationships.
  Use an empty list [] when no explicit match exists.

  LANGUAGE

  Use simple, client-friendly language.
  Avoid unnecessary technical jargon.
  If technical terminology exists in the source report, simplify it where possible while preserving meaning.
  Keep observations concise, clear, and professional.

  OUTPUT VALIDITY

  Return ONLY valid JSON.
  Do not return markdown.
  Do not return explanations.
  Do not return comments.
  Do not wrap JSON inside code blocks.
  Every required field must be present.
  Use "Not Available" for unknown values.
  Use [] for unknown image references.
  INSPECTION REPORT:
  {inspection_text}

  THERMAL REPORT:
  {thermal_text}
  """

    response = model.invoke(prompt)
    raw = response.content
    cleaned = _clean_json(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:

        data = {
            "property_issue_summary": "Not Available - the AI model returned a response that could not be parsed as JSON.",
            "observations": [],
            "additional_notes": raw[:3000],
            "missing_information": "Model output could not be parsed. Raw response truncated above."
        }

    return data
