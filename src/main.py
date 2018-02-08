import time
from random import shuffle
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA
from GA_lib import operation as op
from GA_lib import evaluate
from GA_lib import modify






start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lr202.txt'

numVehicles, loadCapacities, speed, data = proc.load_file(filename)
locations = data[0]
demands = data[1]
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


# solving the problems !!!!
start_time = time.time()






start_time = time.time()
tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
reqs = [(tour[i],deliverySiblings[tour[i]]) for i in range(len(tour)) if requestType[tour[i]]=='pickup']
print('The Requests are :'+str(reqs))
tour = []
shuffle(reqs)
for r in reqs:
    tour = evaluate.new_tour_after_insert_requests(r, tour, DISTANCES, DURATIONS, timeWindows)
cal_time = time.time() - start_time


print (tour)
print('My Solution is :' + str(tour))
print('my Solution:' + str(evaluate.tour_distance(tour, DISTANCES)))
print('Violate time windows:' + str(evaluate.time_violated(tour, DURATIONS, timeWindows)))
print('Violate time precedence:'+str(evaluate.precedence_violated(tour,requestType, pickupSiblings)))

best_tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
print (best_tour)

print('best solution : ' + str(evaluate.tour_distance(best_tour, DISTANCES)))
print('Violate time windows:' + str(evaluate.time_violated(best_tour, DURATIONS, timeWindows)))
print('Violate time precedence:'+str(evaluate.precedence_violated(tour,requestType, pickupSiblings)))
print(" cal time --- %s seconds ---" % (cal_time))
print ('Have equal nodes:'+str(set(tour)==set(best_tour)))

