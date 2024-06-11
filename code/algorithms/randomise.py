# chooses a random starting point, and a random itinerary from there
import random


def random_route(route_dict):
    """
    Makes an instance of class Route choose a random itinerary
    """

    for key in route_dict:

        route = route_dict[key]

        # choose random starting point
        random_start(route)

        # choose connections until time is up
        while route.time <= 120:
            destinations = route.present_destinations(route.itinerary[-1].name)
            options = list(destinations.keys())
            choice = random.choice(options)
            time = destinations[choice]

            # make sure to add the Station instance and not just name
            route.add_station(route.station_dict[choice], time)


def random_start(route):
    """
    selects random starting point for route
    """
    station_names = list(route.station_dict.keys())
    choice = random.choice(station_names)
    route.add_station(route.station_dict[choice], 0)
