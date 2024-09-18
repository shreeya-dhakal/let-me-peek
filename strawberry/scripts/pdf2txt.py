import os
import argparse
from pdf2image import convert_from_path
import pytesseract

class PDFtoTextConverter:
    def __init__(self, pdfs_path, out_txt_path):
        self.folder_path = pdfs_path
        self.output_folder = out_txt_path
        if not os.path.exists(out_txt_path):
            os.makedirs(out_txt_path)
        
        pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
        self.tesseract_config = r'--oem 3 --psm 6 -l nep+eng'

    def convert_pdf_to_text(self, pdf_file):
        try:
            images = convert_from_path(pdf_file)
            
            text = ""
            for i, image in enumerate(images):
                text += pytesseract.image_to_string(image, config=self.tesseract_config)
                text += f"\n\n--- Page {i+1} ---\n\n"
            
            return text
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
            return ""


def main():
    parser = argparse.ArgumentParser(description="Convert PDFs in a folder to text files using OCR")
    parser.add_argument("--pdfs_path", help="Path to the folder containing PDFs")
    parser.add_argument("--out_txt_path", help="Path to the folder where text files will be saved")
    args = parser.parse_args()

    converter = PDFtoTextConverter(args.pdfs_path, args.out_txt_path)

    for filename in os.listdir(converter.folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(converter.folder_path, filename)
            text = converter.convert_pdf_to_text(pdf_path)
            output_file = os.path.join(converter.output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)

if __name__ == "__main__":
    main()
    