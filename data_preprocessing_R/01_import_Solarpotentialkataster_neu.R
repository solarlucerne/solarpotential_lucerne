## ---------------------------
## Script name: 00_import_Solarpotentialkataster_neu.R
## 
## Purpose of script: Import shapefiles and visualize them. (Play around!)
## 
## Author: Michael Schmid
## 
## Date Created: 2020-11-26
##
## Copyright (c) Michael Schmid, 2020
## Email: michi.smith@bluewin.ch
##
## ---------------------------
##
## Notes:
##   
##
## ---------------------------

# imsbasics::clc()
library(sf)
library(ggplot2)
library(leaflet)

## -----------------------------------------------------------------------------



load_path <- "data/Solarpotentialkataster/neu/mygeodata/unnamed.gdb/"
# shapefile <- "AVBBXXXX_V2_PY_Luzern_20171231.csv"

for (file in list.files(load_path)) {
  assign(x = unlist(strsplit(file, "[.]"))[1], 
         value = read.csv(file = paste0(load_path, file)))
}

# "AVBBXXXX_V2_PY_Luzern_20171231.csv"      --> Basic parameters 2017 (without EGID)
# "AVBBXXXX_V2_PY_Luzern_20201025.csv"      --> Basic parameters 2020 (with EGID)
# "AVEINXXX_V3_PT_Luzern_20201025.csv"      --> Lookup EGID <-> Adress & Swiss-Coordinates
# "SOLPKT18_V2_PY_Luzern_SpatialJoinC.csv"  --> Solarpotential-Data with EGID
# "symdiff.csv"                             --> Synch Problems 
