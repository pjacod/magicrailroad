from code.algorithms import randomise
from code.classes import graph
from code.algorithms import hill_climber as hc


def main_loop(input1, input2, iterations):
    lst_k_values = []

    for solution in range(iterations):
        # create a scenario
        test_graph = graph.Graph(input1, input2)

        amount = randomise.amount_routes()

        # add a route to scenario
        test_graph.add_routes(amount)

        # use hill climber to choose itinerary for route
        hill_climber = hc.Hillclimber(test_graph)
        hill_climber.run()

        # calculate k_value of traject
        lst_k_values.append(test_graph.calculate_k())

    return lst_k_values, test_graph
