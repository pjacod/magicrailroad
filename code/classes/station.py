
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
