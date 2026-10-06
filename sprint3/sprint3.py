import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")
print(df.head())
print("Dimensions :", df.shape)
print("\nColonnes :")
print(df.columns.tolist())

print("\nValeurs manquantes :")
print(df.isna().sum())