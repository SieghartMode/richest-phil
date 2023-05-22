import pandas as pd
import csv
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

csv_path = 'data.csv'
data = pd.read_csv(csv_path, sep=',', parse_dates = ['Date posted'], dayfirst=True)

def date_to_bin(date):
  return 12 * (date.year - 2016) + date.month - 1
data['Bin'] = data['Date posted'].dt.date.map(date_to_bin)

count_bins = [[0] * 12 for i in range(7)]
for i in range(7):
  for j in range(12):
    count_bins[i][j] = (data['Bin'] == 12 * i + j).sum()
print(count_bins)

# Removing irrelevant rows and columns
data = data.dropna(subset=['Timestamp']) # empty rows
data = data.dropna(axis=1, how='all') # empty columns
data = data.drop(axis=1, columns=['ID', 'Timestamp', 'Tweet URL', 'Group', 'Collector', 'Category', 'Topic', 'Screenshot', 'Reasoning', 'Remarks']) # columns with irrelevant data
data = data.drop(axis=1, columns=['Tweet Translated', 'Quote Tweets', 'Views']) # columns which are mostly empty

data = data.drop(labels=[18,23,48,103,109,150])
data = data.reset_index(drop = True)

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

columns = ['Following', 'Followers', 'Likes', 'Replies', 'Retweets']
for column_name in columns: 
  data['{}_zscore'.format(column_name)] = stats.zscore(data[column_name])

category_mapping = {
   'Identified': 0,
   'Anonymous': 1,
   'Media': 2
}

data['Account type'] = data['Account type'].map(category_mapping)
data['Text'] = data['Tweet Type'].str.contains('Text').astype(int)
data['Image'] = data['Tweet Type'].str.contains('Image').astype(int)
data['Video'] = data['Tweet Type'].str.contains('Video').astype(int)
data['URL'] = data['Tweet Type'].str.contains('URL').astype(int)
data['Reply'] = data['Tweet Type'].str.contains('Reply').astype(int)

category_mapping = {
   'Rational': 0,
   'Emotional': 1,
   'Transactional': 2
}

data['Content type'] = data['Content type'].map(category_mapping)

count_bins = [[0] * 12 for i in range(7)]
for i in range(7):
  for j in range(12):
    count_bins[i][j] = (data['Bin'] == 12 * i + j).sum()

# see if tweet was posted during campaign period
start_date_2016 = pd.to_datetime('2016-01-01 00:00:00')
end_date_2016 = pd.to_datetime('2016-05-09 23:59:59')

start_date_2019 = pd.to_datetime('2018-10-12 00:00:00')
end_date_2019 = pd.to_datetime('2019-05-13 23:59:59')

start_date_2022 = pd.to_datetime('2021-10-01 00:00:00')
end_date_2022 = pd.to_datetime('2022-05-09 23:59:59')

data['Date posted'] = pd.to_datetime(data['Date posted'])

data['Elections'] = data['Date posted'].apply(lambda x: 1 if (start_date_2016 <= x <= end_date_2016) or 
                                                                  (start_date_2019 <= x <= end_date_2019) or 
                                                                  (start_date_2022 <= x <= end_date_2022) 
                                                                  else 0)

# Heatmap
fig, ax = plt.subplots()
im = ax.imshow(count_bins)

ax.set_yticks(ticks=range(7), labels=range(2016,2023))
ax.set_xticks(ticks=range(12), labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Non','Dec'])
for i in range(7):
  for j in range(12):
    count = (data['Bin'] == 12 * i + j).sum()
    count_bins[i][j] = count
    ax.text(j, i, count, ha="center", va="center", color="w")
plt.show()

data.to_csv('./preprocessed.csv')
