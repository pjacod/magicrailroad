import pandas as pd
from .station import Station
from .route import Route
import csv
import random


class Graph():

    def __init__(self, stations_csv_path, connections_csv_path):

        if stations_csv_path == 'data/StationsHolland.csv':
            self.max_routes = 7
            self.max_time = 120
            self.average_connections = 9

        else:
            self.max_routes = 20
            self.max_time = 180
            self.average_connections = 10

        self.available_keys = set(range(1, self.max_routes + 1))

        self.route_dict = {}

        self.dict = self.read_input_1(stations_csv_path)
        self.df = self.read_input_2(connections_csv_path)

        self.station_dict = self.create_station_dict()

        self.open_stations = []
        self.open = True

    def read_input_1(self, stations_csv_path):
        """
        reads a csv file containing the coordinate positions of every station.
        returns a dict with key=station : value=(x,y)
        """
        df = pd.read_csv(stations_csv_path)

        dict = {}
        for index, row in df.iterrows():
            dict[row['station']] = (row['x'], row['y'])

        return dict

    def read_input_2(self, connections_csv_path):
        """
        reads a csv file containing all connections between stations, and the
        corresponding travel time. returns a df
        """
        return pd.read_csv(connections_csv_path)

    def create_station_dict(self):
        """
        using self.df and self.dict, creates a list of instances of class Station
        """
        station_dict = {}
        for key in self.dict.keys():

            # create instance of station, with name and location
            station = Station(key, self.dict[key])

            # call function to add destinations to Station, by using the df from connections_csv_path
            station.define_destinations(self.df)

            # add station to station_dict
            station_dict[station.name] = station

        return station_dict

    def check_open(self):
        """
        checks whether there are any open connections still to make
        """
        self.open_list = []

        for station in self.station_dict.values():
            if station.open != 0:
                self.open_list.append(station)

        if self.open_list == []:
            self.open = False

        return self.open


    def amount_routes(self):
        return random.randint(1, self.max_routes)


    def add_routes(self, total_routes):
        """
        creates instances of class Route
        """

        for route in range(total_routes):

            key = str(random.choice(list(self.available_keys)))
            self.route_dict[key] = Route(key, self.station_dict)

            self.available_keys.remove(int(key))

        return key

    def remove_route(self, route):
        """
        removes instance of route
        """
        self.route_dict.pop(route)
        self.available_keys.add(int(route))

    def show_routes(self):
        """
        TEMPORARY? shows the routes
        """
        print(self.route_dict)

    def calculate_k(self):
        """
        calculates the k the percentage of stations used in the route.
        """
        # int
        total_connections = self.df.shape[0]
        used_connections = set()
        total_time = 0

        for route in self.route_dict.values():
            total_time += route.time
            for i in range(len(route.itinerary) - 1):
                station1 = route.itinerary[i].name
                station2 = route.itinerary[i + 1].name

                # if station1 and station2 are in the same row in df
                if ((self.df['station1'] == station1) & (self.df['station2'] == station2)).any() or \
                    ((self.df['station1'] == station2) & (self.df['station2'] == station1)).any():

                    # sort stations in connection alphabetically (to avoid duplicates)
                    connection = tuple(sorted((station1, station2)))
                    used_connections.add(connection)

        p = len(used_connections) / total_connections
        T = len(self.route_dict)
        Min = total_time
        self.k_value = p * 10000 - (T * 100 + Min)
        #print(f"The k value is : {self.k_value}")
        return self.k_value


    def define_cost(self, weights):
        """
        use a list of weights to set cost for every connection for every station in graph
        necessary for using greedy algorithm
        """
        for station_name in self.station_dict:
            station = self.station_dict[station_name]
            for key in station.destinations.keys():

                new_cost = weights[0] * station.destinations[key][0] + weights[1] * station.destinations[key][1]
                station.destinations[key][2] = new_cost

    def a_star(self, weights):
        pass

    def check_50(self, filename):
        '''
        saves the last route and k_value, and writes them to an output file for the check50
        '''
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # write routes
            writer.writerow(['train', 'stations'])
            for name, route in self.route_dict.items():
                stations_list = [station.name for station in route.itinerary]

                # join station names with comma and space
                stations_str = ', '.join(stations_list)
                writer.writerow([f'train_{name}', f'[{stations_str}]'])

            # write score
            writer.writerow(['score', self.k_value])
