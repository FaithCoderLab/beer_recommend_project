# Azure의 Custom Vision 라이브러리를 추가. 예측을 위하여 prediction을 포함
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
# OpenAPI 스펙에 맞춰서 Authentication을 처리할 수 있도록 해주는 코드
from msrest.authentication import ApiKeyCredentials
from io import BytesIO
from PIL import Image

# 사용자가 만든 AI 모델의 예측 기능을 사용하기 위한 endpoint 지정
prediction_endpoint = "https://5a046customvision-prediction.cognitiveservices.azure.com"
 # KEY 값 지정
prediction_key = "3hhcv8lZ8O9ocDydwdejP1Rvlw1biY58z0zgsDr4LLfZyuBUPUEgJQQJ99AJACYeBjFXJ3w3AAAIACOG0Z9Z"
 # 프로젝트 ID 지정
project_id = "0129dd02-9b71-4b9b-bc5b-0c7c636b6056"
 # 모델명 지정
model_name = "test"

 # 앞에서 지정한 API KEY를 써서 커스텀 비전 모델을 사용할 클라이언트를 인증
credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
 # endpoint를 써서 클라이언트 등록
predictor = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)

# 테스트 이미지를 Codespace workspace에 추가한 후 image_file 변수로 지정
#image_file = "images/captured_photo.jpg"

def find_drink(image_data):
    # 테스트 이미지를 열고 모델에 적용해서 결과를 저장
    max_size = (800, 800)
    image_data.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    buffer = BytesIO()
    image_data.save(buffer, format="png")  # Use appropriate format (JPEG/PNG)
    image_bytes = buffer.getvalue()

    results = predictor.classify_image(project_id, model_name, image_bytes)
        # 예측한 결과를 출력
    # for prediction in results.predictions[:2]:
    #     print(f"Tag: {prediction.tag_name}, Probability: {prediction.probability:.2f}")
    return results.predictions[0].tag_name, results.predictions[0].probability

if __name__ == "__main__":
    image_file = "images/captured_photo.jpg"
    print(find_drink(image_file))