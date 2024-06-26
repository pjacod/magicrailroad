import pandas as pd
import argparse
import csv
import os
from code.classes import graph
from code.algorithms import hill_climber as hc
from code.visualize import visualize as vis

def generate_experiment_name(Progression_bool_status, changes_iterations = ''):
    """
    Generates a filename for an experiment
    """
    return 'result_' + Progression_bool_status + '_' + changes_iterations + '.csv'


def export_result_to_csv(experiment_path, exp_kwargs, results):
    """
    Exports the results of an experiment as experiment parameters to a file
    in the location described by `experiment_path`.
    """
    exp_params = tuple(exp_kwargs.keys())
    exp_param_values = tuple(exp_kwargs.values())

    os.makedirs(os.path.dirname(experiment_path), exist_ok=True)

    with open(experiment_path, 'w') as output_file:
        csv_writer = csv.writer(output_file)

        # write header
        csv_writer.writerow(exp_params + ('k_value', 'best_k_value'))

        # repeat experiment parameters and add the outcome for each experiment
        for k_value, best_k_value in results:
            csv_writer.writerow(exp_param_values + (k_value, best_k_value))

def generate_combinations():
    # Define the possible numbers between 5 and 1.5 ending in .0 or .5
    possible_numbers = [5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5]

    lst_combinations = []

    for number_1 in possible_numbers:
        for number_2 in possible_numbers:
            for number_3 in possible_numbers:
                lst_combinations.append([number_1, number_2, number_3])

    return lst_combinations


def loop_hill_climber(input1, input2, iterations):
    '''
    loops through the hill climber algorithm with different parameters.
    These parameters consist of if the hill climber uses progression for applied changes to the graph
    and how much each changes function alters a route
    '''

    lst_progression_bool = [False, True]
    lst_divisions = generate_combinations()

    # dictionary for arguments
    experiment_kwargs = {
    'Progression_bool': False,
    'divisions': [3, 2, 1.5]
    }

    # empty list of k_values per set of parameters
    lst_k_values = []

    # loop through experiments with and without progression enabled
    for progression in lst_progression_bool:
        experiment_kwargs['Progression_bool'] = progression

        # loop through experiments with different division arguments for change functions
        for division in lst_divisions:
            experiment_kwargs['divisions'] = division

            # create a graph and add routes
            test_climber = graph.Graph(input1, input2)
            amount = test_climber.amount_routes()
            test_climber.add_routes(amount)

            # create hill_climber and initiate k_value of one run
            hill_climber = hc.Hillclimber(test_climber, experiment_kwargs['Progression_bool'], experiment_kwargs['divisions'])

            best_k_value = 0

            # run algorithm 10 times and take for specific parameters the best k_value
            for climbers in range(10):
                new_k_value, test_climber = hill_climber.run(10)

                if new_k_value >= best_k_value:
                    best_k_value = new_k_value


                # save results of all k_values and best_k_values in a list
                results = []
                results.append((new_k_value, best_k_value))

                # export the results to a csv file
                exp_name = generate_experiment_name('Progression_disabled')
                export_result_to_csv(f'data/data_hill_climber/{exp_name}', experiment_kwargs, results)

            # save graph of parameters with the best results
            lst_k_values.append(best_k_value)
            if best_k_value >= max(lst_k_values):
                best_graph = test_climber

            # print iteration every division
            print('run_completed')


    return best_graph, lst_k_values


def main(input1, input2, iterations):
    best_graph, lst_k_values = loop_hill_climber(input1, input2, iterations)

    vis.bar_k(lst_k_values)
    vis.histogram_k(lst_k_values)
    vis.plot_connections(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')
    vis.plot_routes(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', best_graph.route_dict)
    best_graph.show_routes()

if __name__ == "__main__":

    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "read both input file names")

    parser.add_argument("input1", help = "input file 1 (csv)")
    parser.add_argument("input2", help = "input file 2 (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    main(args.input1, args.input2, 1)
