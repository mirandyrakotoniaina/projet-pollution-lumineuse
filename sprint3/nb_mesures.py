import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")

plt.figure(figsize=(10, 5))

plt.hist(df["nb_mesures"].dropna(), bins=15)

plt.xlabel("nombre de mesures")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de nb_mesures")
plt.show()