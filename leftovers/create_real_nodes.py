import googlemaps
import pandas as pd
import numpy as np
import json
gmaps=googlemaps.Client(key='AIzaSyASnqTekb7L3egtHgzCYe6O1CXLI7ZJoh8')
df = pd.read_csv('real_map/Places_LatLong.csv',header=None,names = ['place', 'lat', 'long', 'demand', 'ET','LT','service_time','p_sib','d_sib','json'])

for index, row in df.iterrows():
    print (row['place'], row['json'])

df.to_csv('res.csv',header=None,index=False)

'''
# data is the returned json

r=data['rows']
element=r[0]['element'][0]
dist=elements['distance']['value']
duration=elements['duration']['value']

'''