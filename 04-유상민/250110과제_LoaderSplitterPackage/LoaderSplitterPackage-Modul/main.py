# main.py
from loaders import load_file
from splitters import split_texts
from analyzers import analyze_with_gpt
from utils import detect_input_type, detect_file_type, load_env

def main(input_data):
    # 환경 변수 로드
    env = load_env()
    if not env.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

    # 입력 데이터 유형 및 파일 유형 감지
    input_type = detect_input_type(input_data)
    file_type = detect_file_type(input_data) if input_type == "FILE" else "URL"

    # URL로 잘못 감지되지 않도록 보완
    if file_type != "URL":
        input_type = "FILE"

    print(f"1. Input 데이터 유형: {input_type}")
    print(f"2. 파일 타입: {file_type}")

    try:
        # 데이터 로드
        loader_results = load_file(file_type, input_data)
        print(f"3. Loader 결과: 데이터 로드 완료")

        # 데이터 분리
        split_results = split_texts(file_type, loader_results)
        print(f"4. Splitter 결과: {len(split_results)}개의 텍스트 조각 생성")

        # 데이터 분석
        gpt_result = analyze_with_gpt(file_type, (loader_results, split_results))
        print("5. GPT 분석 결과:")
        print(gpt_result)

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    # 입력 파일 경로 설정
    input_data = "/workspaces/JJU-1/04-유상민/250110과제_LoaderSplitterPackage/input데이터 모음/231024_포스코기술투자의 여신전문금융업 등록 말소.pdf"
    main(input_data)
