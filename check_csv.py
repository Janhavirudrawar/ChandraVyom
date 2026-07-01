import pandas as pd

df = pd.read_csv("data/Delhi_UHI_Training_Data.csv")

print(df.shape)
print(df.columns)
print(df.head())