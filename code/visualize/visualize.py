from matplotlib import pyplot as plt

def visualize_station_percentage(graph):
    """
    visualizes the percentage of stations used in the route.
    """

    graph.route_percentages = {}

    for route_number, route in graph.route_dict.items():

        used_stations = len(set(route.itinerary))
        total_stations = len(graph.station_dict)
        unused_stations = total_stations - used_stations

        # calculate percentages
        percentage_used = (used_stations / total_stations) * 100
        percentage_unused = (unused_stations / total_stations) * 100
        graph.route_percentages[route_number] = {'used': percentage_used, 'unused': percentage_unused}

        # data for pie chart
        sizes = [used_stations, unused_stations]
        labels = ['Used', 'Unused']

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, colors=['red', 'blue'], autopct='%1.1f%%')
        plt.title(f'Percentage of stations used in route {route_number}')
        plt.show()

def histogram_k(costs):

    plt.title('cost per iteration')
    plt.xlabel('cost')
    plt.ylabel('frequency')
    plt.hist(costs, bins = )
    plt.show()
