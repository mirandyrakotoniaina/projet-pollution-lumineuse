import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")

#Histogramme
plt.figure(figsize=(10, 5))

plt.hist(df["NSB_median_night"].dropna(), bins=15)

plt.xlabel("NSB_median_night (mag/arcsec²)")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de NSB_median_night")
plt.show()


#Valeurs principalement concentrées autour de 21,12–21,38 mag/arcsec², avec un maximum de fréquence autour de 21,25 mag/arcsec².
#Valeurs faibles -> ciel relativement plus lumineux
#Valeurs élevées -> ciel relativement plus sombre

#Statistique descriptive
print(df["NSB_median_night"].describe())

#Valeur atypique
Q1 = df["NSB_median_night"].quantile(0.25)
Q3 = df["NSB_median_night"].quantile(0.75)

IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

print("Q1 :", Q1)
print("Q3 :", Q3)
print("IQR :", IQR)
print("Borne inférieure :", borne_inf)
print("Borne supérieure :", borne_sup)
valeurs_atypiques = df[
    (df["NSB_median_night"] < borne_inf) |
    (df["NSB_median_night"] > borne_sup)
]

print("\nNombre de valeurs atypiques :", len(valeurs_atypiques))
print(valeurs_atypiques[["night_id", "NSB_median_night"]])