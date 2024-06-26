
class Station():

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.destinations = {}

        self.open = 0

    def define_destinations(self, df):
        """
        sets the self.destinations for this station, given the df
        as dictionary {destination : [distance, counter, cost]}
        """

        # iterate over rows of df, save every destinations
        for index, row in df.iterrows():
            if row['station1'] == self.name:
                self.destinations[row['station2']] = [row['distance'], 0, 0]

            if row['station2'] == self.name:
                self.destinations[row['station1']] = [row['distance'], 0, 0]

        # set self.open
        self.open = len(self.destinations.keys())

<<<<<<< HEAD

=======
>>>>>>> b0b45e377a5e3471ba3f7f5c708673d54561ef13
    def __repr__(self):
        return self.name
