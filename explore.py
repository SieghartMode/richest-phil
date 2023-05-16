import pandas as pd
import csv

csv_path = 'data.csv'
data = pd.read_csv(csv_path, sep=',')

# Removing irrelevant rows and columns
data = data.dropna(subset=['Timestamp']) # empty rows
data = data.dropna(axis=1, how='all') # empty columns
data = data.drop(axis=1, columns=['ID', 'Timestamp', 'Tweet URL', 'Group', 'Collector', 'Category', 'Topic', 'Screenshot', 'Reasoning', 'Remarks']) # columns with irrelevant data
data = data.drop(axis=1, columns=['Quote Tweets', 'Views']) # columns which are mostly empty

print("Number of empty values per column:")
print(data.isnull().sum())
print("\n")

keywords_list = set([phrase.lower() for phrase in set(data['Keywords'])])
keyword_set = sorted(set([word for phrase in keywords_list for word in phrase.split()]))
print("Keywords used:")
print(keyword_set)
