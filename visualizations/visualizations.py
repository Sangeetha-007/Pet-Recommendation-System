import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
import sklearn
import seaborn as sns
import matplotlib.pyplot as plt

df =pd.read_csv("pets.csv")
# Example features
features = ['breed', 'color']  # you can add more
df_features = df[features]

# One-hot encode categorical features
encoder = OneHotEncoder(sparse_output=False)
X_encoded = encoder.fit_transform(df_features)


# Compute similarity matrix
similarity_matrix = cosine_similarity(X_encoded)


# Select subset of pets to visualize (optional)
selected_idx = [0, 1, 2, 3, 4]  # indices of pets to show
sim_subset = similarity_matrix[selected_idx][:, selected_idx]

# Get pet names for labels
pet_names = df.iloc[selected_idx]['name']

plt.figure(figsize=(8,6))
sns.heatmap(sim_subset, annot=True, xticklabels=pet_names, yticklabels=pet_names, cmap="YlGnBu", fmt=".2f")
plt.title("Cosine Similarity Heatmap of Cats", fontweight='bold', fontsize=18)
plt.show()
