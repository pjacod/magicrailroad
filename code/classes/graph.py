import pandas as pd
import matplotlib.pyplot as plt
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
        for route in range(1, total_routes + 1):
            self.route_dict[str(route)] = Route(str(route), self.station_dict)

    def show_routes(self):
        """
        TEMPORARY? shows the routes
        """
        print(self.route_dict)

    def visualize_station_percentage(self):
        """
        visualizes the percentage of stations used in the route.
        """
        self.route_percentages = {}

        for route_number, route in self.route_dict.items():

            used_stations = len(set(route.itinerary))
            total_stations = len(self.station_dict)
            unused_stations = total_stations - used_stations

            # calculate percentages
            percentage_used = (used_stations / total_stations) * 100
            percentage_unused = (unused_stations / total_stations) * 100
            self.route_percentages[route_number] = {'used': percentage_used, 'unused': percentage_unused}

            # data for pie chart
            sizes = [used_stations, unused_stations]
            labels = ['Used', 'Unused']

            plt.figure(figsize=(7, 7))
            plt.pie(sizes, labels=labels, colors=['red', 'blue'], autopct='%1.1f%%')
            plt.title(f'Percentage of stations used in route {route_number}')
            plt.show()

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
        print(f"The k value is : {self.k_value}")
        return self.k_value


    def write_output(self, output_file):
        """
        writes the route number and route percentages to an output file.
        """
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            f.write("Route, Percentage Used, Percentage Unused")
            for route_number, percentages in self.route_percentages.items():
                writer.writerow([route_number, f"{percentages['used']}", f"{percentages['unused']:}"])
