import PyPDF2
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import pdfplumber
import os

class DocumentLoader:
    def __init__(self, file_path, output_dir=None):
        """Initialize with the PDF file path and output directory."""
        self.file_path = file_path
        # output_dir을 명시하지 않으면 기본 경로로 설정
        self.output_dir = output_dir or "C:\\Users\\eys63\\GitHub\\JJU\\01-이연승\\과제\\25_01_22과제_ChromaDB\\output"
        os.makedirs(self.output_dir, exist_ok=True)  # Create output directory if it doesn't exist

    def load_with_pypdf(self):
        """Extract text using PyPDF2."""
        text = ""
        try:
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"PyPDF2 Error: {e}")
            return None

    def load_with_pymupdf(self):
        """Extract text using PyMuPDF."""
        text = ""
        try:
            doc = fitz.open(self.file_path)
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            print(f"PyMuPDF Error: {e}")
            return None

    def load_with_pdfminer(self):
        """Extract text using PDFMiner."""
        try:
            text = extract_text(self.file_path)
            return text
        except Exception as e:
            print(f"PDFMiner Error: {e}")
            return None

    def load_with_pdfplumber(self):
        """Extract text using PDFPlumber."""
        text = ""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"PDFPlumber Error: {e}")
            return None

    def save_text(self, method_name, text):
        """Save extracted text to a file."""
        try:
            output_path = os.path.join(self.output_dir, f"{method_name}_extracted_text.txt")
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Text saved to {output_path}")
        except Exception as e:
            print(f"Error saving text: {e}")

    def process(self):
        """Process the PDF with all methods and save results."""
        print(f"Processing file: {self.file_path}")

        methods = {
            "PyPDF2": self.load_with_pypdf,
            "PyMuPDF": self.load_with_pymupdf,
            "PDFMiner": self.load_with_pdfminer,
            "PDFPlumber": self.load_with_pdfplumber,
        }

        for method_name, method in methods.items():
            print(f"Using {method_name}...")
            text = method()
            if text:
                print(f"{method_name} succeeded. Saving result...")
                self.save_text(method_name, text)
            else:
                print(f"{method_name} failed to extract text.")


if __name__ == "__main__":
    # PDF 경로 설정
    pdf_path = r"C:\Users\eys63\GitHub\JJU\01-이연승\data\Linear Algebra and Its Applications, chapter1.pdf"

    # DocumentLoader 객체 생성 및 실행
    loader = DocumentLoader(pdf_path)
    loader.process()
