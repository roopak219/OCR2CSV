import re
import csv
from pathlib import Path

TEXT_FOLDER = Path(r"C:\Users\WELCOME\Downloads\Electoral roll\Text")
OUTPUT_FOLDER = Path(r"C:\Users\WELCOME\Downloads\Electoral roll\Master")
OUTPUT_FOLDER.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_FOLDER / "master_v1.csv"

rows = []

# ---------------- OCR Fixes ---------------- #

OCR_FIXES = {
    "प्ार": "HR",
    "पार": "HR",
    "नार": "HR",
    "पा२": "HR",
    "प्ा१": "HR",
    "प्ाए": "HR",
    "पाप": "HR",
    "I": "1"
}

def clean_ocr(text):

    for old, new in OCR_FIXES.items():
        text = text.replace(old, new)

    text = re.sub(r"\.{2,}", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_epic(text):

    text = clean_ocr(text)

    patterns = [
        r'HR/\d{2}/\d{2}/\d+',
        r'HR/\d{2}/\d{2}1/\d+',
        r'HR/\d{2}/\d{2}/033\d+',
        r'HR/\d{2}/\d{2}/085\d+'
    ]

    for pattern in patterns:

        m = re.search(pattern, text)

        if m:
            return m.group()

    return ""


# ---------------- MAIN ---------------- #

folders = sorted(TEXT_FOLDER.iterdir())

for folder in folders:

    if not folder.is_dir():
        continue

    part = folder.name

    print(f"Processing {part}")

    txt_files = sorted(folder.glob("*.txt"))

    for txt in txt_files:

        page = txt.stem.replace("page_", "")

        with open(txt, encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                # Only voter rows
                if not re.match(r'^[0-9०-९]+', line):
                    continue

                m = re.match(r'^([0-9०-९]+)\s+([^\s]+)\s+(.*)', line)

                if not m:
                    continue

                serial = m.group(1)
                token = m.group(2)
                rest = m.group(3)

                # House number
                if re.match(r'^[0-9०-९]+([/-][0-9०-९]+)?[A-Za-zक-ह]*$', token):
                    house = token
                    details = rest
                else:
                    house = ""
                    details = token + " " + rest

                details = clean_ocr(details)

                epic = extract_epic(details)

                rows.append({
                    "Part": part,
                    "Page": page,
                    "Serial": serial,
                    "House": house,
                    "Details": details,
                    "EPIC": epic,
                    "Raw": line
                })

# ---------------- WRITE CSV ---------------- #

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Part",
            "Page",
            "Serial",
            "House",
            "Details",
            "EPIC",
            "Raw"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print(f"\nDone!")
print(f"Rows : {len(rows)}")
print(f"Saved : {OUTPUT_FILE}")