import pandas as pd
import numpy as np
#import sklearn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

df = pd.read_csv('pets.csv')
#print(df.head())


# Create text corpus (description + breed + attributes)
df["content"] = df["breed"] + " " + df["color"]
#print(df["content"])

# Convert text into vectors, Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['content'])
print(tfidf_matrix.shape)

# Compute similarity
similarity_matrix = cosine_similarity(tfidf_matrix)
#print(df['pet_id'].head(5))


# Recommendation function
def recommend(pet_id, n=5):
    # print(pet_id in df['pet_id'].values)
    # print(df['pet_id'].dtype)
    # print(type(pet_id))
    # print("pet_id =", pet_id)

    idx = df.index[df['pet_id'] == pet_id][0]
    scores = list(enumerate(similarity_matrix[idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    recommended_idx = [i[0] for i in sorted_scores[1:n+1]]
    print (df.iloc[recommended_idx])
    #print(df.iloc[recommended_idx].size)  #prints the total size (rows *columns)
    return df.iloc[recommended_idx]  #prints the recommended pets
 
recommend(pet_id=59837509, n=5)




