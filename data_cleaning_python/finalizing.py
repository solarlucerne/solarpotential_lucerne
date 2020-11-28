"""
Created on Sat Nov 28 2020

Data cleaning and wrangling - final step - creating final data table

@author: giuseppeperonato
"""

import pandas as pd

data = pd.read_csv("building-types-peak-power.csv")
data.drop(["Unnamed: 0"], axis=1, inplace=True)

# Create function to caluclate total floor area:
def calculate_floor_area(area, floors):
    """
    :param area: base area of the building
    :param floors: number of floors of the building
    :return: total floor area of the building
    """
    return area * floors


# Replace all NA values with 0:
data.fillna(0, inplace=True)

# Transformi columns from float to intetger:
columns_to_transform = ["Bauperiode", "Renovationsjahr.des.Gebäudes", "Anzahl.Geschosse"]

for column in columns_to_transform:
    data.loc[:, column] = data.loc[:, column].astype(int)


# Drop columns not needed:
to_keep = ["GWR_EGID", "Peak Power", "Gebäudekategorie", 
           "GBKLASSE", "Quartier", "TD_FLAECHE", "EIGNUNG", 
           "Anzahl.Geschosse", "Gebäudefläche", "Bauperiode", 
           "Renovationsjahr.des.Gebäudes"]

data = data.loc[:, data.columns.intersection(to_keep)]



# Mapping "Quartiere":
neighborhoods = {1061001: "Oberseeburg-Rebstock",
                 1061002: "Würzenbach-Schädrüti",
                 1061003: "Bellerive-Schlössli",
                 1061004: "Halde-Lützelmatt",
                 1061005: "Wesemlin-Dreilinden",
                 1061006: "Maihof-Rotsee",
                 1061007: "Hochwacht-Zürichstrasse",
                 1061008: "Altstadt-Wey",
                 1061009: "Bramberg-St.Karli",
                 1061010: "Kantonsspital-Ibach",
                 1061011: "Baselstrasse-Bernstrasse",
                 1061012: "Bruch-Gibraltar",
                 1061013: "Obergütsch-Untergütsch",
                 1061014: "Hirschmatt-Kleinstadt",
                 1061015: "Obergrund-Allmend",
                 1061016: "Neustadt-Voltastrasse",
                 1061017: "Unterlachen-Tribschen",
                 1061018: "Sternmatt-Hochrüti",
                 1061019: "Langensand-Matthof",
                 1061030: "Udelboden",
                 1061031: "Reussbühl",
                 1061032: "Ruopigen",
                 1061033: "Matt",
                 1061034: "Littau Dorf",
                 1061035: "An der Emme",
                 1061036: "Littauerberg",
                 1061099: "Bürgenstock"}

data.loc[:, "Quartier"] = data.loc[:, "Quartier"].map(neighborhoods)


# Mapping "Bauperiode"
bauperiode = {0: "Unbekannt",
              8011: "Vor 1919", 
              8012: "1919-1945",
              8013: "1946-1960",
              8014: "1961-1970",
              8015: "1971-1980",
              8016: "1981-1985",
              8017: "1986-1990",
              8018: "1991-1995",
              8019: "1996-2000",
              8020: "2001-2005",
              8021: "2006-2010",
              8022: "2011-2015",
              8023: "Nach 2015"}

data.loc[:, "Bauperiode"] = data.loc[:, "Bauperiode"].map(bauperiode)


# Mapping building categories:
building_categories = {1010: "Provisorische Unterkunft",
                       1020: "Gebäude ausschließlich für Wohnnutzung",
                       1030: "Wohngebäude mit Nebennutzung",
                       1040: "Gebäude mit teilweiser Wohnnutzung",
                       1060: "Gebäude ohne Wohnnutzung",
                       1080: "Sonderbau"}

data.loc[:, "Gebäudekategorie"] = data.loc[:, "Gebäudekategorie"].map(building_categories)


# Add column with total floor area:
area = data["Gebäudefläche"]
floors = data["Anzahl.Geschosse"]

data["Floor.Area"] = calculate_floor_area(area, floors)

# Add address column:
# Read data, concatenate address columns and add to the "addresses" df, drop "old" columns
# and merge with the "data" df.

addresses = pd.read_csv("addresses.csv")

addresses["Adresse"] = addresses["Strassenbezeichnung"] + " " + addresses["Eingangsnummer Gebäude"]

addresses.drop(["Strassenbezeichnung", "Eingangsnummer Gebäude"], axis=1, inplace=True)

data = data.merge(addresses, left_on="GWR_EGID", right_on="GWR_EGID")

# Rename columns
data.rename(columns = {"GWR_EGID": "Eidgen. Gebäude ID",
                       "TD_FLAECHE": "Dachfläche",
                       "EIGNUNG": "Eignung",
                       "Renovationsjahr.des.Gebäudes": "Renovationsjahr",
                       "Anzahl.Geschosse": "Anzahl Geschosse",
                       "GBKLASSE": "Gebäudeklasse",
                       "Floor.Area": "Grundfläche"},
           inplace=True)


# Write CSV:
data.to_csv("final_provisory.csv", index = False, header = True, sep = ',', encoding = 'utf-8')
