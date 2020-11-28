import pandas as pd

data = pd.read_csv("data/buildings.csv")

# Create function for calculating the Peak Power value:
def to_peak_power(roof_size):
    """
    :param roof_size: Roof size
    :return: Peak power value for the according roof size
    """
    return (roof_size/1.6) * 0.3

# Create new "Gebäudeklasse" Column which will be mapped later and
# fill NA values:
data["GBKLASSE"] = data["Gebäudeklasse"]
data["GBKLASSE"].fillna(0, inplace=True)

# Convert "GBKLASSE" column to integer for mapping:
data.loc[:, "GBKLASSE"] = data.loc[:, "GBKLASSE"].astype(int)

# Check:
# data.dtypes

# Create dictionary with building classes which will be mapped to the
# new "GBKLASSE" column:

building_classes = {0: "Unbekannt",
                   1110: "Gebäude mit einer Wohnung",
                   1121: "Gebäude mit zwei Wohnungen",
                   1122: "Gebäude mit drei oder mehr Wohnungen",
                   1130: "Wohngebäude für Gemeinschaften",
                   1211: "Hotelgebäude",
                   1212: "Andere Gebäude für kurzfristige Beherbergungen",
                   1220: "Bürogebäude",
                   1230: "Gross- und Einzelhandelsgebäude",
                   1231: "Restaurants und Bars in Gebäuden ohne Wohnnutzung",
                   1241: "Bahnhöfe, Abfertigungsgebäude, Fernsprechvermittlungszentralen",
                   1242: "Garagengebäude",
                   1251: "Industriegebäude", 
                   1252: "Behälter, Silos und Lagergebäude",
                   1261: "Gebäude für Kultur- und Freizeitzwecke", 
                   1262: "Museen / Bibliotheken",
                   1263: "Schul- und Hochschulgebäude, Forschungseinrichtungen",
                   1264: "Krankenhäuser und Facheinrichtungen des Gesundheitswesens",
                   1265: "Sporthallen",
                   1271: "Landwirtschaftliche Betriebsgebäude",
                   1272: "Kirchen und sonstige Kultgebäude",
                   1273: "Denkmäler oder unter Denkmalschutz stehende Bauwerke",
                   1274: "Sonstige Hochbauten, anderweitig nicht genannt",
                   1275: "Andere Gebäude für die kollektive Unterkunft",
                   1276: "Gebäude für die Tierhaltung",
                   1277: "Gebäude für den Pflanzenbau",
                   1278: "Andere landwirtschaftliche Gebäude"}

# Map dictionary to "GBKLASSE" column:
data.loc[:, "GBKLASSE"] = data.loc[:, "GBKLASSE"].map(building_classes)


# Create a new column for Peak Power and calculate the Peak Power 
# value with the function from above:
data["Peak Power"] = to_peak_power(data[["TD_FLAECHE"]])

# Write CSV if desired:
# data.to_csv("building-types-peak-power.csv", index = True, header = True, sep = ',', encoding = 'utf-8')
