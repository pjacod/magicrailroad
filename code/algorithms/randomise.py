# chooses a random starting point, and a random itinerary from there
import random


def random_route(route):
    """
    Makes an instance of class Route choose a random itinerary
    """
    ### BUGCHECK
    print(route.station_dict)
    # choose random starting point
    random_start(route)

    # choose connections until time is up
    while route.time <= 120:
        destinations = route.present_destinations(route.itinerary[-1])
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
    route.add_station(random.choice(station_names), 0)
