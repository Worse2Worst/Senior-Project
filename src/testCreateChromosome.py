import time
from random import shuffle
from pdp_lib import processing as proc
from GA_lib import GA
from GA_lib import operation as op
from GA_lib import evaluate
from GA_lib import modify






start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lc107.txt'

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


print(" processing time --- %s seconds ---" % (time.time() - start_time))


# solving the problems !!!!
start_time = time.time()


############################### INSERTION!!!!!!!! #######################################################

print ('Newly created chromosome below')
chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles)
print (chromosome)
cal_time = time.time() - start_time
print("Chromosome initializing time --- %s seconds ---" % (cal_time))