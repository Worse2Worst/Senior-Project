import time
from random import shuffle
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA
from GA_lib import operation
from GA_lib import evaluate

def routeToreqs(route,REQUESTS):
    reqs = set()
    for v in route:
        for i in range(len(REQUESTS)):
            if int(REQUESTS[i][0])== int(v) or int(REQUESTS[i][1])==int(v):
                reqs.add(i)
    reqs = list(reqs)
    return reqs


def print_solution(chromosome):
    num = 1
    for [_,_,tour]in chromosome:
        print('Route '+str(num)+': '+str(tour))
        num += 1


start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lc101.txt'
solution_path = 'pdp_instances/LiLim/solutions/pdp_100/lc101.txt'

numVehicles, LoadCapacities, speed, data = proc.load_file(filename)
LOCATIONS = data[0]
DEMANDS = data[1]
timeWindows = data[2]
serviceTimes = data[3]
pickupSiblings = data[4]
deliverySiblings = data[5]
requestType = data[6]
REQUESTS = proc.generate_request(pickupSiblings,deliverySiblings,requestType)
DISTANCES = proc.createDistanceTable(LOCATIONS)
DURATIONS = proc.createDurationTable(LOCATIONS, DISTANCES, serviceTimes, speed)


print(" processing time --- %s seconds ---" % (time.time() - start_time))


### Reading solutions
file = open(solution_path, 'rt')
line = file.readline()
best_chromosome = []
while line:
    if (line.find('Route')>=0):
        line = line.replace('Route ', '')
        num,route = line.split(':')
        num = int(num)
        route = route.split()
        route = [int(n) for n in route]
        reqs = routeToreqs(route,REQUESTS)
        best_chromosome.append([num,reqs,route])
    line = file.readline()
file.close()


print (best_chromosome)

dist = evaluate.chromosomeRoutesDistance(best_chromosome,DISTANCES)
print('Best known Solution Distance: '+str(dist))
bestNumVeh = len([[route] in [_,_,route] for [_,_,tour] in best_chromosome if (tour)])
print('Number of vehicles of the best known solution:'+str(bestNumVeh ))
print ('Best Known Solution waiting time :'+str(evaluate.chromosomeWatingTime(best_chromosome,DURATIONS,timeWindows)))





# chromosome = GA.initialize_WorstCase_Chromosome(REQUESTS)
MY_chromosome = [[15, [45, 44, 46, 47, 43], [90, 87, 86, 83, 82, 84, 85, 88, 89, 91]], [9, [38, 41, 40, 39, 42], [81, 78, 104, 76, 71, 70, 73, 77, 79, 80]], [6, [17, 18, 19, 16, 20], [32, 33, 31, 35, 37, 38, 39, 36, 105, 34]], [8, [33, 36, 32, 37, 34, 35], [67, 65, 63, 62, 74, 72, 61, 64, 102, 68, 66, 69]], [4, [12, 11, 10, 14, 15, 13], [20, 24, 25, 27, 29, 30, 28, 26, 23, 103, 22, 21]], [11, [7, 6, 9, 8], [13, 17, 18, 19, 15, 16, 14, 12]], [10, [31, 30, 28, 29], [57, 55, 54, 53, 56, 58, 60, 59]], [2, [51, 48, 50, 52, 49], [98, 96, 95, 94, 92, 93, 97, 106, 100, 99]], [3, [0, 1, 3, 4, 2, 5], [5, 3, 7, 8, 10, 11, 9, 6, 4, 2, 1, 75]], [14, [], []], [1, [24, 23, 27, 21, 22, 26, 25], [43, 42, 41, 40, 44, 46, 45, 48, 51, 101, 50, 52, 49, 47]]]
dist = evaluate.chromosomeRoutesDistance(MY_chromosome, DISTANCES)
print (MY_chromosome)
print('My distances is: '+str(dist))
myNumVeh = len([[route] in [_,_,route] for [_,_,tour] in MY_chromosome if (tour)])
print('Number of vehicles of MY solution:'+str(myNumVeh))
print ('Chromosome waiting time :'+str(evaluate.chromosomeWatingTime(MY_chromosome,DURATIONS,timeWindows)))

for [num,reqs,tour] in MY_chromosome:
    if(evaluate.precedence_violated(tour, requestType, pickupSiblings)):
        print('Precedence Violated!!')

for [num,reqs,tour] in MY_chromosome:
    if(evaluate.time_violated(tour, DURATIONS, timeWindows)):
        print('time Violated!!')

print('Have same nodes:' + str(evaluate.haveEqualNodes(best_chromosome, MY_chromosome, LOCATIONS)))


print_solution(MY_chromosome)