# -*- coding: utf-8 -*-
"""Text Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Df3n4lueRrKJhoiNA3tP3EOf5hrIrF6d
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

!pip install vaderSentiment

# Commented out IPython magic to ensure Python compatibility.
# For visualizations
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import seaborn as sns

# For Data Pre-processing
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from textblob import Word, TextBlob
from wordcloud import WordCloud , STOPWORDS

# For topic modeling
#from sklearn.decomposition import NMF, LatentDirichletAllocation

# For sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

df = pd.read_csv('Airline_review_knn_imputed.csv')

df.head()

def replace(text):            # Define a function to clean the text
    text = re.sub(r'[^A-Za-z]+', ' ', str(text)) # Replaces all special characters and numericals with blanks and leaving the alphabets
    return text


# Cleaning the text in the review column
df['Review']= df["Review"].apply(replace)
df.head()
#converting in lower case
df['Review'] = df['Review'].str.lower()
#removing punctuation
df['Review'] = df['Review'].str.replace('[^\w\s]', '')
#removing numbers
df['Review'] = df['Review'].str.replace('\d', '')

text = " ".join(i for i in df.Review)
wordcloud = WordCloud(background_color='white').generate(text)
fig = plt.figure(1, figsize=(20, 12))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

def vadersentimentanalysis(review):
    vs = analyzer.polarity_scores(review)
    return vs['compound']

df['Sentiment'] = df['Review'].apply(vadersentimentanalysis)


def vader_analysis(compound):
    if compound >= 0.5:
        return 'Positive'
    elif compound < 0 :
        return 'Negative'
    else:
        return 'Neutral'
df['Analysis'] = df['Sentiment'].apply(vader_analysis)
df.head()

analysis = df['Analysis'].value_counts()
analysis

plt.figure(figsize=(25,7))
plt.subplot(1,3,2)
plt.title("Sentiments based on Reviews")
plt.pie(analysis.values, labels = analysis.index, explode = (0.01, 0.01, 0.01), autopct='%1.1f%%', shadow=False , colors=('#ff9999', '#66b3ff', '#ffcc99'), startangle=90)
plt.show()

plt.figure(figsize=(8, 6))
plt.hist(df['Overall_Rating'], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Histogram of Overall Ratings')
plt.xlabel('Overall Rating')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# 排列rating值顺序，包括'n'的情况
rating_order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'n']

# 按照顺序绘制直方图
plt.figure(figsize=(8, 6))
df['Overall_Rating'] = df['Overall_Rating'].astype(str)  # 将rating转换为字符串类型
df['Overall_Rating'].value_counts().reindex(rating_order).plot(kind='bar', color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Histogram of Overall Ratings')
plt.xlabel('Overall Rating')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

airline_counts = df['Airline Name'].value_counts()

# Bar chart for number of reviews by airline
plt.figure(figsize=(10, 6))
airline_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Reviews by Airline')
plt.xlabel('Airline')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Function to calculate sentiment score
def get_sentiment_score(text):
    return analyzer.polarity_scores(text)['compound']

# Calculate sentiment score for each review
df['Sentiment Score'] = df['Review'].apply(get_sentiment_score)

# Define threshold for positive sentiment
positive_threshold = 0.05

# Mark reviews with positive sentiment based on the threshold
df['Positive'] = df['Sentiment Score'] > positive_threshold

# the top 10 largest airlines in 2024 by revenue
top_10_airlines = [
    'Delta Air Lines', 'American Airlines', 'United Airlines', 'Lufthansa',
    'Emirates', 'Air France', 'Singapore Airlines', 'Southwest Airlines',
    'Turkish Airlines', 'China Southern Airlines'
]

# Filter the dataset for the top 10 airlines
filtered_df = df[df['Airline Name'].isin(top_10_airlines)]

# Count the number of positive reviews for each airline
positive_airline_counts = filtered_df[filtered_df['Positive']]['Airline Name'].value_counts()

# Bar chart for number of positive reviews by the top 10 airlines
plt.figure(figsize=(10, 6))
positive_airline_counts.plot(kind='bar', color='lightblue')
plt.title('Number of Positive Reviews by Top 10 Airlines')
plt.xlabel('Airline')
plt.ylabel('Number of Positive Reviews')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Calculate average ratings for each aspect
average_ratings = df[['Seat Comfort', 'Cabin Staff Service', 'Food & Beverages', 'Inflight Entertainment', 'Value For Money']].mean()

# Plotting
plt.figure(figsize=(10, 6))
average_ratings.plot(kind='bar', color='skyblue')
plt.title('Average Ratings of Different Aspects')
plt.xlabel('Aspect')
plt.ylabel('Average Rating')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Set the style of the seaborn plot
sns.set_style("whitegrid")

# Create the violin plot
plt.figure(figsize=(12, 8))
sns.violinplot(x='Airline Name', y='Overall_Rating', data=filtered_df, palette='muted')
plt.title('Distribution of Overall Ratings Across Airlines')
plt.xlabel('Airline')
plt.ylabel('Overall Rating')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

numeric_df = df.select_dtypes(include=['int64', 'float64'])

# Compute the correlation matrix
correlation_matrix = numeric_df.corr()

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")

# Set the title
plt.title('Correlation Matrix of Airline Reviews Features')

# Show the plot
plt.show()

df['Airline Name'].value_counts().reset_index()