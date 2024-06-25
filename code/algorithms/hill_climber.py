import copy
import random

class Hillclimber():

    def __init__(self, graph):
        self.graph = copy.deepcopy(graph)
        self.route_dict = self.graph.route_dict

    def run(self, iterations, progression = False):
        '''
        runs hill climber algorithm
        '''
        # list of k_values for each iteration
        k_values = []

        # keep track of the amount of iterations passed
        counter_progression = 0


        for key in self.route_dict:
            route = self.route_dict[key]

            # create a random state as a start
            self.starting_state(route)

        # apply iterations times a change
        for iteration in range(iterations):

            # make a copy of the last version of self.graph
            copy_graph = copy.deepcopy(self.graph)

            # return a random route and its itinerary
            chosen_route_key, chosen_route, route_itinerary = self.random_route_choice(copy_graph)

            # if heuristics are enabled apply changes in progression
            if progression:

                # choose and apply the right change applying function
                function_scale = self.choose_scale(counter_progression, iterations)
                function_scale(copy_graph, chosen_route_key, chosen_route, route_itinerary)

                new_graph = copy_graph

                counter_progression += 1

            # if heuristics aren't enabled apply a random change applying function
            else:
                new_graph = self.random_change(copy_graph, chosen_route_key, chosen_route, route_itinerary)

            # if applied changes return better results go further with the new graph
            self.check_graph(new_graph)

            k_values.append(self.graph.calculate_k())
        return self.graph, k_values


    def starting_state(self, route):
        '''
        initializes a random starting state
        '''

        station_names = list(route.station_dict.keys())
        choice = random.choice(station_names)
        route.add_station(route.station_dict[choice], 0)

        self.fill_route(route)


    def fill_route(self, route, stop_chance = 9):

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
                if distance <= max_time:
                    possible_options[destination] = distance

            # if no more possible_options: break
            if not possible_options:
                break

            # randomly select one of the possible destinations
            choice = random.choice(list(possible_options.keys()))
            time = possible_options[choice]

            # make sure to add the Station instance and not just name
            route.add_station(route.station_dict[choice], time)

    def random_change(self, graph, chosen_route_key, chosen_route, chosen_itinerary):
        '''
        returns a random change to apply
        '''
        # list of all changes methods
        changes_methods = [self.changes_scale_1,
        self.changes_scale_2, self.changes_scale_3,
        self.changes_scale_4, self.changes_scale_5]

        # randomly pick one and apply it on the graph
        random_change = random.choice(changes_methods)
        random_change(graph, chosen_route_key, chosen_route, chosen_itinerary)

        return graph

    def random_route_choice(self, graph):
        '''
        returns a random route and its itinerary for a graph
        '''

        random_route_key = random.choice(list(graph.route_dict.keys()))
        chosen_route = graph.route_dict[random_route_key]
        route_itinerary = chosen_route.itinerary

        return random_route_key, chosen_route, route_itinerary

    def choose_scale(self, counter_progression, iterations):
        '''
        picks the appropriate change function for the amount of iterations
        '''
        # determine how many iterations each method is used
        fifth_iterations = iterations / 5

        # return the right method
        if counter_progression < fifth_iterations:
            return self.changes_scale_1

        elif counter_progression < 2 * fifth_iterations:
            return self.changes_scale_2

        elif counter_progression < 3 * fifth_iterations:
            return self.changes_scale_3

        elif counter_progression < 4 * fifth_iterations:
            return self.changes_scale_4

        else:
            return self.changes_scale_5


    def changes_scale_1(self, graph, chosen_route_key, chosen_route, chosen_itinerary):
        '''
        randomly adds or removes a route
        '''
        # initiate a random chance for either adding or removing a route
        chance = random.random()

        if chance <= 0.5:
            #print(graph.route_dict)
            # adds a new route with random itinerary
            if len(graph.route_dict) < graph.max_routes:
                route_added = graph.add_routes(1)
                self.starting_state(graph.route_dict[route_added])
                self.fill_route(graph.route_dict[route_added])

        else:
            # removes a route
            if len(graph.route_dict) > 0:
                graph.remove_route(chosen_route_key)

    def changes_scale_2(self, graph, chosen_route_key, chosen_route, itinerary):
        '''
        removes and adds rougly two thirds of a random routes' itinerary
        '''
        length_itinerary = len(itinerary)

        # if itinerary is big enough
        if length_itinerary >= 3:

            # randomly remove roughly the first or the last two-thirds of the itinerary
            chance = random.random()
            if chance <= 0.5:
                keep_index = length_itinerary // 3
                chosen_route.itinerary = itinerary[:keep_index]

            else:
                keep_index = length_itinerary - length_itinerary // 3
                chosen_route.itinerary = itinerary[keep_index:]

            # fill in the route with new stations
            self.fill_route(chosen_route, 5)

    def changes_scale_3(self, graph, chosen_route_key, chosen_route, itinerary):
        '''
        removes and adds half of a random routes' itinerary
        '''
        length_itinerary = len(itinerary)

        # if itinerary is big enough
        if length_itinerary >= 2:

            # randomly remove roughly the first or the second half of the itinerary
            chance = random.random()
            if chance <= 0.5:
                keep_index = length_itinerary // 2
                chosen_route.itinerary = itinerary[:keep_index]

            else:
                keep_index = length_itinerary - length_itinerary // 2
                chosen_route.itinerary = itinerary[keep_index:]

            # fill in the route with new stations
            self.fill_route(chosen_route, 5)

    def changes_scale_4(self, graph, chosen_route_key, chosen_route, itinerary):
        '''
        removes and adds roughly a third of a random routes' itinerary
        '''
        length_itinerary = len(itinerary)

        # if itinerary is big enough
        if length_itinerary >= 2:

            # randomly remove roughly the first or the last third of the itinerary
            chance = random.random()
            if chance <= 0.5:
                keep_index = int(length_itinerary // 1.5)
                chosen_route.itinerary = itinerary[:keep_index]

            else:
                keep_index = int(length_itinerary - length_itinerary // 1.5)
                chosen_route.itinerary = itinerary[keep_index:]

            # fill in the route with new stations
            self.fill_route(chosen_route, 5)

    def changes_scale_5(self, graph, chosen_route_key, chosen_route, itinerary):
        '''
        removes and adds the begin or end station of a random routes' itinerary
        '''
        length_itinerary = len(itinerary)

        # if itinerary is big enough
        if length_itinerary >= 2:

            # randomly remove roughly the first or the last third of the itinerary
            chance = random.random()
            if chance <= 0.5:
                chosen_route.itinerary = itinerary[:length_itinerary - 1]

            else:
                chosen_route.itinerary = itinerary[1:]

            # fill in the route with new stations
            self.fill_route(chosen_route, 5)

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
