import pandas as pd
from .station import Station
from .route import Route
import csv


class Graph():

    def __init__(self, input1, input2):
        self.route_dict = {}

        self.dict = self.read_input_1(input1)
        self.df = self.read_input_2(input2)

        self.station_dict = self.create_station_dict()

    def read_input_1(self, input1):
        """
        reads a csv file containing the coordinate positions of every station.
        returns a dict with key=station : value=(x,y)
        """
        df = pd.read_csv(input1)

        dict = {}
        for index, row in df.iterrows():
            dict[row['station']] = (row['x'], row['y'])

        return dict

    def read_input_2(self, input2):
        """
        reads a csv file containing all connections between stations, and the
        corresponding travel time. returns a df
        """
        return pd.read_csv(input2)

    def create_station_dict(self):
        """
        using self.df and self.dict, creates a list of instances of class Station
        """
        station_dict = {}
        for key in self.dict.keys():

            # create instance of station, with name and location
            station = Station(key, self.dict[key])

            # call function to add destinations to Station, by using the df from input2
            station.define_destinations(self.df)

            # add station to station_dict
            station_dict[station.name] = station

        return station_dict


    def add_routes(self, total_routes):
        """
        creates instances of class Route
        """
        for route in range(total_routes):
            self.route_dict[str((route + 1))] = Route(str(route), self.station_dict)

    def remove_route(self, route):
        """
        removes instance of route
        """
        self.route_dict.pop(route)

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
        return self.k_value, p


    def dijkstra_cost(self, weights):
        """
        use a list of weights to update cost for every connection for every station in graph
        necessary for using dijkstra algorithm
        """
        for station_name in self.station_dict:
            station = self.station_dict[station_name]
            for key in station.destinations.keys():

                new_cost = weights[0] * station.destinations[key][0] + weights[1] * station.destinations[key][1]
                station.destinations[key][2] = new_cost


    '''def write_output(self, output_file):
        """
        writes the route number and route percentages to an output file.
        """
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            f.write("Route, Percentage Used, Percentage Unused")
            for route_number, percentages in self.route_percentages.items():
                writer.writerow([route_number, f"{percentages['used']}", f"{percentages['unused']:}"])'''
