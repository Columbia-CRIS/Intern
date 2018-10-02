from generator import generate
from evaluator import evaluate
from mutator import mutate

# for Ubuntu
import matplotlib
matplotlib.use('Agg')

import networkx as nx
import numpy as np
import matplotlib.pyplot as savefig
import matplotlib.pyplot as plt
from functools import reduce
from multiprocessing import Pool

alpha = 0

def saveGraph(adj, gen):
    """ Draws and Saves Graph Image to img/ """
    gr = nx.from_numpy_matrix(np.matrix(adj))
    nx.draw(gr)
    plt.savefig('img/' + str(gen) + '.png') # saves generated image in img/
    plt.close()

def runFitness(graph):
    """ Evaluates the Fitness of Graph given Graph and Alpha value """
    fitness = []
    score = evaluate(graph, alpha)
    return score

# Takes input args, generates a seed pool and then runs the GA
# Input: Args object
# Output: The best graph
def iterate(args):
    """ Given input arguments, generates a seed pool and runs the genetic algorithm, 
    outputting the best graph """
    global alpha # sets alpha value as a global value

    fitness = []
    gens = 1
    globalgensWithoutChange = 0
    gensWithoutChange = 0
    maxScore = 0
    alpha = args.a
    best = None
    annealing = False

    # generates graph through generator.py
    pool = generate(args.n, args.e, args.p, args.c, args.w, args.d) # array of graphs
    print("Generated")

    ## call evaluator and add fitness score of each graph to graph element
    for seed in pool:
        fitness.append(evaluate(seed, args.a)) 

    ## sets max gens without change to either 50 generators or one-fourth of input
    annealingGen = max(len(pool) * 50, len(pool) * args.s / 4)

    # Autostopping mechanism
    while globalgensWithoutChange <= len(pool) * args.s:
        if gensWithoutChange >= annealingGen:
            print("Setting annealing")
            annealing = True

        pool = mutate(pool, fitness, gensWithoutChange, args.c, args.d, annealing) # Set pool with next generation
        fitness = [] # Reset fitness

        # Now populate fitness array
        with Pool(4) as p:
            fitness = p.map(runFitness, pool)

        if gensWithoutChange > annealingGen + (10 * len(pool)):
            print("Stopping annealing")
            annealing = False
            gensWithoutChange = 0

        graphTmp = None
        bestTmp = 0
        for i in range(len(fitness)):
            if fitness[i] > bestTmp:
                bestTmp = fitness[i]
                graphTmp = pool[i]

            if fitness[i] > maxScore:
                maxScore = fitness[i]
                best = pool[i]
                globalgensWithoutChange = 0 # Reset autostop counter
                gensWithoutChange = 0 # Reset annealing counter
                print("====Global best", maxScore)
            else:
                gensWithoutChange += 1
                globalgensWithoutChange += 1

        saveGraph(graphTmp.adj, gens)

        print("Gen", gens,
              "Best", bestTmp,
              "Avg", reduce(lambda x, y: x + y, fitness) / len(fitness))
        gens += 1
    return best
