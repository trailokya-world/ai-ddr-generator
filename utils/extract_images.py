import fitz
import os
import hashlib


def _is_content_image(width, height, min_area=20000, max_aspect=4.0):
  
    area = width * height
    if area < min_area:
        return False
    aspect = max(width, height) / max(min(width, height), 1)
    if aspect > max_aspect:
        return False
    return True


def extract_images(pdf_path, output_dir, content_only=True):

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)

    seen_hashes = set()
    images = []
    order = 0

    for page_num in range(len(doc)):
        page = doc[page_num]

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            width = base_image.get("width", 0)
            height = base_image.get("height", 0)

            if content_only and not _is_content_image(width, height):
                continue

            img_hash = hashlib.md5(image_bytes).hexdigest()
            if img_hash in seen_hashes:
                continue
            seen_hashes.add(img_hash)

            order += 1
            image_name = f"img_{order:03d}_p{page_num + 1}_{img_index}.{image_ext}"
            image_path = os.path.join(output_dir, image_name)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            images.append({
                "path": image_path,
                "page": page_num + 1,
                "order": order
            })

    doc.close()
    return images
