## Credits: https://github.com/sewerus/grismo/blob/5c19f30546c38b1714e50dd0cc49b97584820cc0/isomorfism_test.py#L27

import itertools
import numpy as np
import random
import timeit
import matplotlib.pyplot as plt
import bisect

def neighbour_list(matrix):
    result = []
    n = len(matrix)
    for i in range(n):
        result.append([])
    for i in range(n - 1):
        for j in range(i, n):
            if matrix[i][j]:
                result[i].append(j)
                result[j].append(i)
    return result

def wl_method(graph1, graph2, k_dim = 3):
        graph_1_neighbour_list = neighbour_list(graph1)
        graph_2_neighbour_list = neighbour_list(graph2)

        n=len(graph1)

        # vertices' colors
        graph_1_colors = [0] * n
        graph_2_colors = [0] * n

        # repeat method method_dim times
        for i in range(k_dim):
            # calc collections of neighbours' colors for each vertex
            graph_1_collection = []
            graph_2_collection = []
            for vertex in range(n):
                neighbours_colors = []
                for neighbour in graph_1_neighbour_list[vertex]:
                    bisect.insort(neighbours_colors, graph_1_colors[neighbour])
                graph_1_collection.append(neighbours_colors)
                neighbours_colors = []
                for neighbour in graph_2_neighbour_list[vertex]:
                    bisect.insort(neighbours_colors, graph_2_colors[neighbour])
                graph_2_collection.append(neighbours_colors)

            # prepare color - collection pairs
            pairs = []
            color_index = 0
            for vertex in range(n):
                collection = graph_1_collection[vertex]
                if not collection in [row[1] for row in pairs]:
                    pairs.append([color_index, collection])
                    color_index += 1

            # check if all collections from graph_2 are in prepared pairs
            for vertex in range(n):
                if not graph_2_collection[vertex] in [row[1] for row in pairs]:
                    return False

            # assign new colors
            for vertex in range(n):
                graph_1_colors[vertex] = pairs[[row[1] for row in pairs].index(graph_1_collection[vertex])][0]
                graph_2_colors[vertex] = pairs[[row[1] for row in pairs].index(graph_2_collection[vertex])][0]

        # on the end compare vertices' colors
        for vertex in range(n):
            if graph_1_colors[vertex] != graph_1_colors[vertex]:
                return False

        # not returned False before
        return True
 

