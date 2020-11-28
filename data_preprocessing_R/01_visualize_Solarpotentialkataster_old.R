## ---------------------------
## Script name: 00_import_Solarpotentialkataster.R
## 
## Purpose of script: Import shapefiles and visualize them. (Play around!)
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
library(sf)
library(ggplot2)
library(leaflet)

## -----------------------------------------------------------------------------



load_path <- "data/Solarpotentialkataster/alt/"
shapefile <- "SOLPKT18_V2_PY.shp"

polygons <- st_read(paste0(load_path, shapefile))

# Class 
class(polygons)
# Geometry types = MULTIPOLYGON
unique(st_geometry_type(polygons))
# Coordinate reference system
st_crs(polygons)
# Bounding Box
st_bbox(polygons)


# 1st Try to plot polygons
ggplot() + 
  geom_sf(data = polygons[1:10,], size = 1, color = "black", fill = "cyan1") + 
  ggtitle("AOI Boundary Plot") + 
  coord_sf()

# 2nd Try to plot polygons 
polygons_small <- polygons[1:20, ]
leaflet(polygons_small) %>% 
  addProviderTiles("CartoDB.Positron") %>% 
  addPolygons(color = "green")

# 3rd Try to plot polygons 
poly_geom <- st_geometry(polygons[1:20,])
leaflet(poly_geom) %>% 
  addProviderTiles("CartoDB.Positron") %>% 
  addPolygons(color = "green")


# 4th Try to plot polygons (EPSG 4326 = lonlat)
poly_wgs84 <- polygons 
st_set_crs(poly_wgs84, 4326)
poly_wgs84 <- st_transform(polygons[1:200,], "+init=epsg:4326")
leaflet(poly_wgs84) %>% 
  addProviderTiles("CartoDB.Positron") %>% 
  addPolygons(color = "green")


# 5th Try to plot polygons (EPSG 3857 = Leaflet standard)
poly_wgs84 <- polygons 
st_set_crs(poly_wgs84, 3857)
poly_wgs84 <- st_transform(polygons[1:200,], "+init=epsg:3857")
leaflet(poly_wgs84) %>% 
  addProviderTiles("CartoDB.Positron") %>% 
  addPolygons(color = "green")




