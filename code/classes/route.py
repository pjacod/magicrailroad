


class Route():

    def __init__(self, number, station_list):
        self.number = number

        # station_list is a list of instances of class Station
        self.station_list = station_list
        self.itinerary = []
        self.time = 0

    def start_station(self):
        """
        select a starting station for the route
        """
        # not sure if this is going to work, it should take a random instance of class station and then take name
        self.itinerary.append(random.choice(self.station_list).name)

    def add_station(self):
        """
        add a connection to itinerary, by taking the last station in list and
        choosing one of the destinations from there
        """
        station_name = self.itinerary[-1]

        # find the instance of class Station that corresponds to current station
        for station in self.station_list:
            if station.name == station_name:

                current_station = station
                break

        # choose random station from list of destinations
        options = sorted(current_station.destinations.keys())
        next_station = random.choice(options)

        self.itinerary.append(next_station)
        self.time += current_station.destinations[next_station]

    def define_itinerary(self):
        """
        set the program to define itinerary, stopping when time passes 120
        """
        self.start_station()

        while self.time <= 120:
            self.add_station()

        return self.itinerary, self.time
