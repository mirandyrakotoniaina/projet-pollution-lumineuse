import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")

plt.figure(figsize=(10, 5))

plt.hist(df["year_decimal"].dropna(), bins=15)

plt.xlabel("year_decimal")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de year_decimal")
plt.show()