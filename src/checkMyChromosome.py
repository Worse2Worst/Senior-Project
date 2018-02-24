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
filename = 'pdp_instances/LiLim/pdp_200/LR1_2_9.txt'
solution_path = 'pdp_instances/LiLim/solutions/pdp_200/LR1_2_9.txt'

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
MY_chromosome = [[1, [82, 66, 24, 87, 12, 95, 45, 55], [87, 112, 161, 48, 92, 139, 121, 146, 185, 169, 181, 53, 192, 111, 24, 206]], [18, [77, 58, 31, 20, 13, 89, 33], [155, 63, 44, 3, 5, 117, 68, 208, 25, 116, 11, 79, 172, 197]], [16, [101, 35, 94, 5, 71, 100, 98, 96], [188, 15, 184, 153, 71, 193, 151, 175, 56, 129, 144, 186, 201, 179, 190, 107]], [22, [47, 25, 2, 21, 91], [4, 46, 54, 125, 89, 29, 96, 65, 174, 108]], [8, [0, 97, 88, 14, 60, 83], [1, 51, 26, 123, 187, 162, 171, 170, 78, 148, 119, 203]], [6, [62, 78, 92, 26, 9], [132, 55, 67, 14, 176, 207, 21, 126, 156, 154]], [4, [1, 4, 72, 57, 38, 104], [145, 2, 115, 16, 8, 122, 76, 17, 40, 200, 210, 42]], [10, [43, 53, 11, 42, 28, 10], [106, 85, 94, 12, 23, 58, 127, 22, 47, 82, 74, 97]], [7, [], []], [13, [68, 90, 67, 7, 93, 27], [140, 57, 173, 95, 178, 19, 114, 39, 37, 164, 141, 70]], [19, [40, 63, 32, 75, 19], [41, 150, 137, 36, 80, 64, 133, 195, 182, 9]], [9, [64, 70, 34, 86, 56], [168, 143, 113, 165, 69, 31, 134, 124, 103, 101]], [5, [37, 99, 18, 52, 51, 39], [73, 38, 104, 100, 136, 6, 189, 202, 177, 102, 77, 198]], [2, [49, 8, 84, 102, 69, 103, 15], [196, 13, 20, 30, 34, 98, 163, 62, 194, 142, 159, 10, 83, 45]], [11, [36, 73, 65, 16, 85, 79], [157, 72, 147, 199, 93, 135, 166, 33, 167, 191, 43, 110]], [12, [3, 54], [7, 109, 28, 91]], [14, [23, 22, 80, 30, 6, 81, 44, 61], [18, 120, 158, 50, 86, 209, 131, 66, 130, 160, 180, 49, 61, 205, 27, 75]], [3, [17, 41, 48, 76, 59, 29, 50, 74, 46], [149, 81, 35, 60, 152, 99, 32, 138, 84, 90, 118, 88, 204, 183, 128, 52, 59, 105]]]
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