import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")


#Histogramme (Dans quelle mesure les valeurs centrales du NSB varient-elles au cours d'une nuit, et cette variabilité est-elle similaire d'une nuit à l'autre ?)
plt.figure(figsize=(10, 5))

plt.hist(df["NSB_IQR_night"].dropna(), bins=15)

plt.xlabel("NSB_IQR_night")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de NSB_IQR_night")
plt.show()

#La distribution de NSB_IQR_night s'étend approximativement de 0,02 et 0,22 mag/arcsec²
#La concentration maximale se situe autour de 0,08–0,11 mag/arcsec²

#Statistique descriptive
print(df["NSB_IQR_night"].describe())

#Valeur atypique
Q1 = df["NSB_IQR_night"].quantile(0.25)
Q3 = df["NSB_IQR_night"].quantile(0.75)

IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

print("Q1 :", Q1)
print("Q3 :", Q3)
print("IQR :", IQR)
print("Borne inférieure :", borne_inf)
print("Borne supérieure :", borne_sup)
valeurs_atypiques = df[
    (df["NSB_IQR_night"] < borne_inf) |
    (df["NSB_IQR_night"] > borne_sup)
]

print("\nNombre de valeurs atypiques :", len(valeurs_atypiques))
print(valeurs_atypiques[["night_id", "NSB_IQR_night"]])