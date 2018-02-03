import googlemaps
import pandas as pd
import numpy as np
import json

gmaps=googlemaps.Client(key='AIzaSyASnqTekb7L3egtHgzCYe6O1CXLI7ZJoh8')
df = pd.read_csv('real_map/Places_LatLong.csv',header=None,names = ['place', 'lat', 'long', 'demand', 'ET','LT','service_time','p_sib','d_sib','json'])
df=df['place']
dist=np.zeros((51,51))
dur=np.zeros((51, 51))

for i in range(26,51):
    origin = df[i]+ ' Bangkok'
    #print('origin is : '+origin)
    for j in range(26,51):
        destination = df[j]+' Bangkok'
        if(i==j):
            dist[i][j]=0
            dur[i][j]=0
        else:
            #print('destination is : ' + destination)
            data=gmaps.distance_matrix(origin,destination)
            #print(data)
            try:
                r = data['rows']
                elements = r[0]['elements'][0]
                distance = elements['distance']['value']
                duration = elements['duration']['value']
                dist[i][j]=distance
                dur[i][j]=duration
            except:
                print(origin)
                print(destination)
dist = np.asarray(dist)
np.savetxt("dist.csv", dist, delimiter=",")

dur = np.asarray(dur)
np.savetxt("dur.csv", dist, delimiter=",")
