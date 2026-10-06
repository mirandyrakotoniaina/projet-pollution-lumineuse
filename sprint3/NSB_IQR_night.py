import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")

plt.figure(figsize=(10, 5))

plt.hist(df["NSB_IQR_night"].dropna(), bins=15)

plt.xlabel("NSB_IQR_night")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de NSB_IQR_night")
plt.show()