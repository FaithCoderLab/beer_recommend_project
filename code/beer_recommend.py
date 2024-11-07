import pandas as pd
import numpy as np

data = pd.read_csv("clustering_beer.csv")


def beer_recommend(beer_name):

    target_row = data[data['trained_label'] == beer_name]
    if target_row.empty:
        return "해당 맥주가 아직 추천리스트에 등록되지 않았습니다"
    
    # 해당 맥주의 정보 추출
    target_cluster = target_row['Cluster'].values[0]
    target_pca1 = target_row['pca1'].values[0]
    target_pca2 = target_row['pca2'].values[0]

    # 같은 클러스터만 찾아오기
    same_cluster = data[data['Cluster'] == target_cluster]

    #같은 클러스트 중에서 해당 맥주와의 거리 찾기
    same_cluster = same_cluster.copy()
    same_cluster['distance'] = np.sqrt((same_cluster['pca1'] - target_pca1) ** 2 + (same_cluster['pca2'] - target_pca2) ** 2)

    #해당 맥주가 추천되지 않도록 빼기
    same_cluster = same_cluster[same_cluster['trained_label'] != beer_name]

    nearest_beers = same_cluster.nsmallest(2, 'distance')
    #nearest_beers[['trained_label', 'pca1', 'pca2', 'Cluster', 'distance']]
    nearest_beers = nearest_beers[['trained_label']]
    rec_beers = f'추천맥주 1: {nearest_beers.values[0][0]}\n추천맥주 2: {nearest_beers.values[1][0]}'
    return rec_beers

#print(beer_recommend("hite"))



def find_beername(output: str):
    start = output.find("beer_name:") + len("beer_name: ")
    end = output.find("\n", start)
    beer_name = output[start:end].strip()
    print(beer_name)
    return beer_name

def find_beer_and_recommend(output: str):
    beer_name = find_beername(output)
    return beer_recommend(beer_name)

def find_beerdata(beer_name):
    df = pd.read_csv("DB_New(Beer).csv")
    #print(df.head())
    matching_row = df[df['trained_label'] == beer_name]
    if matching_row.empty:
        return "해당 맥주가 아직 등록되지 않았습니다 ㅠㅠ"
    matching_row = matching_row.drop(columns=["beer_id", "trained_label"])
    nice_string1 = "beer_name: " + beer_name + '\n'
    nice_string2 = '\n'.join([f"{col}: {str(val.values[0])}" for col, val in matching_row.items()])
    return nice_string1 + nice_string2


