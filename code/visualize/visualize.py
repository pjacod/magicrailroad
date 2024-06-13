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


def bar_k(k_values):
    """
    generates a bar chart of k values per attempt.
    """
    iterations = range(1, len(k_values) + 1)

    plt.title('k values per iteration')
    plt.xlabel('attempts')
    plt.ylabel('k value')
    plt.bar(iterations, k_values)
    plt.grid(True)
    plt.show()

def histogram_k(k_values):
    """
    generates a histogram visualizing the distribution of k values.
    """

    plt.title('frequency per k_value')
    plt.xlabel('k_value')
    plt.ylabel('frequency')
    plt.hist(k_values, bins = 10)
    plt.grid(True)
    plt.show()
