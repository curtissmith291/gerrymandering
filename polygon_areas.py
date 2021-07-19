import json
import math
from logging import info
import pyproj    
from pyproj import Geod
import shapely
import shapely.ops as ops
from shapely.geometry.polygon import Polygon
from functools import partial
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Defining functions

def area_calculator(list_of_coords):
    '''
    Calculates the area from an input list of coordinate tuples
    '''
    geom = Polygon(list_of_coords)
    geom_area = ops.transform(
        partial(
            pyproj.transform,
            pyproj.Proj(init='EPSG:4326'),
            pyproj.Proj(
                proj='aea',
                lat_1=geom.bounds[1],
                lat_2=geom.bounds[3]
            )
        ),
        geom)
    area_m2 = geom_area.area
    area_mi2 = area_m2 * 0.00000038610
    return area_mi2

# area + perim function
def area_perimeter(lats, longs):
    geod = Geod('+a=6378137 +f=0.0033528106647475126')

    poly_area, poly_perimeter = geod.polygon_area_perimeter(longs, lats)
    poly_area, poly_perimeter = poly_area * 0.00000038610, poly_perimeter * 0.0006213712
    return abs(poly_area), poly_perimeter

def pp_test(area, perimeter):
    pp_score = (4 * math.pi * area) / (perimeter ** 2)
    return pp_score


with open('/Users/curtissmith/Projects/gerrymandering_large_files/congressional-district-boundaries-master/Alabama_108_to_112.geojson') as test:
    data = json.loads(test.read())

# coordinates = data['features'][0]['geometry']['coordinates'][0][0]
# print(len(coordinates))
# # print(coordinates)

# properties = data['features'][0]['properties']['district']
# print(properties)

# Step 1: Get Number of Districts
num_districts = len(data['features'])
print(f'Number of Districts: {num_districts}')

districts = list(range(num_districts))

# Step 2: initialize list of dictionaries to hold data
info_list = []

# Step 3: Get District Numbers and polygon count
for i in districts:
    district_num = data['features'][i]['properties']['district']
    # appends district number to list of dictionaries
    num_polygons = len(data['features'][i]['geometry']['coordinates'])
    # district count is place in the "districts" list; district is the actual district number
    # the district number can vary; some will be "0"
    info_list.append({"district_count": i, "district":district_num, "polygon_count": num_polygons})

# print(info_list)

# Step 4: get number of coordinates for each polygon; could be intermediate step, might delete later
for i in districts:
    # print(i)
    num_polygons = info_list[i]['polygon_count']
    for x in range(num_polygons):
        coord_count = len(data['features'][i]['geometry']['coordinates'][x][0])
        key_string = f'polygon{x+1}_count'
        info_list[i][key_string] = coord_count
        # Step 5: Calculate polygon area
        # Get list of coordinates for each polygon
        coord_list = data['features'][i]['geometry']['coordinates'][x][0]

        # Returns list of lats and list of longs
        lats = []
        longs = []
        for coord in coord_list:
            longs.append(coord[0])
            lats.append(coord[1])
        area, perimeter = area_perimeter(lats, longs)

        # Calculate the Polsby-Popper Score
        pp_score = pp_test(area, perimeter)

        # Add info to list
        key_string = f'polygon{x+1}_area'
        info_list[i][key_string] = area
        key_string = f'polygon{x+1}_perimeter'
        info_list[i][key_string] = perimeter
        key_string = f'polygon{x+1}_pp_score'
        info_list[i][key_string] = pp_score


# Step 6: Calculate Perimeter

# print(info_list)

# Step X: Create export dictionary
export_dict = {"geo_info":info_list}
export_dict["properties"] = data['features'][0]['properties']
print(export_dict)


