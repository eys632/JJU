from loader_splitter_evaluator import LoaderSplitterEvaluator

def main():
    try:
        # 평가기 초기화
        evaluator = LoaderSplitterEvaluator()
        
        # 테스트할 파일 경로
        test_file = "C:\Python_workspace\bit\sub\data_all\data\자기소개서.md"
        
        print(f"파일 '{test_file}' 분석 중...")
        results = evaluator.evaluate_all_combinations(test_file)
        
        if not results:
            print("사용 가능한 로더/스플리터 조합을 찾을 수 없습니다.")
            return
            
        # 결과 출력
        print("\n=== 평가 결과 ===")
        evaluator.print_results(results)
        
        # 최적의 조합 출력
        best_result = results[0]
        print("\n최적의 조합:")
        print(f"로더: {best_result['loader']}")
        print(f"스플리터: {best_result['splitter']}")
        print(f"점수: {best_result['score']}/100")
        
    except Exception as e:
        print(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    main()
