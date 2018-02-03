import googlemaps
import json
gmaps=googlemaps.Client(key='AIzaSyASnqTekb7L3egtHgzCYe6O1CXLI7ZJoh8')
d=gmaps.distance_matrix('Bangkok Life Assuarance Bangkok','Home Product Center Bangkok')
'''
with open('distance.txt', 'w') as outfile:
    json.dump(d,outfile)
'''
print (d)
