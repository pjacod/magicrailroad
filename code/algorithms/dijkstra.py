# make an algorithm that chooses a dead end as a starting point

# similar architecture to randomise to go through a step, but add a points system to the options
# should i add this points system to the  destinations dict of a station?
#  i think i should, that way it would carry over between routes as well
import random
import copy
from code.classes import graph

class Dijkstra():
    def __init__(self, graph, weights, a_star_layers=0):
        self.graph = copy.deepcopy(graph)
        self.dead_end_list = self.dead_end(self.graph.station_dict)

        self.weights = weights
        self.a_star_layers = a_star_layers


    def dead_end(self, station_dict):
        """
        returns a list of Stations that are dead ends(have only one destination)
        """
        list = []
        for name in station_dict.keys():
            if len(station_dict[name].destinations) == 1:
                list.append(station_dict[name])


        return list

    def random_greedy(self, start_station, route):
        """
        randomly selects an unused connection when available, does not go back where it came from unless only option
        """
        route.add_station(start_station, 0)

        while route.time <= self.graph.max_time:

            destinations = route.present_destinations(route.itinerary[-1].name)
            options = list(destinations.keys())

            # not exceeding the 120 minutes
            max_time = self.graph.max_time - route.time
            open_options = {}
            used_options = {}

            # iterate through destinations and travel time
            for destination, value in destinations.items():
                # if travel time is small enough: add to possible_options
                if value[0] <= max_time:
                    if value[1] == 0:
                        open_options[destination] = value

                    else:
                        used_options[destination] = value

            # if no more possible_options: break
            if open_options == {} and used_options == {}:
                break

            elif open_options:
                choice = random.choice(list(open_options.keys()))
                time = open_options[choice][0]

            else:
                choice = random.choice(list(used_options.keys()))
                time = used_options[choice][0]

            # make sure to add the Station instance and not just name
            route.add_station(route.station_dict[choice], time)


    def dijkstra_like(self, start_station, route):
        """
        start_station = Station instance (NOT station name)
        rus
        """
        route.add_station(start_station, 0)

        while route.time <= self.graph.max_time:
            current_station = route.itinerary[-1]

            destinations = route.present_destinations(current_station.name)

            # not exceeding the max minutes
            max_time = self.graph.max_time - route.time

            min_cost = 10000

            destination_boolean = False
            # iterate through destinations and cost
            for destination, value in destinations.items():

                distance = value[0]

                if distance <= max_time:

                    if self.a_star_layers == 0:
                        if len(route.itinerary > 1):
                            if route.itinerary[-2].name != destination:
                                cost = value[2]

                    else:
                        cost = self.a_star(destination, value, max_time)
                        if cost == 1000:
                            destination_boolean = False



                    if cost <= min_cost:
                        min_cost = cost
                        min_destination = destination
                        destination_boolean = True
                        time = distance



            if destination_boolean:
                route.add_station(route.station_dict[min_destination], time, self.weights)

            else:
                break


    def a_star(self, destination_name, value, max_time):
        """
        returns cost based on a_star_layers ahead of current destination
        cost is percentage of total connections in next layers that are still open
        reduces layers it looks at considering the amount of time left in route
        this is based on avg length of connection = 13 min
        """
        cost = 1000
        potential = 0


        # add 100 potential if current connection is unused
        if value[1] == 0:
            potential += 200


        previous_list = [self.graph.station_dict[destination_name]]

        # define layer range based on how much time left in route
        predicted_layers = int(max_time // 13)

        for layer in range(min([predicted_layers, self.a_star_layers])):
            all_stations = []
            open_count = 0
            total_count = 0

            for station in previous_list:
                open_count += station.open
                total_count += len(station.destinations.keys())

                for next_station_name in station.destinations.keys():
                    all_stations.append(self.graph.station_dict[next_station_name])

            previous_list = all_stations

            percentage = 100 * (open_count / total_count)
            potential += percentage


        cost -= potential
        return cost








    def deadend_start(self):
        """
        creates routes starting from each dead end station.
        runs until there are no more dead ends
        """
        # i counts the routes, important to start a new route every time
        i = 0

        while self.dead_end_list != []:
            i += 1

            start_station = random.choice(self.dead_end_list)
            self.dead_end_list.remove(start_station)

            # selects a route to build from graph dictionary
            route = self.graph.route_dict[str(i)]

            self.dijkstra_like(start_station, route)

        while self.graph.check_open() and i < self.graph.max_routes:

            i += 1

            # find specific station to start from from those in self.graph.open_list
            # HEURISTIC, trying to start from those with 1, 3, 5 open connections
            start_options = []
            for station in self.graph.open_list:
                if station.open == 1:
                    start_options.append(station)

            if start_options != []:
                start_station = random.choice(start_options)

                route = self.graph.route_dict[str(i)]
                self.dijkstra_like(start_station, route)

            else:
                for station in self.graph.open_list:
                    if station.open != 0:
                        start_options.append(station)

                start_station = random.choice(start_options)

                route = self.graph.route_dict[str(i)]
                self.dijkstra_like(start_station, route)




    def random_start(self):
        """
        creates routes starting from random stations
        chooses connection with lowest cost,
        runs until all connections have been made or no routes are left
        """
        i = 0
        while self.graph.check_open() and i < self.graph.max_routes:
            i += 1
            start_station = random.choice(self.graph.open_list)
            route = self.graph.route_dict[str(i)]
            self.random_greedy(start_station, route)



    def select_pairs():
        pass

    def proper_dijkstra():
        """
        """
        pass

    def run_dijkstra(self):
        """
        creates a Graph, then runs the dijkstra algorithm.
        'distance' or cost is based on the time, and how many times a connection has been run
        weights is a list, containing weights for [time, connection?]
        """
        self.graph.dijkstra_cost(self.weights)

        self.graph.add_routes(self.graph.max_routes)


        self.deadend_start()
        #self.random_start()

        print(f'K = {self.graph.calculate_k()}')
        return(self.graph.calculate_k())
