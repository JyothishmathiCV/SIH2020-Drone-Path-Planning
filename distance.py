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
    return c * r * 1000

def get_row_col(nrow,ncol,obj):
    ob = obj["cellno"]
    row = ob//ncol
    col = ob%ncol
    return row,col

data = { "nrow":20, "ncol":23, "children":[{"lat","long","cellno"}] }
data = json.loads(data)
nrows = data["nrow"]
ncols = data["ncol"]
points = data["children"]

dist_matrix = []

for i in range(0,len(points)):
    dist_matrix.append([])
    irow,icol = get_row_col(nrows,ncols,points[i])
    for j in range(0,len(points)):
        if i!=j:
            jrow,jcol = get_row_col(nrows,ncols,points[j])
            dist_matrix[i].append(haversine(points[i]["lon"],points[i]["lat"],points[j]["lon"],points[j]["lat"]))

print(dist_matrix)