import copy
import random

class Hillclimber():

    def __init__(self, graph, progression, iteration_division = None):
        self.graph = copy.deepcopy(graph)
        self.route_dict = self.graph.route_dict

        self.iterations_division = iteration_division
        self.progression = progression

    def run(self, iterations, progression = False):
        '''
        runs hill climber algorithm
        '''
        # list of k_values for each iteration
        k_values = []

        # keep track of the amount of iterations passed
        counter_progression = 0

        # create a random starting routes
        for key in self.route_dict:
            route = self.route_dict[key]
            self.starting_state(route)

        # apply iterations times a change
        for iteration in range(iterations):
            copy_graph = copy.deepcopy(self.graph)

            # return a random route and its itinerary
            chosen_route_key, chosen_route = self.random_route_choice(copy_graph)

            # if heuristics are enabled apply changes in progression
            if self.progression == True:

                # choose and apply the right change applying function
                function_scale = self.choose_scale(counter_progression, iterations)
                function_scale(copy_graph, chosen_route_key, chosen_route)
                new_graph = copy_graph

                counter_progression += 1

            # if heuristics aren't enabled apply a random change applying function
            else:
                new_graph = self.random_change(copy_graph, chosen_route_key, chosen_route)

            # if applied changes return better results go further with the new graph
            self.check_graph(new_graph)

            # append k_value of chosen graph to list
            k_value = self.graph.calculate_k()
            k_values.append(k_value)


        return k_value


    def starting_state(self, route):
        '''
        initializes a random starting state
        '''

        station_names = list(route.station_dict.keys())
        choice = random.choice(station_names)
        route.add_station(route.station_dict[choice], 0)

        self.fill_route(route, self.graph.average_connections)


    def fill_route(self, route, stop_chance):
        '''
        creates a random itinerary for a route instance
        '''

        while route.time <= self.graph.max_time:

            #randomly stop adding connections
            chance = random.randint(0, stop_chance)
            if chance == 1:
                break

            destinations = route.present_destinations(route.itinerary[-1].name)
            options = list(destinations.keys())

            # not exceeding the maximum time
            max_time = self.graph.max_time - route.time
            possible_options = {}

            # iterate through destinations and travel time
            for destination, distance in destinations.items():

                # if travel time is small enough: add to possible_options
                if distance[0] <= max_time:
                    possible_options[destination] = distance[0]

            # if no more possible_options: break
            if not possible_options:
                break

            # randomly select one of the possible destinations
            choice = random.choice(list(possible_options.keys()))
            time = possible_options[choice]

            # make sure to add the Station instance and not just name
            route.add_station(route.station_dict[choice], time)


    def random_route_choice(self, graph):
        '''
        returns a random route and its itinerary for a graph
        '''

        random_route_key = random.choice(list(graph.route_dict.keys()))
        chosen_route = graph.route_dict[random_route_key]
        route_itinerary = chosen_route.itinerary

        return random_route_key, chosen_route


    def random_change(self, graph, chosen_route_key, chosen_route):
        '''
        returns a random change to apply
        '''
        # list of all changes methods
        changes_methods = [self.changes_scale_1,
        self.changes_scale_2, self.changes_scale_3,
        self.changes_scale_4, self.changes_scale_5]

        # randomly pick one and apply it on the graph
        random_change = random.choice(changes_methods)
        random_change(graph, chosen_route_key, chosen_route)

        return graph


    def choose_scale(self, counter_progression, iterations):
        '''
        picks the appropriate change function for the amount of iterations
        '''
        iterations_1 = iterations * self.iterations_division[0]
        iterations_2 = iterations_1 + iterations * self.iterations_division[1]
        iterations_3 = iterations_2 + iterations * self.iterations_division[2]
        iterations_4 = iterations_3 + iterations * self.iterations_division[3]

        # return the right method
        if counter_progression < iterations_1:
            return self.changes_scale_1

        elif counter_progression < iterations_2:
            return self.changes_scale_2

        elif counter_progression < iterations_3:
            return self.changes_scale_3

        elif counter_progression < iterations_4:
            return self.changes_scale_4

        else:
            return self.changes_scale_5


    def replace_itinerary(self, chosen_route, scale_divider):
        '''
        replaces part of a route's itinerary
        '''
        length_itinerary = len(chosen_route.itinerary)

        # if itinerary is big enough
        if length_itinerary >= scale_divider:

            # randomly removes the first or last part of the itinerary
            chance = random.random()
            if chance <= 0.5:
                # scale_divider decides how big the part is
                keep_index = int(length_itinerary // scale_divider)
                chosen_route.itinerary = chosen_route.itinerary[:keep_index]

            else:
                keep_index = int(length_itinerary - length_itinerary // scale_divider)
                chosen_route.itinerary = chosen_route.itinerary[keep_index:]

            # fill in the route with new stations
            self.fill_route(chosen_route, self.graph.average_connections)

    def changes_scale_1(self, graph, chosen_route_key, chosen_route):
        '''
        randomly adds or removes a route
        '''
        # initiate a random chance for either adding or removing a route
        chance = random.random()

        if chance <= 0.5:

            # adds a new route with random itinerary
            if len(graph.route_dict) < graph.max_routes:
                route_added = graph.add_routes(1)
                self.starting_state(graph.route_dict[route_added])
                self.fill_route(graph.route_dict[route_added], self.graph.average_connections)

        else:

            # removes a route
            if len(graph.route_dict) > 0:
                graph.remove_route(chosen_route_key)


    def changes_scale_2(self, graph, chosen_route_key, chosen_route):
        '''
        removes and adds rougly two thirds of a random routes' itinerary
        '''
        self.replace_itinerary(chosen_route, 3)


    def changes_scale_3(self, graph, chosen_route_key, chosen_route):
        '''
        removes and adds half of a random routes' itinerary
        '''
        self.replace_itinerary(chosen_route, 2)


    def changes_scale_4(self, graph, chosen_route_key, chosen_route):
        '''
        removes and adds roughly a third of a random routes' itinerary
        '''
        self.replace_itinerary(chosen_route, 1.5)


    def changes_scale_5(self, graph, chosen_route_key, chosen_route):
        '''
        removes and adds the begin or end station of a random routes' itinerary
        '''
        length_itinerary = len(chosen_route.itinerary)

        # if itinerary is big enough
        if length_itinerary >= 2:

            # randomly remove roughly the first or the last third of the itinerary
            chance = random.random()
            if chance <= 0.5:
                chosen_route.itinerary = chosen_route.itinerary[:length_itinerary - 1]

            else:
                chosen_route.itinerary = chosen_route.itinerary[1:]

            # fill in the route with new stations
            self.fill_route(chosen_route, self.graph.average_connections)


    def check_graph(self, new_graph):
        '''
        checks if new graph is better than old one
        and if so moves forward with the new graph
        '''
        # calculate quality of old and new state
        quality_state = self.graph.calculate_k()
        quality_changed_state = new_graph.calculate_k()

        # move further with the graph with the best state quality
        if quality_changed_state >= quality_state:
            self.graph = new_graph
