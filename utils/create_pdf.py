from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
)

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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

    section_style = ParagraphStyle(
    "SectionStyle",
    parent=styles["Heading1"],
    fontSize=16,
    spaceAfter=10
)
    

    elements.append(Paragraph("Detailed Diagnostic Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    
    
    
    property_info = report_data.get(
    "property_information",
    {}
    )

    elements.append(
        Paragraph(
            "Property Information",
            section_style
        )
    )

    property_table = [
        ["Customer Name", property_info.get("customer_name", "Not Available")],
        ["Mobile", property_info.get("mobile", "Not Available")],
        ["Email", property_info.get("email", "Not Available")],
        ["Address", property_info.get("address", "Not Available")],
        ["Property Age (Years)", property_info.get("property_age", "Not Available")],
        ["Property Type", property_info.get("property_type", "Not Available")],
        ["Floors", property_info.get("floors", "Not Available")],
        ["Previous Structural Audit", property_info.get("previous_structural_audit_done", "Not Available")],
        ["Previous Repair Work", property_info.get("previous_repair_work_done", "Not Available")],
        ["Inspection Date & Time", property_info.get("inspection_date_time", "Not Available")],
        ["Inspected By", property_info.get("inspected_by", "Not Available")]
    ]

    table = Table(
        property_table,
        colWidths=[180, 320]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),
            ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE")
        ])
    )

    elements.append(table)
    elements.append(Spacer(1,20))

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

        #relevant inspection photos, by explicit Photo N reference 
        for p in obs.get("inspection_photo_refs", []):
            img_path = photo_map.get(p)
            img = _safe_image(img_path, 250, 180)
            if img:
                elements.append(img)
                elements.append(Paragraph(f"Photo {p}", styles["BodyText"]))
                elements.append(Spacer(1, 6))
                any_image = True

        #relevant thermal images, by explicit filename reference
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


    elements.append(Paragraph("3. Thermal Findings Summary", styles["Heading1"]))
    elements.append(Paragraph(
        report_data.get("thermal_summary", "Not Available"),
        styles["BodyText"]
    ))
    elements.append(Spacer(1, 12))


    elements.append(Paragraph("4. Additional Notes", styles["Heading1"]))
    elements.append(Paragraph(
        report_data.get("additional_notes", "Not Available"),
        styles["BodyText"]
    ))
    elements.append(Spacer(1, 12))

    missing_info = report_data.get(
        "missing_information",
        []
    )

    if isinstance(missing_info, list):

        for item in missing_info:
            elements.append(
                Paragraph(
                    f"• {item}",
                    styles["BodyText"]
                )
            )

    else:

        elements.append(
            Paragraph(
                str(missing_info),
                styles["BodyText"]
            )
        )

    doc.build(elements)
