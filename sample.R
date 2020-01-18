library(rgdal)
library(raster)
library(rgeos)
library(dismo)
library(ggplot2)
library(sf)
library(lattice)

dryland <- readOGR("/root/sample4/SIH2020-Drone-Path-Planning/dryland/dryland.shp", "dryland") 

grid <- raster(extent(dryland))

# Create an empty raster.

res(grid) <- 2

# Make the grid have the same coordinate reference system (CRS) as the shapefile.
proj4string(grid)<-proj4string(dryland)

# Transform this raster into a polygon and you will have a grid, but without Brazil (or your own shapefile).
gridpolygon <- rasterToPolygons(grid)

#print(paste(attr(raster(grid),"nrow"),attr(raster(grid),"ncol"))," Original GRID")

dry.grid <- gIntersection(dryland, gridpolygon,byid=TRUE)

grid_ctr <- coordinates(dry.grid)

plot(dry.grid, axes=TRUE)

points(grid_ctr, col="red", pch=16)


plot(dry.grid)

print(grid_ctr)

writeOGR(dry.grid, dsn=getwd(), layer="inters_shape", driver="ESRI Shapefile", overwrite_layer=T)

