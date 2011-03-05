#### Get/Parse Arguments ####
Args = commandArgs()
inputFC = sub(".shp", "", Args[5], ignore.case = TRUE)
fields = Args[6]
varNames = strsplit(fields, ";")
varNames = c(unlist(varNames))
numVars = length(varNames)

#### Import the Cluster Library ####
print("Loading Libraries....")

#### Using Maptools For Shapefiles ####
library(maptools)  	

print("Begin Calculations....")
shp = readShapeSpatial(inputFC)
allVars = coordinates(shp)

#### Set Col Labels ####
colLabs = rep(0, numVars + 2)
colLabs[1] = "XCoords"
colLabs[2] = "YCoords"

for (i in 1:length(varNames)){
    allVars = cbind(allVars, shp[[varNames[i]]])
    colLabs[i+2] = varNames[i]
    } 

#### Create Data Frame for Analysis ####
new = data.frame(allVars)
names(new) = colLabs

#### Print Variable Summary ####
s = summary(new)
print(s)

print("Calculations Complete...")
