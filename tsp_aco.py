import random
import time as tm

class Graph(object):
    def __init__(self, costmatrix: list, level: int):

        self.matrix = costmatrix
        self.level = level

        self.pheromone = [[1 / (level * level) for j in range(level)] for i in range(level)]

class ACO(object):

    def __init__(self, antcount: int, generations: int, alpha: float, beta: float, rho: float, q: int):

        self.antcount = antcount
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = q


    def _updatepheromone(self, graph: Graph, ants: list):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho
                for ant in ants:
                    graph.pheromone[i][j] += ant.delta_pheromone[i][j]


    def solve(self, graph: Graph):
        start = tm.time()
        bestcost = float('inf')
        bestsolution = []
        for gen in range(self.generations):

            ants = [_Ant(self, graph) for i in range(self.antcount)]
            for ant in ants:
                for i in range(graph.level - 1):
                    ant._selectnext()
                ant.totalcost += graph.matrix[ant.tab[-1]][ant.tab[0]]
                if ant.totalcost < bestcost:
                    bestcost = ant.totalcost
                    bestsolution = [] + ant.tab

                ant._updatedelta_pheromone()
            self._updatepheromone(graph, ants)

        runtime=tm.time()-start
        return runtime, bestsolution, bestcost


class _Ant(object):
    def __init__(self, aco: ACO, graph: Graph):
        self.colony = aco
        self.graph = graph
        self.totalcost = 0.0
        self.tab = [] # Taboo is the amount of pheromone remained in the path passed by the ants in another iteration.
        self.delta_pheromone = []
        self.allowed = [i for i in range(graph.level)]
        self.eta = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.level)] for i in
                    range(graph.level)]
        start = random.randint(0, graph.level - 1)
        self.tab.append(start)
        self.current = start
        self.allowed.remove(start)

    def _selectnext(self):
        denominator = 0
        for i in self.allowed:
            denominator += self.graph.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][
                                                                                            i] ** self.colony.beta

        probabilities = [0 for i in range(self.graph.level)]
        for i in range(self.graph.level):
            try:
                self.allowed.index(i)
                probabilities[i] = self.graph.pheromone[self.current][i] ** self.colony.alpha * \
                    self.eta[self.current][i] ** self.colony.beta / denominator
            except ValueError:
                pass
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        self.allowed.remove(selected)
        self.tab.append(selected)
        self.totalcost += self.graph.matrix[self.current][selected]
        self.current = selected

    def _updatedelta_pheromone(self):
        self.delta_pheromone = [[0 for j in range(self.graph.level)] for i in range(self.graph.level)]
        for _ in range(1, len(self.tab)):
            i = self.tab[_ - 1]
            j = self.tab[_]
            self.delta_pheromone[i][j] = self.colony.Q / self.totalcost
