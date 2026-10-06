import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")

#Histogramme(Quel niveau de ciel le plus sombre est atteint au cours des différentes nuits ?)
plt.figure(figsize=(10, 5))

plt.hist(df["NSB_max"].dropna(), bins=15)

plt.xlabel("NSB_max")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de NSB_max")
plt.show()