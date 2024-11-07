import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from adjustText import adjust_text

#데이터 읽어오기
table = pd.read_csv("./beer_data_f.csv")

#필요한 컬럼 선택
beer_df = table[['trained_label', 'category', 'country_iso_alpha_3', 'alcohol', 'aroma','Flavor', 'Mouthfeel']]

#너무 세분화되어 있어서 약간의 통합
beer_df.loc[beer_df['trained_label'] == 'Somersby Apple Cider', 'category'] = 'Flavored - Fruit'

#수치형 데이터 표준화 및 범주형 데이터 원-핫 인코딩 
beer_df = pd.get_dummies(beer_df, columns=['category', 'country_iso_alpha_3'])
beer_df_num = beer_df[['alcohol','aroma','Flavor','Mouthfeel']]
beer_df[['alcohol','aroma','Flavor','Mouthfeel']] = StandardScaler().fit_transform(beer_df_num)  # 데이터 표준화

#특성 데이터 분리
X = beer_df.drop('trained_label', axis=1)

#PCA로 2차원으로 축소
pca = PCA(n_components=2)  
principal_components = pca.fit_transform(X)
principal_df = pd.DataFrame(data=principal_components, columns=['pca1', 'pca2'])
final_df = pd.concat([principal_df, beer_df[['trained_label']]], axis=1)

#K-means 클러스터링 수행
X_data = principal_df[['pca1', 'pca2']]
kmeans = KMeans(n_clusters=4, init='k-means++')
final_df['Cluster'] = kmeans.fit_predict(X_data)


#클러스터링 결과 시각화
plt.figure(figsize=(10, 7))
sns.scatterplot(data=final_df, x='pca1', y='pca2', hue='Cluster', palette='viridis', legend='full')
plt.title('K-means Clustering of Beer Data')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid()

# 각 점 위에 trained_label 값 표시 (adjust_text 사용)
texts = []
for i in range(len(final_df)):
    texts.append(plt.text(final_df['pca1'].iloc[i], final_df['pca2'].iloc[i], final_df['trained_label'].iloc[i],
                          fontsize=9, ha='center'))

# 텍스트가 겹치지 않도록 조정
adjust_text(texts, only_move={'points': 'y', 'text': 'y'}, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

plt.show()