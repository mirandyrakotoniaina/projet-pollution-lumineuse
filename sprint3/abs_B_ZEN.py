import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")

#Histogramme
plt.figure(figsize=(10, 5))

plt.hist(df["abs_B_ZEN"].dropna(), bins=15)

plt.xlabel("Valeur absolue de B_ZEN")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs des valeurs absolues de B_ZEN")
plt.show()


#Statistique descriptive
print(df["abs_B_ZEN"].describe())

#Valeur atypique
Q1 = df["abs_B_ZEN"].quantile(0.25)
Q3 = df["abs_B_ZEN"].quantile(0.75)

IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

print("Q1 :", Q1)
print("Q3 :", Q3)
print("IQR :", IQR)
print("Borne inférieure :", borne_inf)
print("Borne supérieure :", borne_sup)
valeurs_atypiques = df[
    (df["abs_B_ZEN"] < borne_inf) |
    (df["abs_B_ZEN"] > borne_sup)
]

print("\nNombre de valeurs atypiques :", len(valeurs_atypiques))
print(valeurs_atypiques[["night_id", "abs_B_ZEN"]])