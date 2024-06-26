import pandas as pd
import argparse
from code.classes import graph
from code.algorithms import hill_climber as hc
from code.visualize import visualize as vis

def experiment_name(Progression_bool_status, changes_iterations = ''):
    """
    Generates a filename for an experiment
    """
    return print('result_' + Progression_bool_status + '_' + changes_iterations + '.csv')


def export_result_to_csv(experiment_path, exp_kwargs, results):
    """
    Exports the results of an experiment as experiment parameters to a file
    in the location described by `experiment_path`.
    """
    exp_params = tuple(exp_kwargs.keys())
    exp_param_values = tuple(exp_kwargs.values())

    with open(experiment_path, 'w') as output_file:
        csv_writer = csv.writer(output_file)

        # write header
        csv_writer.writerow(exp_params + ('Rabbits', 'Foxes'))

        # repeat experiment parameters and add the outcome for each experiment
        for (rabbits, foxes) in results:
            csv_writer.writerow(exp_param_values + (rabbits, foxes))

def loop_hill_climber(input1, input2, iterations):
    '''
    loops through the hill climber algorithm with different parameters.
    THese paramters consists of if the hill climber uses progression for applied changes to the graph
    and the amount of iterations each changes function runs
    '''

    lst_k_values = []

    for solution in range(iterations):
        # create a scenario
        test_climber = graph.Graph(input1, input2)
        amount = test_climber.amount_routes()

        # add a route to scenario
        test_climber.add_routes(amount)

        experiment_kwargs = {
        'Progression_bool' : [False, True],
        'changes_iterations' : [ [0.2, 0.2, 0.2, 0.2, 0.2], [0.6, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.6, 0.1, 0.1, 0.1], [0.1, 0.1, 0.6, 0.1, 0.1], [0.1, 0.1, 0.1, 0.6, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.6] ]
        }

        for bool in experiment_kwargs['Progression_bool']:
            if bool == False:
                # use hill climber to choose itinerary for route
                hill_climber = hc.Hillclimber(test_climber, bool)
                k_value = hill_climber.run(10)

                lst_k_values.append(k_value)
                if k_value >= max(lst_k_values):
                    best_graph = test_climber

                # export the data to a csv file
                experiment_name = experiment_name('Progression_disabled')
                export_result_to_csv(f'data/{experiment_name}', bool, results)

            else:
                for iterations in experiment_kwargs['changes_iterations']:
                    # use hill climber to choose itinerary for route
                    hill_climber = hc.Hillclimber(test_climber, bool, iterations)
                    k_value = hill_climber.run(10)

                    lst_k_values.append(k_value)
                    if k_value >= max(lst_k_values):
                        best_graph = test_climber


                    # export the data to a csv file
                    experiment_name = experiment_name('Progression_enabled', str(iterations))
                    export_result_to_csv(f'data/{experiment_name}', (bool, iterations), results)

        # calculate k_value of traject
        lst_k_values.append(test_climber.calculate_k())

        if solution % 20 == 0:
            print(solution)

    return k_values, climber_graph



def main(input1, input2, iterations):
    best_graph, lst_k_values = loop_hill_climber(input1, input2, iterations)

    vis.bar_k(lst_k_values)
    vis.histogram_k(lst_k_values)
    vis.plot_connections(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')
    vis.plot_routes(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', best_graph.route_dict)
    best_graph.show_routes()

if __name__ == "__main__":

        # Set-up parsing command line arguments
        parser = argparse.ArgumentParser(description = "read both input file name and writes to output file")

        parser.add_argument("input1", help = "input file 1 (csv)")
        parser.add_argument("input2", help = "input file 2 (csv)")


        # Read arguments from command line
        args = parser.parse_args()

        main(args.input1, args.input2, 1)
