import json
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import os

def download_and_extract_xml(url, extract_path='corp_num'):
    """
    주어진 URL에서 ZIP 파일을 다운로드하고 지정된 경로에 압축을 해제합니다.
    
    Parameters:
    - url (str): ZIP 파일이 위치한 URL
    - extract_path (str): 압축을 해제할 디렉토리 경로
    """
    try:
        print("ZIP 파일을 다운로드 중입니다...")
        with urlopen(url) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(extract_path)
        print(f"ZIP 파일이 '{extract_path}' 디렉토리에 성공적으로 압축 해제되었습니다.")
    except Exception as e:
        print(f"에러 발생: {e}")
        raise

def parse_xml_to_dict(xml_file_path):
    """
    XML 파일을 파싱하여 회사 이름과 고유번호를 딕셔너리로 변환합니다.
    단, stock_code가 비어 있지 않은 데이터만 포함합니다.
    
    Parameters:
    - xml_file_path (str): 파싱할 XML 파일의 경로
    
    Returns:
    - Dict[str, str]: 회사 이름을 키로, 고유번호를 값으로 하는 딕셔너리
    """
    try:
        print(f"XML 파일 '{xml_file_path}'을(를) 파싱 중입니다...")
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        corp_dict = {}
        for company in root.findall('list'):
            corp_name = company.findtext("corp_name")
            corp_code = company.findtext("corp_code")
            stock_code = company.findtext("stock_code")
            
            # stock_code가 비어 있지 않은 경우에만 추가
            if stock_code and stock_code.strip() and corp_name and corp_code:
                corp_dict[corp_name] = corp_code
        
        print("XML 파싱이 완료되었습니다.")
        return corp_dict
    except FileNotFoundError:
        print(f"에러: 파일을 찾을 수 없습니다. 경로를 확인하세요: {xml_file_path}")
        raise
    except ET.ParseError:
        print("에러: XML 파싱 중 문제가 발생했습니다.")
        raise
    except Exception as e:
        print(f"알 수 없는 에러가 발생했습니다: {e}")
        raise

def save_to_json(data, json_file_path):
    """
    데이터를 JSON 파일로 저장합니다.
    
    Parameters:
    - data (Dict[str, str]): JSON으로 변환할 데이터 (회사 이름: 고유번호)
    - json_file_path (str): 저장할 JSON 파일의 경로
    """
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"데이터가 성공적으로 '{json_file_path}' 파일로 저장되었습니다.")
    except Exception as e:
        print(f"JSON 파일 저장 중 에러가 발생했습니다: {e}")
        raise

def main():
    # 필요한 디렉토리 생성
    extract_path = 'corp_num'
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    
    # 회사고유번호 데이터 불러오기
    crtfc_key = '393adedf5807818f854184bdda1b10589f766f51'  # 실제 사용 시 보안에 유의하세요
    url = f'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={crtfc_key}'
    download_and_extract_xml(url, extract_path)
    
    # 압축파일 안의 xml 파일 경로
    xml_file_path = os.path.join(extract_path, 'CORPCODE.xml')
    
    # XML 파일을 딕셔너리로 변환 (corp_name: corp_code) 단, stock_code가 있는 경우만
    corp_dict = parse_xml_to_dict(xml_file_path)
    
    # JSON 파일로 저장
    json_file_path = 'corp_codes.json'
    save_to_json(corp_dict, json_file_path)
    
    # 특정 회사 이름으로 회사 고유번호 찾기 함수
    def find_corp_num(find_name, corp_dictionary):
        """
        회사 이름으로 회사 고유번호를 찾는 함수.
        
        Parameters:
        - find_name (str): 찾고자 하는 회사 이름
        - corp_dictionary (Dict[str, str]): 회사 이름을 키로, 고유번호를 값으로 하는 딕셔너리
        
        Returns:
        - str or None: 회사의 고유번호 또는 찾을 수 없을 경우 None
        """
        return corp_dictionary.get(find_name)
    
    # 예시 사용
    example_name = "삼성전자"  # 찾고자 하는 회사 이름으로 변경하세요
    corp_code = find_corp_num(example_name, corp_dict)
    if corp_code:
        print(f"회사 이름 '{example_name}'의 고유번호는 {corp_code} 입니다.")
    else:
        print(f"회사 이름 '{example_name}'을(를) 찾을 수 없습니다.")

if __name__ == "__main__":
    main()