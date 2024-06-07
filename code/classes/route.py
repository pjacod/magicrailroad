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