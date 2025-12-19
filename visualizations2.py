from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

df =pd.read_csv("pets.csv")
features = ['breed', 'color', 'gender']
df_features = df[features]

encoder = OneHotEncoder(sparse_output=False)  # scikit-learn >=1.2
X_encoded = encoder.fit_transform(df_features)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_encoded)

tsne = TSNE(n_components=2, random_state=42, perplexity=10)  # adjust perplexity for dataset size
X_tsne = tsne.fit_transform(X_encoded)

from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=42, perplexity=10)  # adjust perplexity for dataset size
X_tsne = tsne.fit_transform(X_encoded)

import matplotlib.pyplot as plt
import seaborn as sns

# Example with PCA
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=df['name'], s=100)

plt.subplots_adjust(right=0.75)  
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.title("PCA of Pet Embeddings", fontname="Lucida Grande", fontsize=18, fontweight='bold')
plt.show()


# Example with t-SNE
plt.figure(figsize=(8,6))
sns.scatterplot(x=X_tsne[:,0], y=X_tsne[:,1], hue=df['name'], palette='tab20', s=100)
plt.subplots_adjust(right=0.75) 
plt.title("t-SNE of Pet Embeddings", fontname="Lucida Grande", fontsize=18, fontweight='bold')
plt.xlabel("t-SNE 1")
plt.ylabel("t-SNE 2")
plt.legend(bbox_to_anchor=(1.00005, 1), loc='upper left')
plt.show()

from matplotlib.font_manager import get_font_names

print(get_font_names())