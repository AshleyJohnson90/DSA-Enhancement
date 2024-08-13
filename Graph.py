# Graph class holds the methods to create the graph that will store the locations and directions

class Graph:
    def __init__(self):
        self.connected_locations = {}

    # method to add locations(nodes) to the graph
    def add_location(self, location_name):
        if location_name not in self.connected_locations:
            self.connected_locations[location_name] = {}

    # method to add connections(edges) to connect locations to each other using an undirected graph
    def add_connection(self, location_name1, direction, location_name2, opposite_direction):
        self.connected_locations[location_name1][direction] = location_name2
        self.connected_locations[location_name2][opposite_direction] = location_name1

    # gets the connection(direction) from one location to the other
    def get_connections(self, location_name):
        return self.connected_locations.get(location_name, {})

    # depth first search to find the shortest path to visit all the locations and end in the Dining Room
    def shortest_path(self, start_location, end_location):
        NUMBER_OF_LOCATIONS = 8
        path_directions = []
        visited = set()

        # every location that is visited needs to be stored in a set so the algorithm knows it has visited the location and not
        # an infinite loop through the locations
        def dfs(current_location):
            if current_location in visited:
                return False

            visited.add(current_location)

            # if the location is the end location and all 8 locations have been visited, return True that there is a path
            if current_location == end_location and len(visited) == NUMBER_OF_LOCATIONS:
                return True

            # if the connected location is not in visited, add the direction to the path directions list
            for direction, connected_location in self.connected_locations[current_location].items():
                if connected_location not in visited:
                    path_directions.append(direction)
                    if dfs(connected_location):
                        return True
                    path_directions.pop()

            visited.remove(current_location)
            return False

        # if the depth first search finds a path, return the list of path directions or none if no valid path found
        if dfs(start_location):
            return path_directions
        else:
            return None
