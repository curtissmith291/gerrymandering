import json
import geojson

with open('/Users/curtissmith/Projects/gerrymandering_large_files/congressional-district-boundaries-master/Alabama_108_to_112.geojson') as test:
    data = json.loads(test.read())

# coordinates = data['features'][0]['geometry']['coordinates'][0][0]
# print(len(coordinates))
# # print(coordinates)

# properties = data['features'][0]['properties']['district']
# print(properties)

# Step 1: Get Number of Districts
num_districts = len(data['features'])
print(num_districts)
districts = list(range(num_districts))
print(districts)

# Step 2: initialize list of dictionaries to hold data
info_list = []

# Step 3: Get District Numbers and polygon count
for i in districts:
    district_num = data['features'][i]['properties']['district']
    # appends district number to list of dictionaries
    num_polygons = len(data['features'][i]['geometry']['coordinates'])
    info_list.append({"district":district_num, "polygon_count": num_polygons})

print(info_list)

# Step 4: get number of coordinates for each polygon; could be intermediate step, might delete later