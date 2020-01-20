"""Vehicles Routing Problem (VRP)."""
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

    # speed = data_json["speed"]
        # life = data_json["life"]
        # filename = data_json["filename"]
        # no_of_drones = data_json["no_of_drones"]
        # charging_points = data_json["charging_points"]

def create_data_model(data_json):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = data_json['distance_matrix']
    mapping_points = data_json['mapping_points']
    charging_points = []
    #Home depot is the first charging point - by default
    home_depot = data_json['mapping_points'][data_json['charging_points'][0]['cellno']]
    
    for i in data_json['charging_points']: # This will give the index of the charging point in the distance matrix
        charging_points.append(data_json['mapping_points'][i['cellno']])
    
    dist = data['distance_matrix']
    
    #Deleting all the charging point columns in the distance matrix
    for i in range(0,len(data['distance_matrix'])):
        dist.append([])
        for j in range(0,len(data['distance_matrix'][i])):
            if j not in charging_points:
                dist[i].append(data['distance_matrix'][i][j])

    charging_station = []

    dist2 = []
    k = 0
    # ncs = -1
    for i in range(0,len(dist)):
        if i in charging_points:
            if i == home_depot:
                charging_station.append(dist[i])
                dist2.append(dist[i])
                mapping_points = modify_mapping_point(mapping_points,i,k)
                k += 1   
            else:
                charging_station.append(dist[i])
                modify_mapping_point(mapping_points,i,-charging_points.index(i)-1)
                # ncs -= 1
        else:
            dist2.append(dist[i])
            mapping_points = modify_mapping_point(mapping_points,i,k)
            k += 1       

    data['distance_matrix'] = dist2
    data['charging_station'] = charging_station #Copy the values to data from data_json
    data['mapping_points'] = mapping_points
    data['num_vehicles'] = data_json['no_of_drones']
    data['range_of_drone'] = data_json['life']
    data['speed'] = data_json['speed']
    data['depot'] = home_depot
    data['no_of_rows'] = data_json['nrows']
    data['no_of_cols'] = data_json['ncols']
    return data

def convert_to_cellno(data,index):
    # nrows = data['no_of_rows']
    # ncols = data['no_of_cols']
    mapping = data['mapping_points']
    for cellno in mapping:
        if mapping[cellno][2] == index:
            return mapping[cellno][0],mapping[cellno][1],cellno
    return -1,-1,-1

def modify_mapping_point(mapping_points,pindex,cindex):
    for cellno in mapping_points:
        if(mapping_points[cellno][2] == pindex):
            mapping_points[cellno][2] == cindex
            return mapping_points
    return False


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    max_route_distance = 0
    routing_path = []
    k = -1
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        ranged=data['range_of_drone']
        prev=data['depot']
        routing_path.append([])
        k+=1
        while not routing.IsEnd(index):
            stationindex=data['depot']
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            irow,icol,icellno = convert_to_cellno(data,manager.IndexToNode(index))
            routing_path[k].append([irow,icol,icellno]) 
            ranged-=data["distance_matrix"][manager.IndexToNode(prev)][manager.IndexToNode(index)]
            prev=index
            previous_index = index
            index = solution.Value(routing.NextVar(index)) #Index = next node, prev = previous node
            # Decide if we have to go to the charging point or not
            for i,j in enumerate(data["charging_station"]):
                if data["charging_station"][i][manager.IndexToNode(index)] < data["charging_station"][stationindex][manager.IndexToNode(index)]:
                    stationindex=i
            if ranged <= data["distance_matrix"][manager.IndexToNode(prev)][manager.IndexToNode(index)] + data["charging_station"][stationindex][manager.IndexToNode(index)]:
                plan_output += '  {}  Charging -> '.format(manager.IndexToNode(stationindex))
                irow,icol,icellno = convert_to_cellno(data,-manager.IndexToNode(stationindex)-1)
                routing_path[k].append([irow,icol,icellno])
                ranged=data['range_of_drone']-data["charging_station"][stationindex][manager.IndexToNode(index)]
                # TODO
                # Modify distance covered by the drone in reaching the charging point and returning back - route_distance

            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        # print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)

    print('Maximum of the route distances: {}m'.format(max_route_distance))
    return routing_path




def main(data_json):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model(data_json)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        2000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(data, manager, routing, solution)



if __name__ == '__main__':
    import sys
    main(sys.argv[1])