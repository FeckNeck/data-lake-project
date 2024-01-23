import pandas as pd
import numpy as np
from langdetect import detect
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from textblob import TextBlob

# Read the data
df = pd.read_csv('./data.csv', delimiter='\t')

print(df.head())

# Detect language of each blog post
df['language'] = df['text'].apply(detect)

# remove stopwords in a new column
stop = stopwords.words('english')
df['stopwords_removed'] = df['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

# count the number of words in each blog post
df['word_count'] = df['stopwords_removed'].apply(lambda x: len(x.split()))

# count the number of characters in each blog post
df['char_count'] = df['stopwords_removed'].apply(lambda x: len(x.replace(" ","")))

# count the number sentences in each blog post
df['sentence_count'] = df['stopwords_removed'].apply(lambda x: len(x.split('.')))

# extract numerical data from the blog post
df['numerics'] = df['stopwords_removed'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))

# sentiment analysis
df['sentiment'] = df['stopwords_removed'].apply(lambda x: round(TextBlob(x).sentiment[0], 2))

# subjectivity analysis
df['subjectivity'] = df['stopwords_removed'].apply(lambda x: round(TextBlob(x).sentiment[1], 2))

print(df.head())

# save the dataframe
df.to_csv('./data_processed.csv', index=False)