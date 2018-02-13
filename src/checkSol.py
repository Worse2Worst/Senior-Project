import time
from random import shuffle
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA
from GA_lib import operation
from GA_lib import evaluate
from GA_lib import modify

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
filename = 'pdp_instances/LiLim/pdp_100/lc107.txt'
solution_path = 'pdp_instances/LiLim/solutions/pdp_100/lc107.txt'

numVehicles, LoadCapacities, speed, data = proc.load_file(filename)
locations = data[0]
DEMANDS = data[1]
timeWindows = data[2]
serviceTimes = data[3]
pickupSiblings = data[4]
deliverySiblings = data[5]
requestType = data[6]
REQUESTS = proc.generate_request(pickupSiblings,deliverySiblings,requestType)
DISTANCES = proc.createDistanceTable(locations)
DURATIONS = proc.createDurationTable(locations, DISTANCES, serviceTimes, speed)

print(requestType[96])

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


unlimitedVehicles=300
chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,unlimitedVehicles, DEMANDS, LoadCapacities,maxSpot=2)
dist = evaluate.chromosomeRoutesDistance(chromosome,DISTANCES)
print('Unoptimized distances is: '+str(dist))
print ('Chromosome waiting time :'+str(evaluate.chromosomeWatingTime(chromosome,DURATIONS,timeWindows)))