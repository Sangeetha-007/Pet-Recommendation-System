# Pet Recommendation System

<!--Developed an end-to-end recommendation pipeline using scraped pet profile data. The system transforms unstructured textual descriptions into structured embeddings and applies cosine similarity to identify similar pets. Visualization with PCA and t-SNE validates the embedding space and supports recommendation quality analysis. -->

Developed an end-to-end recommendation pipeline using scraped pet profile data. The system transforms unstructured textual descriptions into structured embeddings and applies cosine similarity to identify similar pets. Visualization with PCA and t-SNE validates the embedding space and supports recommendation quality analysis.

## Technologies Used
* Python: pandas, NumPy, Selenium, Matplotlib, seaborn
* scikit-learn: Used for model evaluation and train/test splitting

## Data Used
This project uses data scraped from Sean Casey Animal Rescue. The final dataset can be found in pets.csv

## Training the Model
The model used to predict was done with Cosine Similarity, visualized with PCA and t-SNE. 
<!--
The code used to train the model can be found in the src/model.ipynb notebook. These were the main steps involved in training the model:

Train-Test Split
A GroupShuffleSplit was used to ensure that data from the same session was kept together in either the train or test set. This was to ensure that there would be no data leakage and the model would be able to evaluate race sessions effectively.
Model Configuration
The specific parameters used can be found in the code.
The model is trained with the rank:pairwise objective, essentially comparing pairs of drivers. This specific method focuses on predicting the correct order of drivers rather than their exact finishing positions. In a use case such as Formula 1, where only the top 10 drivers (out of 20 drivers) earn points, predicting the relative position of drivers is more impactful than exact placement The training data is also well-aligned with this method as it allows the model to compare qualifying and telemetry data among drivers.
The histogram-based tree method was used for this model as it is faster and uses less memory compared to the exact algorithm.
Hyperparameter Optimization
Hyperparameters such as max_depth, learning_rate, and subsample were tuned using Optuna.
Training
The model was trained by grouping each qualifying session to compare drivers within the same race.
Metrics and Model Performance
The model was evaluated using Normalized Discounted Cumulative Gain (NDCG), Spearman's Rank Correlation, Mean Reciprocal Rank, and Top-K Precision/Recall/F1 scores. These metrics were chosen as they are widely used for ranking and recommendation systems, and are well-suited to evaluate ranking models.

Normalized Discounted Cumulative Gain (NDCG)

Measures the quality ranking by giving more weight to the correct placement of top drivers.
Average NDCG: 0.922
A score close to 1.0 indicates that the model is ranking the top drivers accurately.
Spearman's Rank Correlation

Evaluates how well the predicted ranking order matches the actual finishing order.
Average SRC: 0.613
A value above 0.6 indicates a moderate to strong correlation between the predicted and actual order.
Mean Reciprocal Rank (MRR)

Calculates the average of reciprocal ranks of the winner.
Mean Reciprocal Rank: 0.7
A score of 0.70 means that, on average, the actual race winner was ranked highly by the model, usually among the top 2 predictions. In a Formula 1 context, this indicates a strong performance by the model. Predicting the race winner is crucial because of the significant point different between the winner and the rest of the drivers.
Top-K Precision / Recall / F1 Score

Measures how well the model predicts the top drivers (Winner, Top 3, Top 10)
Winner Precision/Recall/F1: 0.538
Top 3 Precision/Recall/F1: 0.675
Top 10 Precision/Recall/F1: 0.774
These values indicate that the model correctly predicts the winner over 53% of the time, and correctly predicts the top 10 over 77% of the time. This level of accuracy indicates a strong performance for a multi-class ranking problem with 20 drivers and multiple external factors like weather, crashes, and driver errors.
Note: It is expected for the precision and recall to be equivalent as the scores are computed with a fixed Top-K set of drivers.
Using the Model for 2025 Predictions
The model has been trained on the 2019-2024 seasons. The 2025 season brought in numerous changes including 6 new rookie drivers, changes in regulations, etc.

In order to predict 2025 races outcomes, use the src/predictions_2025.ipynb notebook.

Installing
Clone the repository
git clone https://github.com/snehavin/F1-RankingModel.git
cd F1-RankingModel
Install dependencies
pip install -r requirements.txt
Create dataset using this notebook. Or, use the existing dataset

Train the model using this notebook. Or, load the existing model

Make predictions on the 2025 season using this notebook! -->

## Limitations & Future Improvements
The Sean Casey Animal Rescue site only had 17 cat profiles during the time of the scrape. The PCA and t-SNE visualizations would provide better insights if there were more profiles to scrape. 
Other animal shelter sites prevented scraping their data due to security reasons. 
<!--While the model demonstrates stong performance on 2019-2024 data, there are several limitations and opportunities for future improvement.

Formula 1 Uncertainty: There is so much data that Formula 1 race engineers utilize to make predictions and inform racing strategy. Though this model uses a variety of data across qualifying, telemetry, and weather factors, there are racing circumstances that cannot be captured including crashes, driver errors, safety cars, unexpected weather changes, etc.
Changes with 2025 Season: The 2025 Formula 1 season has introduced numerous changes in driver lineups, car performance, and regulations that were not seen in the training data from 2019-2024. This introduces additional uncertainty when making predictions on currect races.
Future Improvements:

Implement automated retraining after each race to continuously improve predictions and introduce 2025 data to the model.
Incorporate additional data from FastF1 including tire compound data, pit strategy, etc.  -->
