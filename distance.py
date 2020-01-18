from math import radians, cos, sin, asin, sqrt
import json

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return int(c * r * 1000) ##for meters

def get_row_col(nrow,ncol,obj):
    ob = int(obj["cellno"])
    row = int(ob)//ncol
    col = int(ob)%ncol
    return row,col

with open("./processing/master.json") as f:
    data = f.read()

# data = { "nrow":20, "ncol":23, "children":[{"lat","long","cellno"}] }
data = json.loads(data)
nrows = int(data["nrow"])
ncols = int(data["ncol"])
points = data["children"]

dist_matrix = []

for i in range(0,len(points)):
    dist_matrix.append([])
    irow,icol = get_row_col(nrows,ncols,points[i])
    for j in range(0,len(points)):
        if i!=j:
            jrow,jcol = get_row_col(nrows,ncols,points[j])
            dist_matrix[i].append(haversine(float(points[i]["long"]),float(points[i]["lat"]),float(points[j]["long"]),float(points[j]["lat"])))
        else:
            dist_matrix[i].append(0)

