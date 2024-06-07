# Tweede draft representation, 7-6-2024
# Pierre Jacod
# Sofie van der Westen
import random
import pandas as pd
import argparse
import matplotlib.pyplot as plt

class Station():

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.destinations = {}

    def define_destinations(self, df):
        """
        sets the destinations for this station, given the df
        """

        # iterate over rows of df, save every destinations
        for index, row in df.iterrows():
            if row['station1'] == self.name:
                self.destinations[row['station2']] = row['distance']

            if row['station2'] == self.name:
                self.destinations[row['station1']] = row['distance']


    def count_connection(self):
        """
        maybe implement a function that keeps count of which stations this station
        is already connected with?
        """
        pass


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




class Scenario():

    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2
        self.route_list = []
        self.route_percentages = {}

        self.read_input_1(input1)
        self.read_input_2(input2)
        self.create_station_list()


    def read_input_1(self, input1):
        """
        reads a csv file containing the coordinate positions of every station.
        returns a dict with key=station : value=(x,y)
        """
        df = pd.read_csv(input1)

        dict = {}
        for index, row in df.iterrows():
            dict[row['station']] = (row['x'], row['y'])

        self.dict = dict

    def read_input_2(self, input2):
        """
        reads a csv file containing all connections between stations, and the
        corresponding travel time. returns a df
        """
        self.df = pd.read_csv(input2)

    def create_station_list(self):
        """
        using self.df and self.dict, creates a list of instances of class Station
        """
        station_list = []
        for key in self.dict.keys():
            # create instance of station, with name and location
            station = Station(key, self.dict[key])

            # call function to add destinations to Station, by using the df from input2
            station.define_destinations(self.df)

            # add station to station_list
            station_list.append(station)

        self.station_list = station_list


    def add_route(self, number):
        """
        creates an instance of class Route, and lets it define an itinerary
        """
        route = Route(number, self.station_list)
        route.start_station()
        itinerary, time = route.define_itinerary()
        self.route_list.append((itinerary, time))

    def show_routes(self):
        print(self.route_list)

    def visualize_station_percentage(self):
        """
        visualizes the percentage of stations used in the route.
        """
        total_stations = len(self.station_list)
        route_number = 1
        for route in self.route_list:

            used_stations = len(set(route[0]))
            unused_stations = total_stations - used_stations

            percentage_used = (used_stations / total_stations) * 100
            percentage_unused = (unused_stations / total_stations) * 100

            self.route_percentages[route_number] = {'used': percentage_used, 'unused': percentage_unused}

            # data for pie chart
            sizes = [used_stations, unused_stations]
            labels = ['Used', 'Unused']

            plt.figure(figsize=(7, 7))
            plt.pie(sizes, labels=labels, colors=['red', 'blue'], autopct='%1.1f%%')
            plt.title(f'Percentage van de stations die gebruikt zijn in route {route_number}')
            plt.show()

            route_number += 1

    def write_output(self, output_file):
        """
        writes the route number and route percentages to an output file.
        """
        with open(output_file, 'w') as f:
            f.write("Route,Percentage Used,Percentage Unused\n")
            for route_number, percentages in self.route_percentages.items():
                f.write(f"{route_number},{percentages['used']:.2f},{percentages['unused']:.2f}\n")


def main(input1, input2, output_file):

    # create a scenario
    scenario = Scenario(input1, input2)

    # add a route to scenario
    scenario.add_route("1")
    scenario.show_routes()
    scenario.visualize_station_percentage()
    scenario.write_output(output_file)



if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "read both input file name")

    parser.add_argument("input1", help = "input file 1 (csv)")
    parser.add_argument("input2", help = "input file 2 (csv)")
    parser.add_argument("output_file", help="output file (csv)")


    # Read arguments from command line
    args = parser.parse_args()

    main(args.input1, args.input2, args.output_file)
