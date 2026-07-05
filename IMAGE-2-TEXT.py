from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageOps
from tqdm import tqdm
import pytesseract

IMAGE_FOLDER = Path(r"C:\Users\WELCOME\Downloads\Electoral roll\images")
TEXT_FOLDER = Path(r"C:\Users\WELCOME\Downloads\Electoral roll\Text")

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

LANG = "hin+eng"
PSM = 4
WORKERS = 6


def process_image(args):
    image_path, output_path = args

    # Skip if already OCR'd
    if output_path.exists():
        return

    img = Image.open(image_path)
    img = ImageOps.grayscale(img)

    text = pytesseract.image_to_string(
        img,
        lang=LANG,
        config=f"--oem 3 --psm {PSM}"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def main():

    jobs = []

    for pdf_folder in IMAGE_FOLDER.iterdir():

        if not pdf_folder.is_dir():
            continue

        out_folder = TEXT_FOLDER / pdf_folder.name

        for image in sorted(pdf_folder.glob("*.png")):

            out_file = out_folder / (image.stem + ".txt")

            jobs.append((image, out_file))

    print(f"{len(jobs)} pages found.")

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        list(tqdm(executor.map(process_image, jobs), total=len(jobs)))

    print("Done!")


if __name__ == "__main__":
    main()