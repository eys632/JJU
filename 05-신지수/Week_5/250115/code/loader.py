import os
import yaml
import pdfplumber


class SecureFileLoader:
    """
    파일을 안전하게 로드하기 위한 로더 클래스.
    - 기본 디렉토리(기본값: data/)를 기준으로만 파일을 열 수 있도록 하여
      디렉토리 이동 공격(Directory Traversal Attack)을 방지합니다.
    - 파일 확장자 유효성 검증을 통해 잘못된 확장자를 가진 파일 불러오기를 방지합니다.
    - 예외 처리를 통해 파일 불러오기 실패 시 에러를 확인할 수 있게 합니다.
    """

    def __init__(self, base_dir="data"):
        """
        :param base_dir: 로딩할 파일이 위치한 기본 디렉토리 경로
        """
        self.base_dir = base_dir

    def _validate_and_construct_path(self, filename: str) -> str:
        """
        파일명을 검증하고 안전한 파일 경로를 생성합니다.
        - os.path.basename를 통해 디렉토리 경로 제거
        - os.path.join으로 기본 디렉토리에 연결
        """

        # 1) 확장자 확인 (예: .pdf 또는 .yaml, .yml)
        valid_extensions = [".pdf", ".yaml", ".yml"]
        if not any(filename.lower().endswith(ext) for ext in valid_extensions):
            raise ValueError(
                f"유효한 확장자가 아닙니다. 사용 가능한 확장자: {', '.join(valid_extensions)}"
            )

        # 2) 파일명에서 디렉토리 경로 제거(Directory Traversal 방지)
        safe_filename = os.path.basename(filename)

        # 3) base_dir와 합쳐서 최종 경로 생성
        full_path = os.path.join(self.base_dir, safe_filename)

        # 파일이 실제 디렉토리를 벗어나지 않는지 확인(추가 보안)
        normalized_base = os.path.abspath(self.base_dir)
        normalized_target = os.path.abspath(full_path)
        if not normalized_target.startswith(normalized_base):
            raise PermissionError("파일 경로가 지정된 디렉토리를 벗어났습니다.")

        return full_path

    def load_yaml(self, filename: str) -> dict:
        """
        YAML 파일 로드 함수.
        :param filename: 불러올 YAML 파일명
        :return: 파싱된 YAML 데이터(dict)
        """
        path = self._validate_and_construct_path(filename)

        # 실제 데이터 로딩
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
        except yaml.YAMLError as e:
            raise ValueError(f"YAML 파싱 중 오류가 발생했습니다: {e}")
        except Exception as e:
            raise RuntimeError(f"알 수 없는 오류가 발생했습니다: {e}")

        return data

    def load_pdf(self, filename: str) -> str:
        """
        PDF 파일 텍스트 로드 함수.
        :param filename: 불러올 PDF 파일명
        :return: PDF 전체 페이지의 텍스트를 합쳐서 반환한 문자열
        """
        path = self._validate_and_construct_path(filename)
        all_text = []

        try:
            with pdfplumber.open(path) as pdf:
                # 각 페이지를 순회하면서 텍스트를 추출
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text.append(text)
        except FileNotFoundError:
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
        except Exception as e:
            raise RuntimeError(f"PDF 처리 중 오류가 발생했습니다: {e}")

        # 리스트로 모인 텍스트를 합쳐 하나의 문자열로 반환
        return "\n".join(all_text)


if __name__ == "__main__":
    # 사용 예시
    loader = SecureFileLoader(base_dir="data")
    
    # 1) YAML 로드
    try:
        yaml_data = loader.load_yaml("Q&A.yaml")
        print("YAML 데이터:", yaml_data)
    except Exception as e:
        print("YAML 로딩 오류:", e)

    # 2) PDF 로드
    try:
        pdf_text = loader.load_pdf("Search-o1 Agentic Search-Enhanced.pdf")
        print("PDF 텍스트 내용:\n", pdf_text)
    except Exception as e:
        print("PDF 로딩 오류:", e)
