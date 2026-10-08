import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")

#Histogramme
plt.figure(figsize=(10, 5))

plt.hist(df["year_decimal"].dropna(), bins=15)

plt.xlabel("year_decimal")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de year_decimal")
plt.show()

#les observations couvrent environ 2022 à 2025
#on observe des périodes sans observation
#les deux concentrations importantes sont autour de 2022.4–2022.6 et 2024.4–2024.6

#Statistique descriptive
print(df["year_decimal"].describe())

#Valeur atypique
Q1 = df["year_decimal"].quantile(0.25)
Q3 = df["year_decimal"].quantile(0.75)

IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

print("Q1 :", Q1)
print("Q3 :", Q3)
print("IQR :", IQR)
print("Borne inférieure :", borne_inf)
print("Borne supérieure :", borne_sup)
valeurs_atypiques = df[
    (df["year_decimal"] < borne_inf) |
    (df["year_decimal"] > borne_sup)
]

print("\nNombre de valeurs atypiques :", len(valeurs_atypiques))
print(valeurs_atypiques[["night_id", "year_decimal"]])