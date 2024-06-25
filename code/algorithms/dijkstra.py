# make an algorithm that chooses a dead end as a starting point

# similar architecture to randomise to go through a step, but add a points system to the options
# should i add this points system to the  destinations dict of a station?
#  i think i should, that way it would carry over between routes as well
import random
import copy
from code.classes import graph

class Dijkstra():
    def __init__(self, graph, weights):
        self.graph = copy.deepcopy(graph)
        self.dead_end_list = self.dead_end(self.graph.station_dict)

        self.weights = weights


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

            destinations = route.present_destinations(route.itinerary[-1].name)

            # not exceeding the 120 minutes
            max_time = self.graph.max_time - route.time

            min_cost = 10000

            destination_boolean = False
            # iterate through destinations and cost
            for destination, value in destinations.items():

                distance = value[0]
                cost = value[2]

                # skip previous station, as we do not want to backtrack
                if destination != route.itinerary[-1].name and distance <= max_time:

                    if cost <= min_cost:
                        min_cost = cost
                        min_destination = destination
                        destination_boolean = True
                        time = distance

            if destination_boolean:
                route.add_station(route.station_dict[min_destination], time, self.weights)

            else:
                break


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

            self.random_greedy(start_station, route)

        while self.graph.check_open():

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
                self.random_greedy(start_station, route)

            else:
                for station in self.graph.open_list:
                    if station.open != 0:
                        start_options.append(station)

                start_station = random.choice(start_options)

                route = self.graph.route_dict[str(i)]
                self.random_greedy(start_station, route)




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
