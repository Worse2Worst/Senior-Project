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




start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lrc201.txt'
solution_path = 'pdp_instances/LiLim/solutions/pdp_100/lrc201.txt'

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
chromosome = []
while line:
    if (line.find('Route')>=0):
        line = line.replace('Route ', '')
        num,route = line.split(':')
        num = int(num)
        route = route.split()
        route = [int(n) for n in route]
        reqs = routeToreqs(route,REQUESTS)
        chromosome.append([num,reqs,route])
    line = file.readline()
file.close()


print (chromosome)

dist = evaluate.chromosomeRoutesDistance(chromosome,DISTANCES)
print('Best Solution Distance: '+str(dist))
print ('Chromosome waiting time :'+str(evaluate.chromosomeWatingTime(chromosome,DURATIONS,timeWindows)))

best_chromosome = chromosome
# chromosome = GA.initialize_WorstCase_Chromosome(REQUESTS)
chromosome = [[4, [31, 22, 2, 26, 18, 0, 24, 39, 23, 40, 46, 21, 20], [42, 39, 36, 72, 5, 45, 2, 88, 98, 61, 44, 40, 38, 41, 81, 94, 50, 34, 32, 26, 89, 48, 24, 25, 77, 58]], [3, [44, 9, 29, 45, 14, 48, 50, 13, 32, 15, 16, 17, 47, 37], [92, 95, 63, 33, 28, 27, 29, 31, 30, 62, 67, 71, 90, 53, 99, 57, 86, 87, 9, 10, 74, 97, 13, 17, 60, 100, 70, 102]], [1, [38, 4, 1, 30, 5, 3, 25, 34, 8, 6, 7], [65, 14, 47, 59, 75, 16, 15, 11, 12, 78, 73, 79, 7, 6, 8, 46, 3, 101, 1, 4, 55, 68]], [0, [35, 27, 10, 49, 41, 36, 43, 12, 28, 33, 11, 42, 19], [69, 82, 52, 83, 64, 19, 23, 21, 18, 76, 85, 84, 51, 49, 22, 20, 66, 56, 96, 54, 43, 35, 37, 93, 91, 80]]]
dist = evaluate.chromosomeRoutesDistance(chromosome,DISTANCES)
print (chromosome)
print('My distances is: '+str(dist))
print ('Chromosome waiting time :'+str(evaluate.chromosomeWatingTime(chromosome,DURATIONS,timeWindows)))

for [num,reqs,tour] in chromosome:
    if(evaluate.precedence_violated(tour, requestType, pickupSiblings)):
        print('Precedence Violated!!')

for [num,reqs,tour] in chromosome:
    if(evaluate.time_violated(tour, DURATIONS, timeWindows)):
        print('time Violated!!')

print('Have same nodes:'+str(evaluate.haveEqualNodes(best_chromosome,chromosome,LOCATIONS)))