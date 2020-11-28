## ---------------------------
## Script name: 00_transform_GWR_data.R
## 
## Purpose of script: Transform GWR data (Gebäude- und Wohnungsregister) from 
##                    .dsv to .csv and create an overview in an .xslx file.
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
library(readr)
library(assertthat)

## -----------------------------------------------------------------------------


load_path <- "data/GWR/Datensatz9/rawdata/"
save_path <- "data/GWR/Datensatz9/csv/"
files <- c("ARB", "EIN", "GEB", "GST", "PROJ", "WHG")
overview <- data.frame()

# Import the 6 GWR Datasets and 6 Readme from .dsv data and save as .csv
for (file in files) {
  # Load data & readme (contains column names)
  data <- read_delim(paste0(load_path, "GWR_MADD_", file, "-09_Data_MADD-20201009-A1_20201029.dsv"), delim = "\t")
  meta <- read_delim(paste0(load_path, "GWR_MADD_", file, "-09_Readme_MADD-20201009-A1_20201029.dsv"), delim = "\t")
  # rename columns to full "Bezeichnung2
  assert_that(ncol(data) == nrow(meta))
  assert_that(all(colnames(data) == meta$`Merkmal-Id`))
  colnames(data) <- meta$Bezeichnung
  # save as CSV
  # write_csv(x = data, path = paste0(save_path, file,".csv"))
  # Add data to overview
  df <- cbind(expand.grid(file, meta$"Merkmal-Id"), meta$Bezeichnung, nrow(data))
  df <- cbind(df, as.vector(apply(head(data, n = 10), 2, paste, collapse = ",  ")))
  overview <- rbind(overview, df)
}

colnames(overview) <- c("Datensatz", "Merkmal-Id", "Bezeichnung", "Anz_Beobachtungen", "Top_10_entries")
xlsx::write.xlsx(overview, file = paste0(save_path, "zzz_GWR_overview.xlsx"), row.names = FALSE)
