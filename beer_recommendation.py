# beer_recommendation.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# CSV 파일에서 데이터 로드
beer_df = pd.read_csv('beer_dataset.csv')

# 필요한 특성 선택
features = ['ABV', 'Bitter', 'Sweet', 'Sour', 'Fruits', 'Hoppy', 'Spices', 'Malty']
beer_features = beer_df[features].fillna(0)

# 특성 정규화
scaler = MinMaxScaler()
beer_features_scaled = scaler.fit_transform(beer_features)

def get_main_flavor(beer):
    flavor_features = ['Bitter', 'Sweet', 'Sour', 'Fruits', 'Hoppy', 'Spices', 'Malty']
    main_flavor = max(flavor_features, key=lambda x: beer[x])
    return main_flavor

def recommend_beers(alcohol_tolerance, bitter_rating, sweet_rating, sour_rating,
                    fruity_rating, hoppy_rating, spicy_rating, malty_rating):
    # 사용자 선호도 벡터 생성
    user_preferences = np.array([bitter_rating, sweet_rating, sour_rating,
                                 fruity_rating, hoppy_rating, spicy_rating, malty_rating])
    user_preferences_scaled = user_preferences / 5  # 0-1 스케일로 변환

    # 알코올 수용도에 따른 필터링
    if alcohol_tolerance == 'a':
        filtered_beers = beer_df[beer_df['ABV'] == 0]
    elif alcohol_tolerance == 'b':
        filtered_beers = beer_df[beer_df['ABV'] < 5]
    else:
        filtered_beers = beer_df

    # 필터링된 맥주의 특성 추출
    filtered_features = filtered_beers[features].fillna(0)
    filtered_features_scaled = scaler.transform(filtered_features)

    # 코사인 유사도 계산
    similarity_scores = cosine_similarity(user_preferences_scaled.reshape(1, -1),
                                          filtered_features_scaled[:, 1:])  # ABV 제외
    
    # 유사도 점수를 데이터프레임에 추가
    filtered_beers['similarity'] = similarity_scores[0]

    # 유사도 점수로 정렬하고 상위 3개 추천
    recommended_beers = filtered_beers.sort_values('similarity', ascending=False).head(3)

    # 결과 포맷팅
    results = []
    for _, beer in recommended_beers.iterrows():
        main_flavor = get_main_flavor(beer)
        results.append({
            'name': beer['Name'],
            'style': beer['Style'],
            'main_flavor': main_flavor,
            'abv': beer['ABV']
        })

    return results
