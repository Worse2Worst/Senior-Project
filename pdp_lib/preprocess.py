class Node:
    def __init__(self, index, x, y, demand, ET, LT, ServiceTime, pickup_siblings, delivery_sibling):
        self.index = index
        self.x = int(x)
        self.y = int(y)
        self.demand = int(demand)
        self.ET = int(ET)
        self.LT = int(LT)
        self.service_time = int(0)
        self.p_sib = int(pickup_siblings)
        self.d_sib = int(delivery_sibling)
        self.req_type = 'p' if (int(demand)>0) else 'd'

def read_node(filename):
    file = open(filename, 'rt')
    line = file.readline()
    num_vehicles, load_capacities, speed = line.split() # not used

    nodes = []  # List of nodes
    req = []  # List of requests

    ######  Reading Depot (Not Used in our project) ################
    line = file.readline()  #  This is the DEPOT!! (not used in our project)
    temp=Node(*(line.split()))
    nodes.append(temp)

    ######  Reading the first node ################
    line = file.readline()

    ######  Reading the remaining nodes ################
    while line:
        temp = Node(*(line.split()))
        nodes.append(temp)
        line = file.readline()

    file.close()
    return nodes

