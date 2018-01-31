
def time_violated_index(tour,durations,nodes):
    cur_time = 0
    for i in range(len(tour) - 1):
        # print(len(nodes))
        # print (tour[i])
        cur_ET = nodes[tour[i]].ET
        cur_LT = nodes[tour[i]].LT
        next_ET = nodes[tour[i + 1]].ET
        next_LT = nodes[tour[i + 1]].LT
        time_arrived = cur_time + durations[tour[i]][tour[i + 1]]
        if (time_arrived > next_LT):  # VIOLATED!!!!!
            return i + 1
        cur_time = max(time_arrived, next_ET)
    return -1

def time_violated_nodes(tour,durations,couples,nodes):
    res = []
    index = []
    # if (len(tour) == 0):
    #     print ('BUGGGG!!!!!!!!!!!!!!!')
    #     return res
    cur_time = 0
    # print (tour)
    # print (cur_time)
    for i in range(len(tour) - 1):
        cur_pos = tour[i]
        next_pos = tour[i+1]

        cur_ET = nodes[cur_pos].ET
        cur_LT = nodes[cur_pos].LT
        next_ET = nodes[next_pos].ET
        next_LT = nodes[next_pos].LT
        cur_time = max(cur_time, cur_ET)
        time_arrived = cur_time + durations[cur_pos][next_pos]

        if (time_arrived > next_LT):  # VIOLATED!!!!!
            # debug ---------------------------------------
            print('################ Voilated!!! ####################')
            print(str(cur_pos) + '->' + str(next_pos))
            print('Arrived at '+str(time_arrived))
            print('ET='+str(next_ET)+',LT='+str(next_LT))

            v = tour.pop(i+1)
            print ('pop ' +str(v))
            print('#####################################################################')
            if (time_correction(v,tour,nodes,durations) >= 0):
                res.append(v)
                print('Append ' + str(v))
                i -= 1
            ######################
            next_ET = nodes[tour[i + 1]].ET
            next_LT = nodes[tour[i + 1]].LT
            time_arrived = cur_time + durations[tour[i]][tour[i + 1]]
            i += 1
            ##################

    for x in index :
        res.append(tour[x])
    for v in res:
        if (nodes[v].req_type =='p'):
            d_sib = nodes[v].d_sib
            print ('v ='+str(v))
            print('dsib ='+str(d_sib))
            print(tour)
            temp = tour.index(d_sib)
            index.append(temp)
            res.append(tour[temp])

        else :
            p_sib = nodes[v].p_sib
            temp = tour.index(p_sib)
            index.append(temp)
            res.append(tour[temp])
    for x in index:
        tour.pop(x)
    return res

def time_correction(v,tour,nodes,durations):
    cur_time = 0
    cur_ET = nodes[v].ET
    cur_LT = nodes[v].LT

    # case1 : pickup node
    if (nodes[v].req_type =='p'):
        d_sib = nodes[v].d_sib
        start = 0
        stop = tour.index(d_sib)

    # case 2: delivery node
    else:
        p_sib = nodes[v].p_sib
        start = tour.index(p_sib)
        stop = len(tour) - 1

    if (start > 0):
        cur_time = current_duration(tour,nodes,durations,start-1)

    # special case !! v should be first node
    if (cur_ET+durations[v][tour[0]] <=nodes[tour[0]].LT):
        return -1

    for i in range (start,stop):
        prev = tour[i]
        next = tour[i+1]
        prev_ET = nodes[prev].ET
        prev_LT = nodes[prev].LT
        next_ET = nodes[next].ET
        next_LT = nodes[next].LT
        cur_arrive = cur_time + durations[prev][v]
        if (cur_arrive > cur_LT):
            pass
        cur_arrive = max(cur_arrive,cur_ET)
        next_arrive = cur_arrive + durations[v][next]
        if (next_arrive <= next_LT):
            tour.insert(i,v)
            return -1
        cur_time += durations[prev][next]
        cur_time = max(cur_time,next_ET)
    # cannot insert
    return v

def current_duration(tour,nodes,durations,stop) :
    cur_time = nodes[tour[0]].ET
    for i in range(0,stop - 1):
        cur_time += durations[tour[i]][tour[i+1]]
        cur_time = max(cur_time,nodes[tour[i+1]].ET)
    return cur_time
