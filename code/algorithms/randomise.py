# chooses a random starting point, and a random itinerary from there
import random


def random_routes(route_dict):
    """
    Makes an instance of class Route choose a random itinerary
    """

    for key in route_dict:

        route = route_dict[key]

        # choose random starting point
        random_start(route)

        # choose connections until time is up
        while route.time <= 120:

            #randomly stop adding connections
            chance = random.randint(0, 9)
            if chance == 1:
                break

            destinations = route.present_destinations(route.itinerary[-1].name)
            options = list(destinations.keys())

            # not exceeding the 120 minutes
            max_time = 120 - route.time
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


def random_start(route):
    """
    selects random starting point for route
    """
    station_names = list(route.station_dict.keys())
    choice = random.choice(station_names)
    route.add_station(route.station_dict[choice], 0)


def amount_routes():
    return random.randint(1, 7)
