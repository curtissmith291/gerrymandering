import json
import os
import math
from pyproj import Geod



# Defining functions

# area + perim function
def area_perimeter(lats, longs):
    geod = Geod('+a=6378137 +f=0.0033528106647475126')

    poly_area, poly_perimeter = geod.polygon_area_perimeter(longs, lats)
    poly_area, poly_perimeter = poly_area * 0.00000038610, poly_perimeter * 0.0006213712
    return abs(poly_area), poly_perimeter

def pp_test(area, perimeter):
    pp_score = (4 * math.pi * area) / (perimeter ** 2)
    return pp_score

def info_gatherer(file):
    # Step 0: Open file
    with open(file) as test:
        data = json.loads(test.read())

    # Step 1: Get Number of Districts
    num_districts = len(data['features'])
    # print(f'Number of Districts: {num_districts}')

    districts = list(range(num_districts))
    print(districts)

    # Step 2: initialize list of dictionaries to hold data
    # info_list holds polygon data
    info_list = []
    # hold properties about each district
    properties_list = []

    # Step 3: Get District Numbers and polygon count
    # Iterate through list of districts
    for i in districts:
        print(f'i: {i}')
        district_num = data['features'][i]['properties']['district']
        # appends district number to list of dictionaries
        num_polygons = len(data['features'][i]['geometry']['coordinates'])
        # district count is place in the "districts" list; district is the actual district number
        # the district number can vary; some will be "0"
        info_list.append(
            {"district_count": i, 
            "district": district_num, 
            "polygon_count": num_polygons,
            "polygon_list":[]
            })
        print(info_list)

        # Step 4: Iterate through polygons
        num_polygons = info_list[i]['polygon_count']
        for polygon in range(num_polygons):
            # print(f'polygon: {polygon}')
            num_coordinates = len(data['features'][i]['geometry']['coordinates'][polygon])
            # print(num_coordinates)
            if num_coordinates == 1:
                # print("Path 1")
                coord_count = len(data['features'][i]['geometry']['coordinates'][polygon][0])
                # print(coord_count)
                # Step 5: Calculate polygon area and perimeter
                # Get list of coordinates for each polygon
                coord_list = data['features'][i]['geometry']['coordinates'][polygon][0]

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
                # Located in 'polygon_list':[{}, {}]
                info_list[i]["polygon_list"].append({
                    "polygon_num": polygon,
                    "polygon_count": coord_count,
                    "polygon_area": area, 
                    "polygon_perimeter": perimeter,
                    "pp_score": pp_score, 
                })
            else: 
                # print("Path 2")
                coord_count = len(data['features'][i]['geometry']['coordinates'][polygon])
                # print(coord_count)
                # Step 5: Calculate polygon area and perimeter
                # Get list of coordinates for each polygon
                coord_list = data['features'][i]['geometry']['coordinates'][polygon]
                # print(coord_list)
                # Returns list of lats and list of longs
                lats = []
                longs = []
                for coord in coord_list:
                    longs.append(coord[0])
                    lats.append(coord[1])
                area, perimeter = area_perimeter(lats, longs)
                print(area, perimeter)

                # Calculate the Polsby-Popper Score
                pp_score = pp_test(area, perimeter)

                # Add info to list
                # Located in 'polygon_list':[{}, {}]
                info_list[i]["polygon_list"].append({
                    "polygon_num": polygon,
                    "polygon_count": coord_count,
                    "polygon_area": area, 
                    "polygon_perimeter": perimeter,
                    "pp_score": pp_score, 
                })

        # Add properties info
        properties = data['features'][i]['properties']
        print(properties)
        # print(f'properties: {properties}')
        properties_list.append(properties)

    print(f'info_list: {info_list}')
    print(f'properties_list: {properties_list}')

    # Create export dictionary
    export_dict = {"geo_info":info_list, "properties":properties_list}
    # export_dict["properties"] = data["features"][0]["properties"]
    # print(export_dict)
    return export_dict

# --------------------
# Program Starts Below
# --------------------

# initialize main_dictionary, where all calculated informtion for each district will be stored
main_dictionary =  {"entries": []}

# initializing list to hold errors
error_list = []
path = '/Users/curtissmith/Projects/gerrymandering_large_files/congressional-district-boundaries-master/'
# filename = 'Oklahoma_60_to_62.geojson'
# filename = 'Alabama_108_to_112.geojson'
filename = 'South_Carolina_93_to_97.geojson'


file = os.path.join(path, filename)

try:
    data_dict = info_gatherer(file)

    # Append export dictionary to main dictionary
    main_dictionary["entries"].append(data_dict)
except:
    error_list.append(filename)

print(main_dictionary)

# Export data
# with open("gerrymandering/output.json", 'w') as out_file:
#     json.dump(main_dictionary, out_file, indent = 4)

# print("Complete")
# print(f'Errors: {error_list}')