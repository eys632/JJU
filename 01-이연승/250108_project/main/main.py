import os
import mimetypes
import openai
from dotenv import load_dotenv
import asyncio

# 1. .env 파일 로드
load_dotenv()

# 2. 파일 형식 판별 함수
def detect_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type

# 3. 로더 선택 함수
def select_loader(file_type):
    if 'pdf' in file_type:
        return ["PDFLoader1", "PDFLoader2", "PDFLoader3"]
    elif 'text' in file_type:
        return ["txtLoader"]
    elif 'json' in file_type:
        return ["JsonLoader"]
    else:
        return []

# 4. 스플리터 정의
def get_splitters():
    return [
        "CharacterTextSplitter",
        "TokenTextSplitter",
        "RecursiveCharacterTextSplitter"
    ]

# 5. OpenAI API 활용 함수 (최신 API 사용)
async def evaluate_splits(api_key, loader, splitter, data):
    try:
        openai.api_key = api_key
        prompt = f"Loader: {loader}\nSplitter: {splitter}\nData: {data}"
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant evaluating document splits."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response
    except Exception as e:
        print(f"Error evaluating {loader} with {splitter}: {e}")
        return None

# 6. 메인 함수
async def main():
    file_path = input("파일 경로를 입력하세요: ")
    file_type = detect_file_type(file_path)
    if not file_type:
        print("Error: 파일 형식을 감지할 수 없습니다.")
        return
    
    loaders = select_loader(file_type)
    if not loaders:
        print(f"Error: {file_type}에 대한 적절한 로더가 없습니다.")
        return

    splitters = get_splitters()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: 환경 변수 OPENAI_API_KEY가 설정되지 않았습니다.")
        return

    results = []
    for loader in loaders:
        for splitter in splitters:
            data = f"Simulated data using {loader}"
            result = await evaluate_splits(api_key, loader, splitter, data)
            if result:
                results.append({
                    "loader": loader,
                    "splitter": splitter,
                    "result": result
                })
    
    if results:
        best_combination = max(
            results, 
            key=lambda x: x['result']['choices'][0]['message']['content']
        )
        print(f"최적 조합: {best_combination}")
    else:
        print("No results to evaluate.")

# 실행
if __name__ == "__main__":
    asyncio.run(main())
