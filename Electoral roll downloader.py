import requests
import urllib3
from pathlib import Path

# -------------------------------
# Disable SSL warnings
# -------------------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------------
# Configuration
# -------------------------------
BASE_URL = "https://ceoharyana.gov.in/ElectoralRoll2002/CMB41Year2002/"
SAVE_DIR = Path("Sonipat_2002")

START_PART = 55
END_PART = 186

SAVE_DIR.mkdir(exist_ok=True)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}

downloaded = 0
failed = 0

for part in range(START_PART, END_PART + 1):

    filename = f"CMB041{part:04d}.pdf"
    url = BASE_URL + filename

    try:
        response = requests.get(
            url,
            headers=headers,
            verify=False,
            timeout=30,
            stream=True
        )

        if (
            response.status_code == 200
            and "application/pdf" in response.headers.get("Content-Type", "").lower()
        ):

            filepath = SAVE_DIR / filename

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            downloaded += 1
            print(f"✓ Downloaded: {filename}")

        else:
            failed += 1
            print(f"✗ Skipped: {filename} (Status {response.status_code})")

    except Exception as e:
        failed += 1
        print(f"✗ Error downloading {filename}")
        print(e)

print("\n----------------------------")
print(f"Downloaded : {downloaded}")
print(f"Failed     : {failed}")
print(f"Saved to   : {SAVE_DIR.resolve()}")
print("----------------------------")