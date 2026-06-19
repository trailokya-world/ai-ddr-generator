from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet
import os


def _safe_image(path, width, height):
    try:
        if path and os.path.exists(path):
            return Image(path, width=width, height=height)
    except Exception:
        pass
    return None


def create_pdf(report_data, photo_map, thermal_map, output_path):
    """
    photo_map:   {photo_number(int): image_path}            -- from inspection report
    thermal_map: {filename(str): {"thermal_scan_path", "reference_photo_path",
                                   "hotspot", "coldspot", "page"}}
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    elements = []


    elements.append(Paragraph("Detailed Diagnostic Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("1. Property Issue Summary", styles["Heading1"]))
    elements.append(Paragraph(
        report_data.get("property_issue_summary", "Not Available"),
        styles["BodyText"]
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("2. Area-wise Observations", styles["Heading1"]))

    observations = report_data.get("observations", [])

    if not observations:
        elements.append(Paragraph("Not Available", styles["BodyText"]))

    for idx, obs in enumerate(observations):
        elements.append(Paragraph(
            f"Area {idx + 1}: {obs.get('area', 'Not Available')}",
            styles["Heading2"]
        ))
        elements.append(Paragraph(
            f"<b>Observation:</b> {obs.get('observation', 'Not Available')}",
            styles["BodyText"]
        ))
        elements.append(Paragraph(
            f"<b>Probable Root Cause:</b> {obs.get('root_cause', 'Not Available')}",
            styles["BodyText"]
        ))
        severity = obs.get("severity", "Not Available")
        reasoning = obs.get("severity_reasoning", "")
        sev_line = f"<b>Severity:</b> {severity}"
        if reasoning:
            sev_line += f" — {reasoning}"
        elements.append(Paragraph(sev_line, styles["BodyText"]))
        elements.append(Paragraph(
            f"<b>Recommended Action:</b> {obs.get('recommendation', 'Not Available')}",
            styles["BodyText"]
        ))
        elements.append(Spacer(1, 8))

        any_image = False

       
        for p in obs.get("inspection_photo_refs", []):
            img_path = photo_map.get(p)
            img = _safe_image(img_path, 250, 180)
            if img:
                elements.append(img)
                elements.append(Paragraph(f"Photo {p}", styles["BodyText"]))
                elements.append(Spacer(1, 6))
                any_image = True


        for fname in obs.get("thermal_image_refs", []):
            t = thermal_map.get(fname)
            if not t:
                continue

            scan_img = _safe_image(t.get("thermal_scan_path"), 250, 180)
            if scan_img:
                elements.append(scan_img)
                elements.append(Paragraph(
                    f"Thermal scan ({fname}) — Hotspot: {t.get('hotspot', 'Not Available')}, "
                    f"Coldspot: {t.get('coldspot', 'Not Available')}",
                    styles["BodyText"]
                ))
                elements.append(Spacer(1, 6))
                any_image = True

            ref_img = _safe_image(t.get("reference_photo_path"), 250, 180)
            if ref_img:
                elements.append(ref_img)
                elements.append(Spacer(1, 6))
                any_image = True

        if not any_image:
            elements.append(Paragraph("Image Not Available", styles["BodyText"]))

        elements.append(Spacer(1, 15))


    elements.append(Paragraph("3. Additional Notes", styles["Heading1"]))
    elements.append(Paragraph(
        report_data.get("additional_notes", "Not Available"),
        styles["BodyText"]
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("4. Missing or Unclear Information", styles["Heading1"]))
    elements.append(Paragraph(
        report_data.get("missing_information", "Not Available"),
        styles["BodyText"]
    ))

    doc.build(elements)
