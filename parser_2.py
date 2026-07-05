
import re
import csv
from pathlib import Path

INPUT_FILE = r"C:\Users\WELCOME\Downloads\Electoral roll\Text\page2.txt"
OUTPUT_FILE = r"C:\Users\WELCOME\Downloads\Electoral roll\Master\master5.csv"

Path("output").mkdir(exist_ok=True)

rows = []

with open(INPUT_FILE, encoding="utf-8") as f:

    for line in f:

        line = line.strip()

        if not line:
            continue

        # Skip headers
        if not re.match(r'^[0-9०-९]+', line):
            continue

        m = re.match(r'^([0-9०-९]+)\s+([^\s]+)\s+(.*)', line)

        if not m:
            continue

        serial = m.group(1)
        token = m.group(2)
        rest = m.group(3)

        # ---------------- House Number ----------------

        if re.match(r'^[0-9०-९]+([/-][0-9०-९]+)?[A-Za-zक-ह]*$', token):
            house = token
            details = rest
        else:
            house = ""
            details = token + " " + rest

        # ---------------- Age ----------------

        age = ""

        m_age = re.search(r'(\d{1,3})\s*$', details)

        if m_age:
            age = m_age.group(1)
            details = details[:m_age.start()].strip()

        # ---------------- EPIC ----------------

        epic = ""

        epic_patterns = [
            r'HR/\d+/\d+/\d+',
            r'HR/\d+/\d+[A-Za-zI]*/\d+',
            r'[A-Za-zप्ा०-९/!\]\[]+033\d+',
            r'[A-Za-zप्ा०-९/!\]\[]+085\d+'
        ]

        for pattern in epic_patterns:

            m_epic = re.search(pattern, details)

            if m_epic:
                epic = m_epic.group()
                details = details.replace(epic, "").strip()
                break

        # ---------------- Clean ----------------

        details = re.sub(r'\.{2,}', ' ', details)
        details = re.sub(r'\s+', ' ', details).strip()

        rows.append({
            "Serial": serial,
            "House": house,
            "Details": details,
            "Age": age,
            "EPIC": epic,
            "Raw": line
        })

# ---------------- Write CSV ----------------

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Serial",
            "House",
            "Details",
            "Age",
            "EPIC",
            "Raw"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print(f"Done. Parsed {len(rows)} rows.")