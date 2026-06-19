import streamlit as st
import os

from utils.extract_text import extract_text
from utils.extract_images import extract_images
from utils.thermal_parser import build_thermal_map
from utils.generate_ddr import generate_ddr
from utils.create_pdf import create_pdf

st.title("DDR Report Generator")

inspection_pdf = st.file_uploader("Upload Inspection Report", type=["pdf"])
thermal_pdf = st.file_uploader("Upload Thermal Report", type=["pdf"])

if st.button("Generate DDR"):

    if inspection_pdf and thermal_pdf:

        os.makedirs("temp", exist_ok=True)

        inspection_path = "temp/inspection.pdf"
        thermal_path = "temp/thermal.pdf"

        with open(inspection_path, "wb") as f:
            f.write(inspection_pdf.getbuffer())

        with open(thermal_path, "wb") as f:
            f.write(thermal_pdf.getbuffer())

        with st.spinner("Extracting text..."):
            inspection_text = extract_text(inspection_path)
            thermal_text = extract_text(thermal_path)
        st.success("Text Extracted Successfully.")
        
        with st.spinner("Extracting images..."):
            inspection_images = extract_images(inspection_path, "extracted_images/inspection")
            thermal_images = extract_images(thermal_path, "extracted_images/thermal")
        st.success("Images Extracted Successfully.")
        
        # Photo N -> path (used by the LLM's inspection_photo_refs)
        photo_map = {img["order"]: img["path"] for img in inspection_images}

        # filename -> {thermal_scan_path, reference_photo_path, hotspot, coldspot}
        thermal_map = build_thermal_map(thermal_text, thermal_images)
        thermal_filenames = list(thermal_map.keys())

        with st.spinner("Generating DDR with AI..."):
            ddr = generate_ddr(
                inspection_text,
                thermal_text,
                max_photo_number=len(inspection_images),
                thermal_filenames=thermal_filenames
            )
            
            
        os.makedirs("output", exist_ok=True)
        create_pdf(ddr, photo_map, thermal_map, "output/ddr_report.pdf")

        st.success("DDR Generated Successfully")

        with st.expander("View raw structured DDR (JSON)"):
            st.json(ddr)

        with open("output/ddr_report.pdf", "rb") as f:
            if st.download_button(
                "Download DDR PDF",
                f,
                file_name="DDR_Report.pdf"
            ):
                st.success("DDR_Report.pdf Downloaded Successfully")
            
    else:
        st.warning("Please upload both the Inspection Report and the Thermal Report PDFs.")
