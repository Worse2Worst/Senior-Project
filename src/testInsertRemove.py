import time
from random import shuffle

import GA_lib.GA
from pdp_lib import processing as proc
from GA_lib import GA
from GA_lib import operation as op
from GA_lib import evaluate




start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lr202.txt'

maxSpot = 1000
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


print(" processing time --- %s seconds ---" % (time.time() - start_time))


# solving the problems !!!!
start_time = time.time()



start_time = time.time()
tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
reqs = [(tour[i],deliverySiblings[tour[i]]) for i in range(len(tour)) if requestType[tour[i]]=='pickup']
print('The Requests are :'+str(reqs))

allReqs = [(96, 23), (59, 91), (92, 24), (98, 84), (85, 15), (14, 44), (42, 54), (2, 43), (75, 58), (39, 99), (38, 18), (16, 5), (61, 80), (8, 55), (86, 6), (94, 95), (97, 4), (56, 25), (12, 26)]
tour = [59,92,98,85,91,14,42,75,39,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,56,4,54,55,25,24,80,12,26,58]
tourReqs = [(tour[i],deliverySiblings[tour[i]]) for i in range(len(tour)) if requestType[tour[i]]=='pickup']
tourReqsIndex = [REQUESTS.index(item) for item in tourReqs]
insertingReqs = [(96,23),(2,43)]
insertingReqsIndex  = [REQUESTS.index(item) for item in insertingReqs]

print('Tour Requests index : '+str(tourReqsIndex))

chromosome = [[10,tourReqsIndex,tour]]
################################ INSERTION!!!!!!!! #######################################################
GA_lib.GA.insert_requests_into_chromosome(chromosome, insertingReqsIndex, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot)

tour = chromosome[0][2]
cal_time = time.time() - start_time
print ('My Tour is : '+str(tour))
print (len(tour))

print('my Solution:' + str(evaluate.tour_distance(tour, DISTANCES)))
print('Violate time windows:' + str(evaluate.time_violated(tour, DURATIONS, timeWindows)))
print('Violate time precedence:'+str(evaluate.precedence_violated(tour,requestType, pickupSiblings)))


best_tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
print ('Best Tour is :'+str(best_tour))
print (len(best_tour))
print('best solution : ' + str(evaluate.tour_distance(best_tour, DISTANCES)))
print('Violate time windows:' + str(evaluate.time_violated(best_tour, DURATIONS, timeWindows)))
print('Violate time precedence:'+str(evaluate.precedence_violated(tour,requestType, pickupSiblings)))
print ('Have equal nodes:'+str(set(tour)==set(best_tour)))

print(" cal time --- %s seconds ---" % (cal_time))


############ Remove Requests !! ######################################
start_time = time.time()
chromosome = [[0,[],[]],[1,[],[]],[10,tourReqsIndex,tour]]
tabooVehicles = {0}
reqsToRemove = [47,0]
GA_lib.GA.remove_requests(chromosome, tabooVehicles, reqsToRemove, REQUESTS)
removedTour = chromosome[2][2]
print ('My Tour after remove is : '+str(removedTour))
print('Violate time windows:' + str(evaluate.time_violated(removedTour, DURATIONS, timeWindows)))
print('Violate time precedence:'+str(evaluate.precedence_violated(removedTour,requestType, pickupSiblings)))

cal_time = time.time() - start_time

print(" cal time --- %s seconds ---" % (cal_time))

