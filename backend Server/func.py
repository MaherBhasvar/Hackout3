from math import cos, asin, sqrt


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((float(lat2) - float(lat1)) * p)/2 + cos(float(lat1) * p) * \
        cos(float(lat2) * p) * (1 - cos((float(lon2) - float(lon1)) * p)) / 2
    return 12742 * asin(sqrt(a))


def majorCityFinder(name, currLoc, Data):
    closest = 100000
    ret_nm = name
    ind = -1
    for i in enumerate(Data):
        if name == i[1][0]:
            return i[1], -1, 0
        elif distance(currLoc[0], currLoc[1], i[1][1], i[1][2]) < closest:
            closest = distance(currLoc[0], currLoc[1], i[1][1], i[1][2])
            ret_nm = i[1]
            ind = i[0]
    return ret_nm, ind, closest


def nearby3(name, currLoc, Data):
    gg = Data.copy()
    a = majorCityFinder(name, currLoc, gg)
    gg.pop(a[1])
    b = majorCityFinder(name, currLoc, gg)
    gg.pop(b[1])
    c = majorCityFinder(name, currLoc, gg)
    return a, b, c


def local(dist):
    if dist < 20:
        return "cab", dist*10
    else:
        return "bus", dist*2
