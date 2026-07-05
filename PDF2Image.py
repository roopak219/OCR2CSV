import fitz
from pathlib import Path

PDF_FOLDER = Path(r"C:\Users\WELCOME\Downloads\Electoral roll\Sonipat_2002")
IMAGE_FOLDER = Path(r"C:\Users\WELCOME\Downloads\Electoral roll\images")

DPI = 400

def convert_all_pdfs():

    IMAGE_FOLDER.mkdir(exist_ok=True)

    pdfs = sorted(PDF_FOLDER.glob("*.pdf"))

    print(f"Found {len(pdfs)} PDFs")

    for pdf in pdfs:

        print(f"\nProcessing {pdf.name}")

        out_folder = IMAGE_FOLDER / pdf.stem
        out_folder.mkdir(exist_ok=True)

        doc = fitz.open(pdf)

        for page_no in range(len(doc)):

            page = doc.load_page(page_no)

            pix = page.get_pixmap(dpi=DPI)

            filename = out_folder / f"page_{page_no+1:03d}.png"

            pix.save(filename)

        print(f"Saved {len(doc)} pages")

if __name__ == "__main__":
    convert_all_pdfs()