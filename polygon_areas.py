import json
import geojson

with open('/Users/curtissmith/Projects/gerrymandering_large_files/congressional-district-boundaries-master/Alabama_108_to_112.geojson') as test:
    data = json.loads(test.read())

coordinates = type(data['features'][0]['geometry']['coordinates'])
print(coordinates)


# x = type(data['features'][1]['properties'])
# y = data['features'][1]['properties']
# print(x)
# print(y)

# properties = data['features'][0]['properties']