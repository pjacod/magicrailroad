import random
from .station import Station

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

    def add_station(self, station, time, weights=[]):
        """
        adds station(selected by outside algorithm), to the list containing itinerary
        and adds time to self.time
        adds a connection count to station.destinations
        """

        if self.itinerary != []:
            last_station = self.itinerary[-1]
            station.destinations[last_station.name][1] += 1
            last_station.destinations[station.name][1] +=1

            if weights != []:
                station.destinations[last_station.name][2] += weights[1]
                last_station.destinations[station.name][2] += weights[1]



        self.itinerary.append(station)
        self.time += time




    def show_status(self):
        """
        shows the current itinerary and time
        """
        return self.itinerary, self.time

    #def dijkstra_options(self):
        """
        make a dictionary to store options while running dijkstra
        dict = {key}
        """
        #self.dijkstra_options = {}


    def __repr__(self):
        return f"Route {self.number}, {self.time} minutes; {self.itinerary}"
