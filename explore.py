import pandas as pd
import csv

csv_path = 'data.csv'
data = pd.read_csv(csv_path, sep=',', parse_dates = ['Joined', 'Date posted'])

# Removing irrelevant rows and columns
data = data.dropna(subset=['Timestamp']) # empty rows
data = data.dropna(axis=1, how='all') # empty columns
data = data.drop(axis=1, columns=['ID', 'Timestamp', 'Tweet URL', 'Group', 'Collector', 'Category', 'Topic', 'Screenshot', 'Reasoning', 'Remarks']) # columns with irrelevant data
data = data.drop(axis=1, columns=['Tweet Translated', 'Quote Tweets', 'Views']) # columns which are mostly empty

# impute missing bio and location
data['Account bio'].fillna('NO BIO', inplace=True)
data['Location'].fillna('NO LOCATION', inplace=True)

for col in data:
  if col in ['Following', 'Followers', 'Likes', 'Replies', 'Retweets']:
    data[col] = data[col].astype('int')
  elif col!='Date posted':
    data[col] = data[col].astype('category')
print("Column types:")
print(data.dtypes)
print()

print("Number of empty values per column:")
print(data.isnull().sum())
print()

keywords_list = set([phrase.lower() for phrase in set(data['Keywords'])])
keyword_set = sorted(set([word for phrase in keywords_list for word in phrase.split()]))
print("Keywords used:")
print(keyword_set)
print()

tweet_type_list = [typ.lower().strip() for value in data['Tweet Type'] for typ in value.split(',')]
print("Number of each tweet type:")
print(pd.DataFrame(tweet_type_list).value_counts())
print()

print("Number of each content type:")
print(data['Content type'].value_counts())
print()

print("Numerical data statistics:")
print(data.describe(datetime_is_numeric=True))

data.to_csv('./preprocessed.csv')
