"""
Created on Fri Nov 27 2020

Data Aggregation - First step

@author: thomasjenny
"""

import pandas as pd

# Load data:
data = pd.read_csv("data/eignung_3_and_4_grouped.csv")
data.drop(["Unnamed: 0"], axis=1, inplace=True)

# Separation of the columns: Since we want one value per building,
# we need to calculate sums and mean values, depending on the column.
columns_means = ["X", "Y", "DACHART", "EXPO_GRAD", 
                 "EXPO_KLASSE", "NEIGUNG", "EIGNUNG"]

columns_sums = ["TD_FLAECHE", "GESAMT_EINSTR", "MITTLERE_EINSTR", 
                "PV_ERTRAG", "PV_CO2_ERSP", "ST_ERTRAG", "ST_CO2_ERSP", 
                "ST_OEL_ERSP"]

# List of the columns we don't need the means or sums from (some
# columns excluded)
other_values = ["GWR_EGID", "Amtliche.Gebäudenummer", 
                "Name.des.Gebäudes", "E.Gebäudekoordinate",
                "N.Gebäudekoordinate", "Quartier", "Gebäudestatus",
                "Gebäudekategorie", "Gebäudeklasse", 
                "Baujahr.des.Gebäudes.YYYY", "Baumonat.des.Gebäudes.MM", 
                "Baujahr..und.monat.des.Gebäudes..YYYY.oder.YYYY.MM..GBAUJ.GBAUM.",
                "Bauperiode", "Renovationsjahr.des.Gebäudes",
                "Abbruchjahr.des.Gebäudes", "Gebäudefläche", "Gebäudevolumen", 
                "Informationsquelle.zum.Gebäudevolumen", "Gebäudevolumen..Norm",
                "Anzahl.Geschosse", "Anzahl.separate.Wohnräume", "Zivilschutzraum",
                "Energiebezugsfläche", "Wärmeerzeuger.Heizung.1",
                "Energie..Wärmequelle.Heizung.1", "Informationsquelle.Heizung.1", 
                "Datum.der.Erstellung", "Datum.der.letzten.Änderung", 
                "BFS.Gemeindenummer", "Gemeindename", "Kantonskürzel"]

# Complete list of other values: this list includes the columns that
# are excluded in the list "other_values" if one wants to work with all
# the columns.
other_values2 = ["GWR_EGID", "Amtliche.Gebäudenummer", "Name.des.Gebäudes", 
                 "E.Gebäudekoordinate", "N.Gebäudekoordinate", "Quartier",
                 "Gebäudestatus", "Gebäudekategorie", "Gebäudeklasse",
                 "Baujahr.des.Gebäudes.YYYY", "Baumonat.des.Gebäudes.MM",
                 "Baujahr..und.monat.des.Gebäudes..YYYY.oder.YYYY.MM..GBAUJ.GBAUM.",
                 "Bauperiode", "Renovationsjahr.des.Gebäudes", 
                 "Abbruchjahr.des.Gebäudes", "Gebäudefläche", "Gebäudevolumen",
                 "Informationsquelle.zum.Gebäudevolumen", "Gebäudevolumen..Norm",
                 "Anzahl.Geschosse", "Anzahl.separate.Wohnräume", "Zivilschutzraum",
                 "Energiebezugsfläche", "Wärmeerzeuger.Heizung.1",
                 "Energie..Wärmequelle.Heizung.1", "Informationsquelle.Heizung.1", 
                 "Aktualisierungsdatum.Heizung.1", "Wärmeerzeuger.Heizung.2",
                 "Energie..Wärmequelle.Heizung.2", "Informationsquelle.Heizung.2",
                 "Aktualisierungsdatum.Heizung.2", "Wärmeerzeuger.Warmwasser.1",
                 "Energie..Wärmequelle.Warmwasser.1", "Informationsquelle.Warmwasser.1",
                 "Aktualisierungsdatum.Warmwasser.1", "Wärmeerzeuger.Warmwasser.2",
                 "Energie..Wärmequelle.Warmwasser..2", "Informationsquelle.Warmwasser.2",
                 "Aktualisierungsdatum.Warmwasser.2", "Datum.der.Erstellung",
                 "Datum.der.letzten.Änderung", "BFS.Gemeindenummer", "Gemeindename",
                 "Kantonskürzel"]

# Calculate means and sums:
means = data.groupby(by="GEB_ID")[columns_means].mean()
sums = data.groupby(by="GEB_ID")[columns_sums].sum()

# Drop double rows from the "other_values" list (if applicable) 
# and only keep the value from the corresponding first row:
other_columns = data.groupby(by="GEB_ID")[other_values].first()

# Concatenate the 3 dataframes:
buildings = pd.concat([means, sums, other_columns], axis=1)

# Add column "DACHART_Factor" and convert the "DACHART" floats into factors:
buildings.loc[buildings["DACHART"] == 1, "DACHART_Factor"] = "slope"
buildings.loc[buildings["DACHART"] == 0, "DACHART_Factor"] = "flat"
buildings.loc[(buildings["DACHART"] > 0) & (buildings["DACHART"] < 1), "DACHART_Factor"] = "mixed"

# Check the result:
# buildings.head()

# Write CSV file if desired:
# buildings.to_csv("buildings.csv", index = True, header = True, sep = ',', encoding = 'utf-8')
