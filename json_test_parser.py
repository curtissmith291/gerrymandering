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
    if area == 0 and perimeter == 0:
        pp_score = "error: area & perimeter = 0"
    else:
        pp_score = (4 * math.pi * area) / (perimeter ** 2)
    return pp_score

def info_gatherer(file):
    # Step 0: Open file
    with open(file) as test:
        data = json.loads(test.read())

    # Step 1: Get Number of Districts
    num_districts = len(data['features'])
    print(f'Number of Districts: {num_districts}')

    districts = list(range(num_districts))
    # print(districts)

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
        # print(f'Number of Polygons: {num_polygons}')
        # district count is place in the "districts" list; district is the actual district number
        # the district number can vary; some will be "0"
        info_list.append(
            {"district_count": i, 
            "district": district_num, 
            "polygon_count": num_polygons,
            "polygon_list":[]
            })
        # print(info_list)

        # Step 4: Iterate through polygons
        num_polygons = info_list[i]['polygon_count']
        for polygon in range(num_polygons):
            print(f'polygon: {polygon} of {num_polygons}')
            num_coordinates = len(data['features'][i]['geometry']['coordinates'][polygon])
            print(f'Number of Coordinates: {num_coordinates}')
            error = False
            error_message = ''
            if num_coordinates == 1:
                # print("path 1")
                coord_count = len(data['features'][i]['geometry']['coordinates'][polygon][0])
                print(f'Coordinat Count: {coord_count}')
                # Step 5: Calculate polygon area and perimeter
                # Get list of coordinates for each polygon
                coord_list = data['features'][i]['geometry']['coordinates'][polygon][0]
                print(coord_list)
                # if len(coord_list) < 3:
                #     # print(len(coord_list))
                #     # print(coord_list)
                #     error_removed = True
                #     break

                # Returns list of lats and list of longs
                lats = []
                longs = []
                for coord in coord_list:
                    longs.append(coord[0])
                    lats.append(coord[1])
                # print(lats)
                # print(longs)
                area, perimeter = area_perimeter(lats, longs)
                print(f'perimeter: {perimeter}')
                print(f'area: {area}')
                # Some jsons contain lists of the same values of corrdinates; causes "0" or "-0" for perimiter
                # 0 for perimiter will be flagged as erronious data
                if perimeter == 0 or perimeter == -0:
                    # "-0" breaks pp_test, convert to "0"
                    perimeter = abs(perimeter)
                    print(f'perimeter: {perimeter}')
                    error = True
                    message = "0 perimeter; repeating coordinates"
                # Calculate the Polsby-Popper Score
                pp_score = pp_test(area, perimeter)
                print(f'pp_score: {pp_score}')
                # Add info to list
                # Located in 'polygon_list':[{}, {}]
                if error == True:
                    error_message = message
                info_list[i]["polygon_list"].append({
                    "polygon_num": polygon,
                    "polygon_count": coord_count,
                    "polygon_area": area, 
                    "polygon_perimeter": perimeter,
                    "error": error_message,
                    "pp_score": pp_score, 
                })
                # print(info_list)

            elif num_coordinates != 1:
                # print("path 2")
                coord_count = len(data['features'][i]['geometry']['coordinates'][polygon])
                # print(f'Coord Count: {coord_count}')

                # Step 5: Calculate polygon area and perimeter
                # Get list of coordinates for each polygon
                sub_lists = data['features'][i]['geometry']['coordinates'][polygon]

                # This block removed and sublists that are less than 3 points, i.e. can't make a polygon
                # most likely errors in creation of the GeoJSON files
                error_removed = False
                for sub_list in range(len(sub_lists)):
                    coord_list = sub_lists[sub_list]
                    if len(coord_list) < 3:
                        # print(len(coord_list))
                        # print(coord_list)
                        error_removed = True
                        break
                    # Filters out sub-sub lists, can add in if necessary later. 
                    # for x in coord_list:
                    #     if len(x) > 1:
                    #         # print(len(x))
                    #         # print(len(x[0]))
                    #         # print(len(x[1]))
                    #         coord_list.remove(x)

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
                        "sub_polygon_count": coord_count,
                        "sub_polygon": sub_list,
                        "polygon_area": area, 
                        "polygon_perimeter": perimeter,
                        "pp_score": pp_score, 
                        "error_removed": error_removed,
                    })
                    
        # Add properties info
        properties = data['features'][i]['properties']
        # print(f'properties: {properties}')
        properties_list.append(properties)
        # print(f'properties list : {properties_list}')

    # print(f'info_list: {info_list}')
    # print(f'properties_list: {properties_list}')

    # Create export dictionary
    export_dict = {"geo_info":info_list, "properties":properties_list}
    print(f'Export dict {export_dict}')
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
# filename = 'South_Carolina_93_to_97.geojson'
filename = 'New_York_94_to_97.geojson'


file = os.path.join(path, filename)

try:
    data_dict = info_gatherer(file)

    # Append export dictionary to main dictionary
    main_dictionary["entries"].append(data_dict)
except:
    error_list.append(filename)

# print("running")
# for filename in os.listdir(path):
#     file = os.path.join(path, filename)

#     try:
#         data_dict = info_gatherer(file)

#         # Append export dictionary to main dictionary
#         main_dictionary["entries"].append(data_dict)
#     except:
#         error_list.append(filename)

# # Export data
# with open("gerrymandering_large_files/output.json", 'w') as out_file:
#     json.dump(main_dictionary, out_file, indent = 4)

print("Complete")
print(f'Errors: {error_list}')