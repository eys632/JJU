import requests
import streamlit as st

# API 정보
API_KEY = "4321964459"  # 발급받은 API 키를 입력하세요
BASE_URL = "https://data.ex.co.kr/openapi/trtm/realUnitTrtm"  # 실시간 교통 정보 API 엔드포인트

# Streamlit 앱 제목
st.title("실시간 교통 정보 조회")

# 사용자가 선택할 수 있는 시작/끝 단위 코드 입력 받기
start_unit_code = st.text_input("시작 단위 코드 (예: 101)", "101")
end_unit_code = st.text_input("끝 단위 코드 (예: 105)", "105")

# 요청 파라미터 설정
params = {
    "key": API_KEY,             # API 키
    "type": "xml",              # 응답 형식 (xml 또는 json)
    "iStartUnitCode": start_unit_code,    # 시작 단위 코드
    "iEndUnitCode": end_unit_code,      # 끝 단위 코드
    "numOfRows": "10",          # 한 번에 가져올 데이터 수
    "pageNo": "1"               # 페이지 번호
}

# API 요청 및 처리 버튼
if st.button("교통 정보 조회"):
    try:
        # GET 요청
        response = requests.get(BASE_URL, params=params)
        st.write("요청 URL:", response.url)  # 완성된 URL 출력

        if response.status_code == 200:  # 요청 성공
            # XML 응답 처리 (json을 원하면 response.json() 사용)
            data = response.text  # XML 데이터
            st.subheader("응답 데이터:")
            st.text(data)  # 실시간 교통 정보 출력

        else:
            # 요청 실패
            st.error(f"API 요청 실패. 상태 코드: {response.status_code}")
            st.text(f"응답 메시지: {response.text}")  # 서버에서 반환한 메시지 출력

    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 중 오류 발생: {e}")
