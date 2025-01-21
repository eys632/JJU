# loaders/secure_file_loader.py

import os
import yaml
import pdfplumber
from typing import Dict
import logging
from exceptions.file_loader_exceptions import (
    FileLoaderError,
    InvalidFileExtensionError,
    DirectoryTraversalError,
    YamlParsingError,
    PdfProcessingError,
)
from config.settings import BASE_DIR

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureFileLoader:
    def __init__(self, base_dir: str = BASE_DIR) -> None:
        self.base_dir = base_dir

    def _validate_and_construct_path(self, filename: str) -> str:
        valid_extensions = [".pdf", ".yaml", ".yml"]
        if not any(filename.lower().endswith(ext) for ext in valid_extensions):
            logger.error(f"유효한 확장자가 아닙니다. 사용 가능한 확장자: {', '.join(valid_extensions)}")
            raise InvalidFileExtensionError(
                f"유효한 확장자가 아닙니다. 사용 가능한 확장자: {', '.join(valid_extensions)}"
            )

        safe_filename = os.path.basename(filename)
        full_path = os.path.join(self.base_dir, safe_filename)

        normalized_base = os.path.abspath(self.base_dir)
        normalized_target = os.path.abspath(full_path)
        if not normalized_target.startswith(normalized_base):
            logger.error("파일 경로가 지정된 디렉토리를 벗어났습니다.")
            raise DirectoryTraversalError("파일 경로가 지정된 디렉토리를 벗어났습니다.")

        return full_path

    def load_yaml(self, filename: str) -> Dict:
        path = self._validate_and_construct_path(filename)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            logger.info(f"Successfully loaded YAML file: {path}")
        except FileNotFoundError:
            logger.error(f"파일을 찾을 수 없습니다: {path}")
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
        except yaml.YAMLError as e:
            logger.error(f"YAML 파싱 중 오류: {e}")
            raise YamlParsingError(f"YAML 파싱 중 오류: {e}")
        except Exception as e:
            logger.error(f"알 수 없는 오류: {e}")
            raise FileLoaderError(f"알 수 없는 오류: {e}")
        return data

    def load_pdf(self, filename: str) -> str:
        path = self._validate_and_construct_path(filename)
        all_text = []
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text.append(text)
            logger.info(f"Successfully loaded PDF file: {path}")
        except FileNotFoundError:
            logger.error(f"파일을 찾을 수 없습니다: {path}")
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
        except Exception as e:
            logger.error(f"PDF 처리 중 오류: {e}")
            raise PdfProcessingError(f"PDF 처리 중 오류: {e}")
        return "\n".join(all_text)

if __name__ == "__main__":
    loader = SecureFileLoader(base_dir="data")
    try:
        yaml_data = loader.load_yaml("Q&A.yaml")
        print("YAML 데이터:", yaml_data)
    except Exception as e:
        print("YAML 로딩 오류:", e)

    try:
        pdf_text = loader.load_pdf("Search-o1 Agentic Search-Enhanced.pdf")
        print("PDF 텍스트 내용:\n", pdf_text)
    except Exception as e:
        print("PDF 로딩 오류:", e)
