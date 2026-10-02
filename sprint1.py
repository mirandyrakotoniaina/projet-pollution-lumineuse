from astropy.io import fits
import pandas as pd
import numpy as np

#SPRINT 1 : Compréhension scientifique et  gouvernance
# Chargement du fichier FITS
hdul = fits.open("data/ID003.fits")
table = hdul[1].data

# Conversion FITS → DataFrame
data = {}

for name in table.names:
    column = table[name]

    if column.dtype.byteorder == '>':
        column = column.byteswap().view(column.dtype.newbyteorder('='))

    data[name] = column

df = pd.DataFrame(data)

print("Nombre d'observations :", len(df))
print("Nombre de colonnes :", len(df.columns))
print("Colonnes :", df.columns.tolist())


# Conversion de UTC_DATE en datetime
df["UTC_DATE"] = pd.to_datetime(df["UTC_DATE"])

print(df["UTC_DATE"].dtype)
print(df["UTC_DATE"].min())
print(df["UTC_DATE"].max())

# Tri chronologique selon UTC_DATE
df = df.sort_values("UTC_DATE")

print(df[["UTC_DATE", "NSB"]].head())

# Vérification des doublons
doublons = df.duplicated().sum()

print("Nombre de doublons :", doublons)

# Vérification des valeurs manquantes
print("Valeurs manquantes :")
print(df.isna().sum())

# Vérification des valeurs infinies
print("Valeurs infinies :")
print(np.isinf(df.select_dtypes(include=np.number)).sum())

# Identification des observations contenant une valeur infinie dans NSB
print(df[np.isinf(df["NSB"])][[
    "UTC_DATE",
    "UTCNIGHT",
    "NSB",
    "FREQ",
    "GOODNESS"
]])

# Remplacement des valeurs infinies par NaN
df["NSB"] = df["NSB"].replace([np.inf, -np.inf], np.nan)

print("Valeurs manquantes dans NSB après remplacement :",
      df["NSB"].isna().sum())

# Suppression des observations dont le NSB est manquant
df = df.dropna(subset=["NSB"]).copy()

print("Nombre d'observations après nettoyage :", len(df))
print("Valeurs manquantes dans NSB :", df["NSB"].isna().sum())

# Calcul de la différence de température
df["delta_T"] = df["T_AMB"] - df["T_SKY"]

print(df[["T_AMB", "T_SKY", "delta_T"]].head())


# Segmentation des observations selon les écarts temporels
gap = pd.Timedelta("30 min")

df["night_id"] = (
    df["UTC_DATE"].diff() > gap
).cumsum()

print("Nombre de séquences :", df["night_id"].nunique())


#Filtrage
# Filtre de nuit astronomique
df_nuit = df[df["ALT_SUN"] < -18].copy()

print("Observations pendant la nuit astronomique :", len(df_nuit))
print("Observations exclues :", len(df) - len(df_nuit))

# Filtre lunaire
df_lune = df_nuit[
    (df_nuit["ALT_MOON"] < 0) &
    (df_nuit["ILLUMOON"] <= 0.10)
].copy()

print("Observations après filtre lunaire :", len(df_lune))
print("Observations exclues :", len(df_nuit) - len(df_lune))

# Filtre de la Voie lactée
df_galaxie = df_lune[
    df_lune["B_ZEN"].abs() >= 20
].copy()

print("Observations après filtre Voie lactée :", len(df_galaxie))
print("Observations exclues :", len(df_lune) - len(df_galaxie))


# Écart-type glissant de delta_T sur une fenêtre de 30 minutes
df_galaxie = df_galaxie.set_index("UTC_DATE").sort_index()
df_galaxie["delta_T_std_30min"] = (
    df_galaxie["delta_T"]
    .rolling("30min")
    .std()
)

print(
    df_galaxie[
        ["delta_T", "delta_T_std_30min"]
    ].head(10)
)

# Filtre des conditions nuageuses
df_nuages = df_galaxie[
    (df_galaxie["delta_T"] >= 20) &
    (df_galaxie["delta_T_std_30min"] <= 2)
].copy()

print("Observations après filtre nuages :", len(df_nuages))
print("Observations exclues :", len(df_galaxie) - len(df_nuages))


# Médiane glissante de NSB sur une fenêtre de 30 minutes
df_nuages["NSB_median_30min"] = (
    df_nuages["NSB"]
    .rolling("30min")
    .median()
)

print(
    df_nuages[
        ["NSB", "NSB_median_30min"]
    ].head(10)
)

df_nuages["NSB_residu"] = (
    df_nuages["NSB"] - df_nuages["NSB_median_30min"]
)

print(
    df_nuages[
        ["NSB", "NSB_median_30min", "NSB_residu"]
    ].head(10)
)
# Détection des anomalies potentielles liées aux lasers
# Médiane glissante de NSB sur une fenêtre de 30 minutes
df_nuages["NSB_median_30min"] = (
    df_nuages["NSB"]
    .rolling("30min")
    .median()
)

# Résidu par rapport à la médiane locale
df_nuages["NSB_residu"] = (
    df_nuages["NSB"] - df_nuages["NSB_median_30min"]
)

# Écart-type global des résidus
sigma = df_nuages["NSB_residu"].std()

# Seuil de détection à -5 sigma
seuil_5sigma = -5 * sigma

# Sélection des anomalies
candidats_laser = df_nuages[
    df_nuages["NSB_residu"] < seuil_5sigma
].copy()

print("Sigma des résidus :", sigma)
print("Seuil 5σ :", seuil_5sigma)
print("Nombre de candidats laser :", len(candidats_laser))

ecarts = candidats_laser.index.to_series().diff()

print("Écarts entre les candidats :")
print(ecarts.head(20))
print("\nPlus grands écarts :")
print(ecarts.sort_values(ascending=False).head(20))
for seuil in [5, 10, 15, 20, 25, 30]:
    nombre_groupes = (ecarts > pd.Timedelta(f"{seuil}min")).sum() + 1
    print(f"Seuil {seuil} min : {nombre_groupes} épisodes")

candidats_laser["laser_group"] = (
    ecarts > pd.Timedelta("5min")
).cumsum()
print("Nombre d'épisodes :", candidats_laser["laser_group"].nunique())

print(
    candidats_laser["laser_group"]
    .value_counts()
    .sort_index()
)
candidats_laser.to_csv(
    "data/laser_candidates.csv",
    index=True
)

print("Fichier laser_candidates.csv sauvegardé.")

# Taille de chaque séquence
taille_sequences = df_nuages.groupby("night_id").size()

print("Nombre de séquences avant filtrage :", len(taille_sequences))

# Conserver uniquement les séquences avec au moins 50 observations
sequences_valides = taille_sequences[
    taille_sequences >= 50
].index

df_final = df_nuages[
    df_nuages["night_id"].isin(sequences_valides)
].copy()

print("Nombre d'observations après filtrage :", len(df_final))
print("Nombre de séquences après filtrage :", df_final["night_id"].nunique())

df_final.to_csv(
    "data/ID003_final.csv",
    index=True
)

print("Fichier ID003_final.csv sauvegardé.")



#Verification finale print("Nombre d'observations :", len(df_final))
print("Nombre de séquences :", df_final["night_id"].nunique())
print("Valeurs manquantes :", df_final.isna().sum().sum())
print(
    "Valeurs infinies :",
    np.isinf(
        df_final.select_dtypes(include=np.number)
    ).sum().sum()
)