import math
import algorithm

def distance(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return int(math.sqrt((x1-x2)**2+(y1-y2)**2))

points = []
distance_matrix = []

for i in range(0,10):
    for j in range(0,10):
        points.append((i*10,j*10))
# print(len(points))

for i in range(0,10*10):
    distance_matrix.append([])
    for j in range(0,10*10):
        distance_matrix[i].append(distance(points[i],points[j]))

# m = 0
# for i in distance_matrix:
#     if max(i) > m:
#         m = max(i)

# print((distance_matrix))
# print(distance((0,0),(10,10)))
data = {}

mapping_points = {}

for i in range(0,10):
    for j in range(0,10):
            mapping_points[str(i*10+j+1)] = (i+1,j+1,i*10+j)

# print(mapping_points)

charging_station = []
charging_point = [15,57]

for i in charging_point:
    charging_station.append(distance_matrix[i])

data['distance_matrix'] = distance_matrix
data['charging_points'] = charging_point
data['charging_station'] = charging_station #Copy the values to data from data_json
data['mapping_points'] = mapping_points
data['no_of_drones'] = 4
data['life'] = 150
data['speed'] = 25
data['depot'] = 65
data['nrows'] = 20
data['ncols'] = 20

print("===============")

routing_path = algorithm.main(data)

print("===============")
sample = {}
for i in routing_path:
    for j in i:
        del j[2]
    print(len(i))
sample["drone_routes"] = routing_path
sample['width'] = 'xx'
sample['height'] = 'xx'
sample['grid_size'] = [10,10]
sample['image'] = 'xx'
print(sample)

