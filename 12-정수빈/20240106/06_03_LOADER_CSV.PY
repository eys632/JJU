from langchain.document_loaders import UnstructuredFileLoader
from xml.etree.ElementTree import Element, SubElement, tostring
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 데이터 로드
file_path = "boston.csv"

# UnstructuredFileLoader를 사용해 데이터 로드
loader = UnstructuredFileLoader(file_path)
docs = loader.load()

# 상위 10개 데이터 추출
top_docs = docs[:10]

# XML 생성 함수
def create_xml(docs):
    root = Element("data")
    for i, doc in enumerate(docs):
        row_elem = SubElement(root, "row", id=str(i + 1))
        for line in doc.page_content.split("\n"):
            if "." in line:
                key, value = map(str.strip, line.split(".", 1))
                col_elem = SubElement(row_elem, key.replace(".", "_"))
                col_elem.text = value
    return root

# XML 생성
xml_root = create_xml(top_docs)

# XML 문자열로 변환 및 출력
xml_str = tostring(xml_root, encoding="unicode")
print(xml_str)

# XML 파일로 저장 (선택 사항)
output_path = "boston_top10.xml"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(xml_str)

print(f"XML 파일이 저장되었습니다: {output_path}")

# CSV 데이터 로드
data = pd.read_csv(file_path)

# 상관계수 계산 및 상위 3개 변수 선택
correlation = data.corr()
target_correlation = correlation['MEDV'].abs().sort_values(ascending=False)  # MEDV가 주택 가격을 의미한다고 가정
top_features = target_correlation.index[1:4]  # 상위 3개의 변수 선택 (MEDV 제외)

print("주택 가격에 영향을 주는 상위 3가지 요소:", top_features.tolist())

# 상관관계 히트맵 그리기
plt.figure(figsize=(8, 6))
sns.heatmap(data[top_features.tolist() + ['MEDV']].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap of Top Features")
plt.show()

# 회귀 모델 구축
X = data[top_features]
y = data['MEDV']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# 회귀 모델 결과
y_pred = model.predict(X_test)

# 모델 평가
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R-squared (R2): {r2:.2f}")

# 실제 값과 예측 값 비교
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red", linestyle="--")
plt.xlabel("Actual MEDV")
plt.ylabel("Predicted MEDV")
plt.title("Actual vs Predicted MEDV")
plt.grid(alpha=0.3)
plt.show()

# 상위 변수와 주택 가격의 관계 시각화
for feature in top_features:
    plt.figure(figsize=(8, 6))
    plt.scatter(data[feature], data['MEDV'], alpha=0.7, edgecolors='k')
    plt.title(f"{feature} vs MEDV")
    plt.xlabel(feature)
    plt.ylabel("MEDV")
    plt.grid(alpha=0.3)
    plt.show()
