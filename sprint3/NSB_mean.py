import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")


#Histogramme
plt.figure(figsize=(10, 5))

plt.hist(df["NSB_mean"].dropna(), bins=15)

plt.xlabel("NSB_mean (mag/arcsec²)")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de NSB_mean")
plt.show()

#Valeurs principalement concentrées autour de 21,20–21,25 mag/arcsec²,
# La quasi-totalité des nuits se situe entre 21,05 et 21,35 mag/arcsec²
# la distribution de NSB_mean est globalement concentrée

#Statistique descriptive
print(df["NSB_mean"].describe())

#Valeur atypique
Q1 = df["NSB_mean"].quantile(0.25)
Q3 = df["NSB_mean"].quantile(0.75)

IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

print("Q1 :", Q1)
print("Q3 :", Q3)
print("IQR :", IQR)
print("Borne inférieure :", borne_inf)
print("Borne supérieure :", borne_sup)
valeurs_atypiques = df[
    (df["NSB_mean"] < borne_inf) |
    (df["NSB_mean"] > borne_sup)
]

print("\nNombre de valeurs atypiques :", len(valeurs_atypiques))
print(valeurs_atypiques[["night_id", "NSB_mean"]])