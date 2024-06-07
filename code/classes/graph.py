
from .station import Station
from .route import Route

class Graph():

    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2
        self.route_list = []

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
        itinerary, time =
        self.route_list.append((itinerary, time))

    def show_routes(self):
        print(self.route_list)
