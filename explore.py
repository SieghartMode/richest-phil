import pandas as pd
import csv

csv_path = 'data.csv'
data = pd.read_csv(csv_path, sep=',')
print(data.head())
