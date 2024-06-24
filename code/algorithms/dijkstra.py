# make an algorithm that chooses a dead end as a starting point

# similar architecture to randomise to go through a step, but add a points system to the options
# should i add this points system to the  destinations dict of a station?
#  i think i should, that way it would carry over between routes as well
import random
import copy
from code.classes import graph

class Dijkstra():
    def __init__(self, graph, max_time, max_routes, weights):
        self.graph = copy.deepcopy(graph)
        self.dead_end_list = self.dead_end(self.graph.station_dict)
        self.max_time = max_time
        self.max_routes = max_routes

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

        while route.time <= self.max_time:

            destinations = route.present_destinations(route.itinerary[-1].name)
            options = list(destinations.keys())

            # not exceeding the 120 minutes
            max_time = self.max_time - route.time
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
        """
        route.add_station(start_station, 0)

        while route.time <= self.max_time:

            destinations = route.present_destinations(route.itinerary[-1].name)

            # not exceeding the 120 minutes
            max_time = self.max_time - route.time

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


    def first_part(self):
        """
        creates routes starting from each dead end station.
        method to choose route is a kind of random greedy,
        that randomly selects an unused connection when available
        runs until there are no more dead ends
        """
        i = 0

        while self.dead_end_list != []:
            i += 1

            start_station = random.choice(self.dead_end_list)
            self.dead_end_list.remove(start_station)

            # selects a route to build from graph dictionary
            route = self.graph.route_dict[str(i)]

            self.dijkstra_like(start_station, route)


    def run_dijkstra(self):
        """
        creates a Graph, then runs the dijkstra algorithm.
        'distance' or cost is based on the time, and how many times a connection has been run
        weights is a list, containing weights for [time, connection?]
        """
        self.graph.dijkstra_cost(self.weights)

        self.graph.add_routes(self.max_routes)

        self.first_part()

        self.graph.show_routes()
        print(f'K = {self.graph.calculate_k()}')
