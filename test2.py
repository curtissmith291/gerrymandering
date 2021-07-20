import json
import os

path = '/Users/curtissmith/Projects/gerrymandering_large_files/congressional-district-boundaries-master/'
# filename = 'Oklahoma_60_to_62.geojson'
# filename = 'Alabama_108_to_112.geojson'
filename = 'South_Carolina_93_to_97.geojson'


file = os.path.join(path, filename)

with open(file) as test:
    data = json.loads(test.read())

num_districts = len(data['features'])
districts = list(range(num_districts))

for i in districts:
    district_num = data['features'][i]['properties']['district']
    # print(district_num)

    num_polygons = len(data['features'][i]['geometry']['coordinates'])
    # print(num_polygons)

# branch_1 = len(data['features'][0]['geometry']['coordinates'][0])   #coord_count
# branch_2 = len(data['features'][0]['geometry']['coordinates'][0][0])
# print(branch_1)
# print(branch_2)

# Number of Districts
num_disticts = len(data['features'])
print(f'Number of Districts: {num_districts}')

district = 0

# Keys for the "features" dictionary
# should be "geometry", "type", "properties"
feature_keys = data['features'][district].keys()
# print(f'Feature keys: {feature_keys}')

# Keys for the "geometry" dictionary
# should be "type", "coordinates"
geometry_keys = data['features'][district]['geometry'].keys()
print(f'Geometry keys: {geometry_keys}')

num_polygons = len(data['features'][district]['geometry']['coordinates'])
print(f'Number of Polygons: {num_polygons}')
# print(data['features'][0]['geometry']['coordinates'])

extra_list = len(data['features'][district]['geometry']['coordinates'][0])
print(f'Extra List Index: {extra_list}')
# print(data['features'][district]['geometry']['coordinates'][0])

sub_polys_count = len(data['features'][district]['geometry']['coordinates'][0][0])
print(f'Number of Sub Polys: {sub_polys_count}')

# print(data['features'][district]['geometry']['coordinates'][0][0])


# print(len(data['features'][district]['geometry']['coordinates'][0][0][0]))

# print(len(data['features'][district]['geometry']['coordinates'][1]))

# print(len(data['features'][district]['geometry']['coordinates'][0][0]))
# print(data['features'][district]['geometry']['coordinates'][0][0])


