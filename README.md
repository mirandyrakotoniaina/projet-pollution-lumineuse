# Sprint 1 — Compréhension scientifique et gouvernance des données

## 1. Objectif du sprint

L'objectif de ce sprint est de comprendre la structure et la signification des données de brillance du ciel, d'évaluer leur qualité et de déterminer quelles observations sont suffisamment fiables pour l'analyse.

### Question de référence

> **Quelles sont mes données, que signifie chaque variable, quelles observations sont fiables et quelles observations dois-je conserver pour analyser correctement la brillance du ciel ?**

---

## 2. Données utilisées

Le fichier utilisé est :

```text
data/ID003.fits
```

Le fichier FITS contient :

* **2 HDU**

  * `HDU 0` : `PrimaryHDU`
  * `HDU 1` : `BinTableHDU`
* **511 034 observations**
* **29 variables**
* **815 nuits UTC**

La variable principale étudiée est :

```text
NSB
```

Elle représente la **brillance du ciel nocturne**, exprimée en magnitude par seconde d'arc carré.

---

## 3. Structure des données

Les variables sont regroupées en quatre familles :

### Temps et calendrier

`UTC_DATE`, `UTC_JD`, `UTC_WDAY`, `UTCNIGHT`, `UTCTIME`, `LOC_DATE`, `LOC_JD`, `LOC_WDAY`, `LOCNIGHT`, `LOCTIME`

### Capteurs et photométrie

`EFFIC`, `GOODNESS`, `T_AMB`, `T_SKY`, `FREQ`, `NSB`, `ZP`

### Éphémérides Soleil-Lune

`AZ_SUN`, `ALT_SUN`, `AZ_MOON`, `ALT_MOON`, `AGE_MOON`, `ILLUMOON`, `DISTMOON`

### Coordonnées célestes et modèles

`L_ZEN`, `B_ZEN`, `ALPHAZEN`, `BETAZEN`, `GAMBONS`

---

## 4. Contrôle de qualité

Le profilage initial a montré :

* **0 valeur manquante**
* **0 doublon complet**
* **4 valeurs infinies dans `NSB`**

Les quatre observations concernées présentent :

```text
FREQ = 0
GOODNESS = 0
NSB = inf
```

Elles ont donc été considérées comme non exploitables.

Les valeurs infinies de `NSB` ont été remplacées par `NaN`, puis les quatre observations ont été supprimées.

```text
511 034 observations
        ↓
511 030 observations
```

---

## 5. Variable dérivée : ΔT

Une nouvelle variable a été créée à partir des températures :

```text
ΔT = T_AMB - T_SKY
```

Cette variable est utilisée pour caractériser les conditions atmosphériques et participer au filtrage des observations affectées par les nuages.

---

## 6. Segmentation temporelle

Les observations ont été triées selon `UTC_DATE`.

Une nouvelle séquence temporelle est créée lorsqu'un écart de plus de **30 minutes** est observé entre deux mesures successives.

Résultat :

```text
2 504 séquences temporelles
```

---

## 7. Filtrage scientifique

Les filtres sont appliqués successivement afin de conserver les observations adaptées à l'étude de la brillance du ciel.

| Étape             | Condition                                | Observations conservées |
| ----------------- | ---------------------------------------- | ----------------------: |
| Données initiales | —                                        |                 511 034 |
| Nettoyage `NSB`   | Suppression des 4 `inf`                  |                 511 030 |
| Nuit astronomique | `ALT_SUN < -18°`                         |                 364 288 |
| Filtre lunaire    | `ALT_MOON < 0` et `ILLUMOON ≤ 0.10`      |                  74 271 |
| Filtre galactique | `abs(B_ZEN) ≥ 20°`                       |                  53 710 |
| Filtre nuages     | `ΔT ≥ 20°C` et écart-type glissant ≤ 2°C |                  29 179 |

### Nuit astronomique

Seules les observations avec :

```text
ALT_SUN < -18°
```

sont conservées afin d'exclure les périodes où le Soleil influence la luminosité du ciel.

### Lune

Les conditions utilisées sont :

```text
ALT_MOON < 0°
ILLUMOON ≤ 0.10
```

La Lune doit être sous l'horizon et son illumination doit être inférieure ou égale à 10 %.

### Voie lactée

Le filtre :

```text
|B_ZEN| ≥ 20°
```

permet d'éviter les observations proches du plan galactique, où la luminosité naturelle du ciel peut être plus importante.

### Nuages

Les conditions utilisées sont :

```text
ΔT ≥ 20°C
```

et

```text
écart-type glissant de ΔT sur 30 min ≤ 2°C
```

L'objectif est de conserver des périodes présentant des conditions suffisamment stables et favorables aux mesures.

---

## 8. Détection des anomalies laser

Une médiane glissante de `NSB` sur une fenêtre de **30 minutes** est calculée.

Le résidu est ensuite obtenu par :

```text
NSB_residu = NSB - NSB_median_30min
```

L'écart-type global des résidus est utilisé pour définir un seuil de détection à **5σ**.

Résultats :

```text
Sigma des résidus : 0.049857
Seuil 5σ : -0.249285

Candidats détectés : 85
Épisodes détectés : 18
```

Les candidats ne sont pas supprimés du dataset principal car les créneaux laser planifiés ne sont pas disponibles pour confirmer qu'il s'agit réellement de perturbations laser.

Ils sont conservés séparément dans :

```text
data/laser_candidates.csv
```

---

## 9. Sélection des séquences exploitables

Après les différents filtres scientifiques :

```text
29 179 observations
124 séquences
```

Les séquences contenant moins de **50 observations** sont ensuite exclues conformément aux recommandations de la documentation TESS-W.

Dataset final :

```text
28 793 observations
90 séquences temporelles
```

Ce dataset constitue la base nettoyée utilisée pour la suite du projet.

---

## 10. Livrables du Sprint 1

Les principaux résultats produits pendant ce sprint sont :

```text
data/
├── ID003.fits
├── ID003_clean.csv
├── ID003_clouds_filtered.csv
├── ID003_final.csv
├── ID003_segmented.csv
└── laser_candidates.csv

sprint1.py
```

### Statut

**Sprint 1 — Terminé**
