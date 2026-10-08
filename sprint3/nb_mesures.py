import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("../data/ID003_features_nuit.csv")


#Histogramme (Chaque nuit est-elle représentée par un nombre suffisant et comparable de mesures pour que ses statistiques soient fiables ?)
plt.figure(figsize=(10, 5))

plt.hist(df["nb_mesures"].dropna(), bins=15)

plt.xlabel("nombre de mesures")
plt.ylabel("Nombre de nuits")
plt.title("Distribution des valeurs de nb_mesures")
plt.show()
#nb_mesures varie approximativement de 50 à 550 mesures par nuit.
#La concentration principale se situe autour de 380–450 mesures.
#Le mode se trouve autour de 415–450 mesures, avec environ 18 nuits.
#Il existe aussi plusieurs nuits avec moins de 350 mesures.
#Quelques nuits dépassent 480 mesures.

#Statistique descriptive
print(df["nb_mesures"].describe())

#Valeur atypique
Q1 = df["nb_mesures"].quantile(0.25)
Q3 = df["nb_mesures"].quantile(0.75)

IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

print("Q1 :", Q1)
print("Q3 :", Q3)
print("IQR :", IQR)
print("Borne inférieure :", borne_inf)
print("Borne supérieure :", borne_sup)
valeurs_atypiques = df[
    (df["nb_mesures"] < borne_inf) |
    (df["nb_mesures"] > borne_sup)
]

print("\nNombre de valeurs atypiques :", len(valeurs_atypiques))
print(valeurs_atypiques[["night_id", "nb_mesures"]])