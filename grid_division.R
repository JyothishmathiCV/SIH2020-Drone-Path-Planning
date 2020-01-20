args<-commandArgs(TRUE)

library(rgdal)
library(raster)
library(rgeos)
library(dismo)
library(ggplot2)
library(sf)
library(lattice)

setwd(args[1])

getwd()

print(paste(getwd(),"/",args[2],".shp",sep=""))

dryland <- readOGR(paste(getwd(),"/",args[2],".shp",sep=""),args[2]) 

grid <- raster(extent(dryland))

# Create an empty raster.

res(grid) <-  0.0960961

# Make the grid have the same coordinate reference system (CRS) as the shapefile.
proj4string(grid)<-proj4string(dryland)

# Transform this raster into a polygon and you will have a grid, but without Brazil (or your own shapefile).
gridpolygon <- rasterToPolygons(grid)

png(filename=paste(args[2],"grid.png",sep=""))

plot(gridpolygon)

dev.off()



dry.grid <- gIntersection(dryland, gridpolygon,byid=TRUE)

grid_ctr <- coordinates(dry.grid)

png(filename=paste(args[2],"out.png",sep=""))

plot(dry.grid)

points(grid_ctr, col="red", pch=16)

dev.off()


print(grid_ctr)


print(paste(attr(raster(grid),"nrow"),attr(raster(grid),"ncol"),sep=" "))



