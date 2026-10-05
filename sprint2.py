import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#SPRINT 2 : Data engineering et feature engineering
# Chargement du dataset final du Sprint 1
df = pd.read_csv("data/ID003_final.csv")

# Conversion de la date
df["UTC_DATE"] = pd.to_datetime(df["UTC_DATE"])

# Tri chronologique
df = df.sort_values("UTC_DATE")

print(df.head())
print(df.shape)
print(df.columns)

#A.Variables dérivées recommandées
#1. delta_T (Sprint 1)

#2. Création de la variable year_decimal
df["year_decimal"] = (
    df["UTC_DATE"].dt.year
    + (df["UTC_DATE"].dt.dayofyear - 1) / 365.25
)
print(df[["UTC_DATE", "year_decimal"]].head())

#3. Création de la variable NSB_median_night (médiane de la NSB par night_id)
df["NSB_median_night"] = df.groupby("night_id")["NSB"].transform("median")
print(df[["night_id", "NSB", "NSB_median_night"]].head(10))

#4. Création de la variable NSB_IQR_night (IQR de la NSB par night_id)
df["NSB_IQR_night"] = (
    df.groupby("night_id")["NSB"]
      .transform(lambda x: x.quantile(0.75) - x.quantile(0.25))
)
print(df[["night_id", "NSB", "NSB_IQR_night"]].head(10))

#5. Création de la variable abs_B_ZEN (Valeur absolue de la variable B_ZEN)
df["abs_B_ZEN"] = df["B_ZEN"].abs()
print(df[["night_id", "abs_B_ZEN"]].head(10))

#6. Création de la variable Airmass
  #Conversion de ALT_SUN en radians
df["ALT_SUN_RAD"] = np.radians(df["ALT_SUN"])

print(df[["ALT_SUN", "ALT_SUN_RAD"]].head())
  #Calcul du sinus de ALT_SUN_RAD
df["SIN_ALT_SUN"] = np.sin(df["ALT_SUN_RAD"])

print(df[["ALT_SUN", "ALT_SUN_RAD", "SIN_ALT_SUN"]].head())

  #Airmass proprement dit
df["Airmass"] = 1 / df["SIN_ALT_SUN"]

print(df[["ALT_SUN", "SIN_ALT_SUN", "Airmass"]].head())

#B.Contrôle qualité recommandé
#1. Plage de NSB cohérente
plt.figure(figsize=(10, 5))

plt.hist(df["NSB"].dropna(), bins=50)

plt.xlabel("NSB (mag/arcsec²)")
plt.ylabel("Nombre de mesures")
plt.title("Distribution des valeurs de NSB")

plt.show()
#NSB s'étend de 20,375 à 21,55


#2. Valeur de FREQ ne s’écartant pas significativement de 50 000 Hz
print(df["FREQ"].describe())
print(df["FREQ"].value_counts().head(20))

#FREQ s'étend de 0,32 et 2,10


#3. Distribution de delta_T présentant une queue froide correspondant aux nuits claires

#dataset déjà filtré avec le critère ΔT ≥ 20 °C

#4. Mesures de jour (ALT_SUN > 0ř) exclues
print(df["ALT_SUN"].max())
# ALT_SUN < -18°C pour toute observation conservée

#5. Aucune date dupliquée dans l’index
df_index = df.set_index("UTC_DATE")

print("Nombre de dates dupliquées :", df_index.index.duplicated().sum())
#Aucune date dupliquée


#6. Unités cohérentes : ILLUMOON en fraction (0–1)

print("Minimum :", df["ILLUMOON"].min())
print("Maximum :", df["ILLUMOON"].max())
# ILLUMOON entre 0 et 0,1

#C. Agrégation des données par nuit
nb_mesures_nuit = df.groupby("night_id").size()

print(nb_mesures_nuit.head(10))

# Création des caractéristiques de la NSB par nuit
features_nuit = df.groupby("night_id")["NSB"].agg(
    NSB_median_night="median",
    NSB_mean="mean",
    NSB_std="std",
    NSB_min="min",
    NSB_max="max",
    NSB_IQR_night=lambda x: x.quantile(0.75) - x.quantile(0.25)
)

print(features_nuit.head())

# Ajout du nombre de mesures par nuit

features_nuit["nb_mesures"] = df.groupby("night_id")["NSB"].size()


# Caractéristiques astronomiques par nuit

features_nuit["year_decimal"] = df.groupby("night_id")["year_decimal"].first()
features_nuit["abs_B_ZEN"] = df.groupby("night_id")["abs_B_ZEN"].mean()
print(features_nuit.head())

# Vérification du dataset agrégé

print("Nombre de nuits :", features_nuit.shape[0])
print("Nombre de variables :", features_nuit.shape[1])

print("\nValeurs manquantes :")
print(features_nuit.isna().sum())

# Sauvegarde du dataset agrégé par nuit
features_nuit.to_csv("data/ID003_features_nuit.csv")