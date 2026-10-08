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

#La distribution de NSB_max s'étend approximativement de 21,09 à 21,56 mag/arcsec²
#Les valeurs sont principalement concentrées entre 21,31 et 21,43 mag/arcsec², avec un pic autour de 21,34–21,37 mag/arcsec² correspondant environ 19 nuits


#Statistique descriptive
print(df["NSB_max"].describe())

#Valeur atypique
Q1 = df["NSB_max"].quantile(0.25)
Q3 = df["NSB_max"].quantile(0.75)

IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

print("Q1 :", Q1)
print("Q3 :", Q3)
print("IQR :", IQR)
print("Borne inférieure :", borne_inf)
print("Borne supérieure :", borne_sup)
valeurs_atypiques = df[
    (df["NSB_max"] < borne_inf) |
    (df["NSB_max"] > borne_sup)
]

print("\nNombre de valeurs atypiques :", len(valeurs_atypiques))
print(valeurs_atypiques[["night_id", "NSB_max"]])