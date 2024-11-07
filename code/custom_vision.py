# Azure의 Custom Vision 라이브러리를 추가. 예측을 위하여 prediction을 포함
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
# OpenAPI 스펙에 맞춰서 Authentication을 처리할 수 있도록 해주는 코드
from msrest.authentication import ApiKeyCredentials
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

# 사용자가 만든 AI 모델의 예측 기능을 사용하기 위한 endpoint 지정
prediction_endpoint = os.getenv("PREDICTION_ENDPOINT")
 # KEY 값 지정
prediction_key = os.getenv("PREDICTION_KEY")
 # 프로젝트 ID 지정
project_id = os.getenv("PROJECT_ID")
 # 모델명 지정
model_name = os.getenv("MODEL_NAME")

# 앞에서 지정한 API KEY를 써서 커스텀 비전 모델을 사용할 클라이언트를 인증
credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
# endpoint를 써서 클라이언트 등록
predictor = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)



def find_drink(image_data):
    # 테스트 이미지를 줄이기
    max_size = (800, 800)
    image_data.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    #해당 이미지를 bytes로 바꿔줌
    buffer = BytesIO()
    image_data.save(buffer, format="png")
    image_bytes = buffer.getvalue()

    results = predictor.classify_image(project_id, model_name, image_bytes)
    # 예측한 결과를 출력
    return find_beerdata(results.predictions[0].tag_name, results.predictions[0].probability)

def find_beerdata(beer_name, percentage):
    if percentage < 0.5:
        return "인식이 잘 되지 않았네요 ㅠㅠ 정면이 잘 보이게 다시 한번 찍어주세요" + str(beer_name) + str(percentage)
    df = pd.read_csv("DB_New(Beer).csv")
    #print(df.head())
    matching_row = df[df['trained_label'] == beer_name]
    if matching_row.empty:
        return "해당 맥주가 아직 등록되지 않았습니다"
    matching_row = matching_row.drop(columns=["beer_id", "trained_label"])
    nice_string1 = "beer_name: " + beer_name + '\n'
    nice_string2 = '\n'.join([f"{col}: {str(val.values[0])}" for col, val in matching_row.items()])
    nice_string3 = '\n' + "percentage: " + str(percentage)
    return nice_string1 + nice_string2 + nice_string3


#find_beerdata("cc", 1.0)