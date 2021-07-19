from pyproj import Geod
import math


def area_perimeter(lats, longs):
    geod = Geod('+a=6378137 +f=0.0033528106647475126')

    poly_area, poly_perimeter = geod.polygon_area_perimeter(longs, lats)
    poly_area, poly_perimeter = poly_area * 0.00000038610, poly_perimeter * 0.0006213712
    return abs(poly_area), poly_perimeter

lons = [-102.20253523916332, -101.59096157206567, -100.65438018473898, -101.90199046561818]
lats = [37.21550522238942, 37.70825886273666, 36.93243398218993, 36.394249155143996 ]

area, perimeter = area_perimeter(lats, lons)
print(area)
print(perimeter)

def pp_test(area, perimeter):
    pp_score = (4 * math.pi * area) / (perimeter ** 2)
    return pp_score

print(pp_test(area, perimeter))



# geod = Geod('+a=6378137 +f=0.0033528106647475126')

# lons = [-102.20253523916332, -101.59096157206567, -100.65438018473898, -101.90199046561818]
# lats = [37.21550522238942, 37.70825886273666, 36.93243398218993, 36.394249155143996 ]

# poly_area, poly_perimeter = geod.polygon_area_perimeter(lons, lats)

# print("area: {} , perimeter: {}".format(poly_area, poly_perimeter))