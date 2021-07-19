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


# initialize main_dictionary, where all calculated informtion for each district will be stored
main_dictionary =  {"entries": []}

file = '/Users/curtissmith/Projects/gerrymandering_large_files/congressional-district-boundaries-master/Alabama_108_to_112.geojson'

def info_gatherer(file):
    # Step 0: Open file
    with open(file) as test:
        data = json.loads(test.read())

    # Step 1: Get Number of Districts
    num_districts = len(data['features'])
    # print(f'Number of Districts: {num_districts}')

    districts = list(range(num_districts))

    # Step 2: initialize list of dictionaries to hold data
    info_list = []

    # Step 3: Get District Numbers and polygon count
    # Iterate through list of districts
    for i in districts:
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

        # Step 4: Iterate through polygons
        num_polygons = info_list[i]['polygon_count']
        for polygon in range(num_polygons):
            coord_count = len(data['features'][i]['geometry']['coordinates'][polygon][0])
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

    # print(info_list)

    # Create export dictionary
    export_dict = {"geo_info":info_list}
    export_dict["properties"] = data["features"][0]["properties"]
    # print(export_dict)
    return export_dict

export_dict = info_gatherer(file)

# Add Export dictionary to main dictionary
main_dictionary["entries"].append(export_dict)
print(main_dictionary)



