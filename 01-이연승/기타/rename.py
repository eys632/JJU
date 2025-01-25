import os

# 변경할 파일이 있는 폴더 경로
root_folder = r"C:\\Users\\eys63\\GitHub\\JJU\\01-이연승"

# 파일 이름 매핑 (현재 이름 -> 새 이름)
rename_map = {
    "02_LCEL_241226_2_이연승.ipynb": "241226_api key.ipynb",
    "241226_movie_recommendation_prompt.py": "241226_movie recommendation prompt.py",
    "241226_prompt_template_chain.py": "241226_prompt template chain.py",
    "241227_1_CharacterTextSpilitter_이연승.ipynb": "241227_character text splitter.ipynb",
    "241227_2_이연승.ipynb": "241227_appendix text processor.ipynb",
    "07_02_TOKENTEXTSPLITTER.py": "241230_token text splitter.py",
    "241230_1st(0703)_TokenTextSplitter_이연승.ipynb": "241230_token text splitter.ipynb",
    "241230_2_이연승.ipynb": "241230_os and environment.ipynb",
    "241230_3_이연승.ipynb": "241230_langchain installation.ipynb",
    "241230_4_이연승.ipynb": "241230_assignment 1 and 5.ipynb",
    "241230_과제_0702_RESULT_TOKENTEXTSPLITTER.ipynb": "241230_token text splitter result.ipynb",
    "241231_1_이연승.ipynb": "241231_markdown header text splitter.ipynb",
    "241231_3_이연승.ipynb": "241231_document handling.ipynb",
    "241231_과제_html text splitter.py": "241231_html text splitter.py",
    "250102_1_DocumentLoder(pdf)통합본_이연승.ipynb": "250102_pdf loader.ipynb",
    "250102_github practice.py": "250102_github practice.py",
    "06_02_HWPLoader.ipynb": "250103_hwploader setup.ipynb",
    "PDFSplit과제.ipynb": "250103_pdf split task.ipynb",
    "강의내용,과제내용.ipynb": "250103_github basics.ipynb",
    "csvLoader.ipynb": "250106_csv loader.ipynb",
    "langSmith.ipynb": "250106_langsmith.ipynb",
    "upstage.ipynb": "250106_upstage.ipynb",
    "WebbaseLoader.ipynb": "250106_webbase loader.ipynb",
    "06_13_LOADER_LLAMAPARSER-1_0107과제.py": "250107_llama parser loader.py",
    "DirectoryLoader.ipynb": "250107_directory loader.ipynb",
    "LLamaindexParser.ipynb": "250107_llama parser.ipynb",
    "loaders/pdf_loader.py": "250108_pdf loader.py",
    "main/main.py": "250108_main setup.py",
    "01_SimpleOpenAI.ipynb": "250109_prompt template basic.ipynb",
    "01_SimpleOpenAI강사님ver.ipynb": "250109_prompt template instructor version.ipynb",
    "51-00_small_agent.ipynb": "250109_small agent setup.ipynb",
    "02_streamlit.py": "250110_streamlit setup.py",
    "03-01_PydenticOutputParser.ipynb": "250114_output parser basics.ipynb",
    "04_Similarity.ipynb": "250114_similarity analysis.ipynb",
}

# 파일 이름 변경 함수
def rename_files_in_folders(root_folder, rename_map):
    for subdir, _, files in os.walk(root_folder):  # 모든 하위 폴더 탐색
        for old_name, new_name in rename_map.items():
            if old_name in files:  # 현재 폴더에 파일이 있을 경우
                old_path = os.path.join(subdir, old_name)
                new_path = os.path.join(subdir, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")
            else:
                print(f"File not found in: {subdir} - {old_name}")

# 실행
if __name__ == "__main__":
    rename_files_in_folders(root_folder, rename_map)
