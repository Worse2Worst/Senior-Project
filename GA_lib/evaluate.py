from pdp_lib import preprocessing
from pdp_lib import processing
from GA_lib import oper as op
import numpy as np

# eval distance of all p_jobs
def eval_distance (p_tours, distances, depot, nodes):
    res = []
    for tours in p_tours:
        res.append(tours_distance(tours,distances,depot,nodes))
    return res

# distance of 'tours' by all vehicles
def tours_distance(tours, distances, depot,nodes):
    dist = 0
    for tour in tours:
        dist += tour_distance(tour,distances,depot,nodes)
    return dist

# distance of just one 'job' by one vehicle
def tour_distance(tour,distances,depot,nodes):
    dist = 0
    for i in range(len(tour)-1):
        dist += distances[tour[i]][tour[i+1]]
    dist += processing.distance(nodes[tour[0]],depot)+processing.distance(nodes[tour[-1]],depot)
    return dist

def evaluate_fitness(p_tours,distances, depot, nodes):
    fitness = [1.0/x for x in eval_distance (p_tours, distances, depot, nodes)]
    return fitness

def select_best_populations(p_tours,distances, depot, nodes, N=5):
    fit = evaluate_fitness(p_tours,distances, depot, nodes)
    best = [x for _, x in sorted(zip( fit,p_tours),reverse=True)]
    return best[0:N]

