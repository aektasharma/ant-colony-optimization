import math
from aco import ACO, Graph
from plot import plot


def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)

def main():
    cities = []
    points = []
    with open('./data/Loc48.txt') as f:
        for line in f.readlines():
            city = line.split(' ')
            cities.append(dict(index=int(city[0]), x=float(city[1]), y=float(city[2])))
            points.append((float(city[1]), float(city[2])))
    costmatrix = []
    level = len(cities)

    for i in range(level):
        row = []
        for j in range(level):
            row.append(distance(cities[i], cities[j]))

        costmatrix.append(row)

    aco = ACO(10, 100, 1.0, 10.0, 0.5, 10)
    graph = Graph(costmatrix, level)
    time ,path, cost = aco.solve(graph)
    print('cost: {}, path: {}'.format(cost, path))
    print('Time taken: ', time, 'sec')
    plot(points, path)

if __name__ == '__main__':
    main()
