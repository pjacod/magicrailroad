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
        sets the self.destinations for this station, given the df
        as dictionary {destination : distance}
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

    def __repr__(self):
        return self.name


class Route():

    def __init__(self, number, station_dict):
        self.number = number

        # station_list is a list of instances of class Station
        self.station_dict = station_dict
        self.itinerary = []
        self.time = 0

    def present_destinations(self, station_name):
        """
        returns the potential destinations from a given station_name
        type = dict
        """
        return self.station_dict[station_name].destinations

    def add_station(self, station, time):
        """
        adds station(selected by outside algorithm), to the list containing itinerary
        and adds time to self.time
        """
        self.itinerary.append(station)
        self.time += time


    def show_status(self):
        """
        shows the current itinerary and time
        """
        return self.itinerary, self.time

    def __repr__(self):
        return f"Route {self.number}, {self.time} minutes; {self.itinerary}"


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


    def add_route(self, number):
        """
        creates an instance of class Route
        """
        self.route_dict[number] = Route(number, self.station_dict)

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

    def write_output(self, output_file): #########################3
        """
        writes the route number and route percentages to an output file.
        """
        with open(output_file, 'w') as f:
            f.write("Route,Percentage Used,Percentage Unused\n")
            for route_number, percentages in self.route_percentages.items():
                f.write(f"{route_number},{percentages['used']:.2f},{percentages['unused']:.2f}\n")

def random_route(route):
    """
    Makes an instance of class Route choose a random itinerary
    """
    # choose random starting point
    random_start(route)

    # choose connections until time is up
    while route.time <= 120:
        destinations = route.present_destinations(route.itinerary[0])
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


def main(input1, input2, output_file):

    # create a scenario
    scenario = Graph(input1, input2)

    # add a route to scenario
    scenario.add_route("1")

    random_route(scenario.route_dict["1"])
    scenario.visualize_station_percentage()

    scenario.show_routes()
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
