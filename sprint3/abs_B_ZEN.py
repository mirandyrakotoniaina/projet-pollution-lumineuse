import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")

plt.figure(figsize=(10, 5))

plt.hist(df["abs_B_ZEN"].dropna(), bins=15)

plt.xlabel("Valeur absolue de B_ZEN")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs des valeurs absolues de B_ZEN")
plt.show()