import re


def build_thermal_map(thermal_text, thermal_images):
    """
    The thermal report has one reading per page, each with a thermal scan
    image followed by a reference photo. PyMuPDF's page.get_images(full=True)
    is not reliably scoped per page for this PDF (it can return the whole
    document's shared image pool), so instead of grouping by page we rely on
    sequential order: after filtering out icons/logos, content images appear
    in the same order as the pages, two per page (scan, then photo).

    Returns:
        {
            "RB02380X.JPG": {
                "hotspot": "28.8 °C",
                "coldspot": "23.4 °C",
                "thermal_scan_path": "...",
                "reference_photo_path": "..."
            },
            ...
        }
    """
    thermal_map = {}

    chunks = re.split(r"--- Page (\d+) ---", thermal_text)
    # re.split with a capturing group -> ['', '1', text1, '2', text2, ...]
    for i in range(1, len(chunks), 2):
        page_num = int(chunks[i])
        chunk = chunks[i + 1] if i + 1 < len(chunks) else ""

        filename_match = re.search(r"Thermal image\s*:\s*([\w\-]+\.(?:JPG|JPEG|PNG))", chunk, re.IGNORECASE)
        hotspot_match = re.search(r"Hotspot\s*:\s*([\d.]+\s*°?\s*C)", chunk)
        coldspot_match = re.search(r"Coldspot\s*:\s*([\d.]+\s*°?\s*C)", chunk)

        filename = filename_match.group(1) if filename_match else f"page_{page_num}_image"

        scan_idx = (page_num - 1) * 2
        photo_idx = scan_idx + 1

        thermal_map[filename] = {
            "page": page_num,
            "hotspot": hotspot_match.group(1) if hotspot_match else "Not Available",
            "coldspot": coldspot_match.group(1) if coldspot_match else "Not Available",
            "thermal_scan_path": thermal_images[scan_idx]["path"] if scan_idx < len(thermal_images) else None,
            "reference_photo_path": thermal_images[photo_idx]["path"] if photo_idx < len(thermal_images) else None,
        }

    return thermal_map
