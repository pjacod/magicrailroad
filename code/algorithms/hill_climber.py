'''
1 random state gegenereerd met code die lijkt op ons randomise algoritme. Hiervoor wordt met onze calculate k-value methode gecheckt wat de kwaliteit van de lijnvoering is.
2 voor deze state space wordt steeds iets in de verbindingen veranderd. Dit zal dan 1 station zijn binnen een traject van de lijnvoering.
3 Dan wordt er met onze calculate k-value methode gecheckt hoe dit invloed heeft op de kwaliteit.
4 Als dit positief is wordt de aanpassing doorgevoerd en wordt de state space geupdate met deze aanpassing, anders wordt de aanpassing ongedaan gemaakt
5 Dit wordt vervolgens steeds herhaald totdat er n-keer geen verbetering in zit
6 Als laatste wordt dit een bepaald aantal keer gerund en wordt de lijnvoering met de beste kwaliteit gekozen
'''

from code.algorithms import randomise
import copy

class Hillclimber():

    def __init__(self, graph):
        self.graph = copy.deepcopy(graph)
        self.route_dict = self.graph.route_dict
        #self.k_difference = ''

    def run(self, iterations):

        self.random_state(self.graph)

        for iteration in range(iterations):
            copy_graph = copy.deepcopy(self.graph)
            new_graph = self.random_change(copy_graph)
            self.choose_state(new_graph)


    def random_state(self, graph):
        randomise.random_routes(graph.route_dict)
        self.random_state = graph.route_dict

    '''
    mogelijk veranderen naar beste change
    '''
    def random_change(self, graph):
        '''
        graph.add_routes(1)
        graph.remove_route()
        







        return graph

        # pas random change toe aan random copy

    def show_options():
        return


    def choose_state(self, new_graph):
        quality_state = self.graph.calculate_K()
        quality_changed_state = new.graph.calculate_K()

        if quality_changed_state > quality_state:
            self.graph = new_graph
            #self.k_difference = quality_changed_state - quality_state


    def is_valid(self):
        return
