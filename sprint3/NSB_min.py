import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")

#Histogramme (À quel niveau de luminosité le ciel descend-il au minimum au cours des différentes nuits ?)
plt.figure(figsize=(10, 5))

plt.hist(df["NSB_min"].dropna(), bins=15)

plt.xlabel("NSB_min")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de NSB_min")
plt.show()

#La distribution de NSB_min s'étend approximativement de 19,5 à 21,35 mag/arcsec².
#La majorité des nuits présente une valeur minimale concentrée autour de 20,85–21,00 mag/arcsec², avec un pic d'environ 30 nuits.

#Statistique descriptive
print(df["NSB_min"].describe())

#Valeur atypique
Q1 = df["NSB_min"].quantile(0.25)
Q3 = df["NSB_min"].quantile(0.75)

IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

print("Q1 :", Q1)
print("Q3 :", Q3)
print("IQR :", IQR)
print("Borne inférieure :", borne_inf)
print("Borne supérieure :", borne_sup)
valeurs_atypiques = df[
    (df["NSB_min"] < borne_inf) |
    (df["NSB_min"] > borne_sup)
]

print("\nNombre de valeurs atypiques :", len(valeurs_atypiques))
print(valeurs_atypiques[["night_id", "NSB_min"]])