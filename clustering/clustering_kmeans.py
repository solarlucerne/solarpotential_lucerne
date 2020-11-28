"""
Created on Fri Nov 27 17:15:13 2020

Clustering using kmeans

@author: giuseppeperonato
"""

import os
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn import metrics

import circle_fit

# Import datatasets
buildings = pd.read_csv("../data/buildings.csv")

# If you want to plot the footprints (data from GoogleDrive)
# footprints = gpd.read_file(
#     "../data/Solarpotentialkataster/Solarpotentialkataster/Abgabe_HSLU_201028.gdb.zip",
#     layer="AVBBXXXX_V2_PY_Luzern_20201025",
# )

# Tranform the point dataset into a geodataframe with XY points
gdf = gpd.GeoDataFrame(
    buildings,
    geometry=gpd.points_from_xy(
        buildings["E.Gebäudekoordinate"], buildings["N.Gebäudekoordinate"]
    ),
    crs="EPSG:2056",
)


# Cleaning the data
gdf = gdf.loc[~gdf.Bauperiode.isna(), :]
gdf = gdf.loc[gdf.PV_ERTRAG > 0, :]

# Creating 10 categories of yearly PV generation (kWh)
gdf["PV_ERTRAG_cat"] = pd.cut(gdf.PV_ERTRAG, 10, labels=range(10))

# Clustering by similarities
X = np.array(
    [
        gdf["PV_ERTRAG_cat"],
        gdf["DACHART"],
        gdf["Gebäudekategorie"],
        gdf["Bauperiode"],
        gdf.geometry.x,
        gdf.geometry.y,
    ]
).transpose()

# Try StandardScaler for now
x_scaled = preprocessing.StandardScaler().fit_transform(X)


FindOptimalk = False
if FindOptimalk:
    sil = []
    sum_of_squared_distances = []
    kmax = 3000
    step = 500
    K = range(2, kmax + 2, step)  # minimum two clusters to find dissimilarity
    for k in K:
        kmeans = KMeans(n_clusters=k).fit(x_scaled)
        labels = kmeans.labels_
        score = metrics.silhouette_score(x_scaled, labels, metric="euclidean")
        sum_of_squared_distances.append(kmeans.inertia_)
        sil.append(score)
        print("k=", k, "silhouette=", score, "inertia=", kmeans.inertia_)

    plt.plot(K, sil)
    plt.xlabel("k")
    plt.ylabel("Silhouette score")


# Clustering
n_clusters = 1500
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(x_scaled)
gdf["cluster"] = kmeans.labels_
# squared distance to cluster center
X_dist = kmeans.transform(X) ** 2
gdf["sqdist"] = X_dist.sum(axis=1).round(2)
gdf.plot(column="cluster", categorical=True, markersize=1)


# Subsetting the dataset
sel = gdf


# Keep only clusters with more than x building
min_buildings = 3
count = gdf.groupby("cluster").count().iloc[:, 0]
sel = sel.loc[gdf["cluster"].isin(count[count > min_buildings].index), :]


# Keep only close buildings fitting in a circle
sel["radius"] = 0
sel2 = sel.copy()
for i, c in enumerate(sel.cluster.unique()):
    x, y, radius, e = circle_fit.least_squares_circle(
        sel.loc[sel.cluster == c, ["E.Gebäudekoordinate", "N.Gebäudekoordinate"]].values
    )
    sel2.loc[sel2.cluster == c, "radius"] = radius

max_radius = 500
sel = sel2.loc[sel2.radius < max_radius, :]


print(
    sel[
        ["PV_ERTRAG", "DACHART", "Bauperiode", "cluster", "radius", "sqdist"]
    ].sort_values(by="cluster")
)

fig, ax = plt.subplots()
gdf.plot(ax=ax, color="grey", markersize=0.5)
sel.plot(column="cluster", ax=ax, markersize=3, categorical=True)
ax.set_xticks([])
ax.set_yticks([])

# Add geographical coordinates (for Google Earth)
sel["coords"] = sel.geometry.to_crs("EPSG:4326")
sel["lat"] = sel.coords.y
sel["lon"] = sel.coords.x

# Export csv so that it can be loaded in GoogleEarth

sel.to_csv("../data/clustering.csv")

# Uncomment to plot by cluster
# for i, c in enumerate(sel.cluster.unique()):
#     fig, ax = plt.subplots()
#     gdf.plot(ax=ax, color="grey", markersize=1)
#     sel.loc[sel.cluster == c, :].plot(column="cluster", ax=ax, markersize=5)
