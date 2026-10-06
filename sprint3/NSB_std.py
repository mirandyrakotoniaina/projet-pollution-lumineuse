import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")


#Histogramme (à quel point les valeurs de NSB varient autour de leur moyenne pendant la nuit.)
plt.figure(figsize=(10, 5))

plt.hist(df["NSB_std"].dropna(), bins=15)

plt.xlabel("NSB_std")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de NSB_std")
plt.show()

# La distribution de NSB_std s'étend approximativement de 0,01 à 0,35 mag/arcsec² et présente une asymétrie à droite
# La majorité des nuits présentent un NSB_std compris entre 0,06 et 0,10, avec un maximum de fréquence autour de 0,06–0,08.


#Statistique descriptive
print(df["NSB_std"].describe())

#Valeur atypique
Q1 = df["NSB_std"].quantile(0.25)
Q3 = df["NSB_std"].quantile(0.75)

IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

print("Q1 :", Q1)
print("Q3 :", Q3)
print("IQR :", IQR)
print("Borne inférieure :", borne_inf)
print("Borne supérieure :", borne_sup)
valeurs_atypiques = df[
    (df["NSB_std"] < borne_inf) |
    (df["NSB_std"] > borne_sup)
]

print("\nNombre de valeurs atypiques :", len(valeurs_atypiques))
print(valeurs_atypiques[["night_id", "NSB_std"]])