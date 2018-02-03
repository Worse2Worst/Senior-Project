import googlemaps
import json
gmaps=googlemaps.Client(key='AIzaSyASnqTekb7L3egtHgzCYe6O1CXLI7ZJoh8')

#Geocode
origin=gmaps.geocode('Stock Exchange of Thailand')
print (origin)

with open('data.txt', 'w') as outfile:
    json.dump(origin,outfile)


#reverse geocode
'''
origin=gmaps.reverse_geocode((13.740191,100.532459))
#origin=origin['Placemark'][0]['address']
destination = gmaps.reverse_geocode((13.785564,100.573680))
print (origin)
print('------------------------------------------')
print (destination)
d=gmaps.distance_matrix((13.785564,100.573680),(13.740191,100.532459))
print('------------------------------------------')
print (d)
'''
