from code.algorithms import randomise
from code.classes import graph


def main_loop(input1, input2, iterations):
    lst_k_values = []

    for solution in range(iterations):
        # create a scenario
        test_graph = graph.Graph(input1, input2)

        amount = randomise.amount_routes()

        # add a route to scenario
        test_graph.add_routes(amount)

        # use randomise to choose itinerary for route
        randomise.random_routes(test_graph.route_dict)

        # calculate k_value of traject
        lst_k_values.append(test_graph.calculate_k())

    return lst_k_values, test_graph
