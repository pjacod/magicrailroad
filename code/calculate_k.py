    def calculate_k(self):
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
        K = p * 10000 - (T * 100 + Min)
        self.k_values.append(K)
        return K
