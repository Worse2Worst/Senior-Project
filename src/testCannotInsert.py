import time
from random import shuffle
from pdp_lib import processing as proc
from GA_lib import GA
from GA_lib import operation as op
from GA_lib import evaluate
from GA_lib import modify




maxSpot=1000

start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/Worse2Worst/trivial01.txt'

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



start_time = time.time()

allReqs = [req for req in REQUESTS]
insertingReqs = [(3,1),(6,4),(5,2)]
insertingReqsIndex  = [REQUESTS.index(item) for item in insertingReqs]


chromosome = [[0,[],[]],[1,[],[]]]
################################ INSERTION!!!!!!!! #######################################################
modify.insert_requests_into_chromosome(chromosome, insertingReqsIndex , DISTANCES, DURATIONS, timeWindows, REQUESTS,maxSpot)

print (chromosome)
cal_time = time.time() - start_time

print ('Newly created chromosome below')
chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles)
print (chromosome)