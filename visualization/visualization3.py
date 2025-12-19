import pandas as pd 
import numpy as np
import openpyxl
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import make_pipeline

df=pd.read_excel("Responses.xlsx")
print(df.head())
#print(df.columns)

df_renamed = df.rename(columns={'What are some qualities/traits (size, color, personality) you look for in a cat if you were to adopt one? 🐈‍⬛': 'TEXT'})
print(df_renamed.columns)
text = ' '.join(df_renamed['TEXT']) 
wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
#Bilinear interpolation is a method of smoothing an image when it is displayed at a resolution different from its original size.
plt.axis('off')  # Turn off axis
plt.show()

#df2=df['tweet_text']

####################################
