## ---------------------------
## Script name: - 
## 
## Purpose of script: Merge GWR-Data & Solarpotentialkataster
## 
## Author: Michael Schmid
## 
## Date Created: 2020-10-22
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

path_sol <- "data/Solarpotentialkataster/neu/mygeodata/unnamed.gdb/"
path_gwr <- "data/GWR/Datensatz9/csv/"

# Import Data from Solarkataster
sol <- read.csv(file = paste0(path_sol, "SOLPKT18_V2_PY_Luzern_SpatialJoinC.csv"), encoding = "UTF-8")

# Import all Tables from GWR 
for (file in c("ARB", "EIN", "GEB", "GST", "PROJ", "WHG")) {
  assign(file, read.csv(paste0(path_gwr, file,".csv"), encoding = "UTF-8"))
}

## ----------------------------- Basic analysis -----------------------------------

# We have 35'146 rows in the sol-data
nrow(sol)
# we have 7046 unique EGID's in the sol-data  
length(unique(sol$GWR_EGID)) 
# We have 25'700 usable rows in the sol-data (columns width EGID)
sum(!is.na(sol$GWR_EGID))

# Of the 25'700 rows we can use 25'698 for EIN, GEB, GST
sum(sol$GWR_EGID %in% ARB$Eidgenössischer.Gebäudeidentifikator) # not interesting ()
sum(sol$GWR_EGID %in% EIN$Eidgenössischer.Gebäudeidentifikator) # -> interesting !!!
sum(sol$GWR_EGID %in% GEB$Eidgenössischer.Gebäudeidentifikator) # -> interesting !!!! 
sum(sol$GWR_EGID %in% GST$Eidgenössischer.Gebäudeidentifikator) # -> maybe interesting 
# sum(sol$GWR_EGID %in% PROJ$...?)                              # not interesting (because not connected to EGID)
sum(sol$GWR_EGID %in% WHG$Eidgenössischer.Gebäudeidentifikator) # not intersting (we are not interested in the apartments)

## ----------------------------- Outer merge -----------------------------------

# Outer Merge sol-Data & GEB-Data (We get the full dataset of 35'146 rows but the merge doesn't 
# work for sol-Data without EGID -> see bottom rows of df)
df_outer <- merge(sol, GEB, by.x = "GWR_EGID", by.y = "Eidgenössischer.Gebäudeidentifikator", all.x = TRUE)
df <- merge(sol, GEB, by.x = "GWR_EGID", by.y = "Eidgenössischer.Gebäudeidentifikator", all.x = FALSE)
save(df_outer, file = "data/df_outer.RData")
save(df, file = "data/df.RData")



## ----------------------------- Find "N_apartments" per EGID ----------------------
apartment_table <- as.data.frame(table(WHG$Eidgenössischer.Gebäudeidentifikator))
names(apartment_table) <- c("EGID", "n_apartments")
save(apartment_table, file = "data/apartment_table.RData")



