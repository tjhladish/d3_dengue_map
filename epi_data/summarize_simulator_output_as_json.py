#!/usr/bin/python
import json

pixel_size = 0.00416667
min_x_center = -90.40409499
min_y_center = 19.72078911
pixel_muni_map_file = '../geo_data/all_yucatan_pixels.out'

# municipality IDs, in the order specified in the yucatan municipalities shapefile
# this needs to be the same order that the features are listed in the SVG!!
munis = [21835, 21915, 21836, 21916, 21837, 21917, 21838, 21918, 21839, 21919,
         21840, 21920, 21841, 21921, 21842, 21922, 21843, 21923, 21844, 21924,
         21845, 21935, 21846, 21936, 21847, 21937, 21848, 21938, 21849, 21939,
         21850, 21940, 21851, 21852, 21853, 21854, 21855, 21856, 21857, 21858,
         21859, 21860, 21861, 21862, 21863, 21864, 21865, 21866, 21867, 21868,
         21869, 21870, 21871, 21872, 21873, 21874, 21875, 21876, 21877, 21878,
         21879, 21880, 21881, 21882, 21883, 21884, 21885, 21886, 21887, 21888,
         21889, 21890, 21891, 21892, 21893, 21894, 21895, 21896, 21897, 21898,
         21899, 21900, 21901, 21902, 21903, 21904, 21905, 21906, 21907, 21908,
         21909, 21910, 21911, 21912, 21913, 21914, 21925, 21926, 21927, 21928,
         21929, 21930, 21931, 21932, 21933, 21934]


def x_to_col_num(x):
    return int(round((x - min_x_center)/pixel_size))

def y_to_row_num(y):
    return int(round((y - min_y_center)/pixel_size))

pixel_muni_map = dict()
for line in file(pixel_muni_map_file):
    p = line.strip().split()
    x,y,muni = float(p[0]), float(p[1]), int(p[3])
    pixel_muni_map[(x_to_col_num(x), y_to_row_num(y))] = munis.index(muni)

'''
tjhladish@peregrine:~/www/d3_dengue_map/epi_data$ head ../geo_data/all_yucatan_pixels.out 
-88.29992664    20.63328984     0.2233016342    21915   Tekom
-88.29575997    20.63328984     0.2515507936    21915   Tekom
-88.2915933     20.63328984     0.1853555888    21915   Tekom
-88.28742663    20.63328984     0.1996035874    21915   Tekom
'''
'''
id type x y x_ctr y_ctr
1 house -89.6848792716 20.6464119922 -89.68326108 20.64578985
2 house -89.6348973583 20.7191701666 -89.63326104 20.72078991
3 house -89.6792403917 20.6473767917 -89.67909441 20.64578985
'''

locid_muni_map = dict()
#locid_xy_map = dict()
locid_pixel_ctr_map = dict()
locations_file = '../epi_data/locations-yucatan_final.txt'
header = True

for line in file(locations_file):
    if header:
        header = False
        continue
    p = line.strip().split()
    if p[1] != 'house':
        continue
    locid = int(p[0])
    xy = (x_to_col_num(float(p[4])), y_to_row_num(float(p[5])))
    try:
        locid_muni_map[locid] = pixel_muni_map[xy]
        #locid_xy_map[locid]   = (float(p[2]), float(p[3]))
        locid_pixel_ctr_map[locid]   = (float(p[4]), float(p[5]))
    except KeyError:
        print line

'''
time,type,id,location,serotype,symptomatic,withdrawn
0,p,550896,113833,4,1,0
0,p,136572,26568,2,1,0
0,p,1304,261,3,0,0
1,p,1789293,370715,2,1,0
1,p,550896,113833,4,1,0
1,p,136572,26568,2,1,0
1,p,75739,15700,3,1,0
1,p,1304,261,3,0,0
2,p,1789293,370715,2,1,0
'''
def get_data(epi_data_file):
    data = []
    pixels = set()
    #minx, maxx, miny, maxy = (), None, (), None

    for line in file(epi_data_file): 
        p = line.strip().split(',')
        if p[0] == 'time': # we're looking at the header
            continue

        day = int(p[0])
        locid = int(p[3])
        xctr, yctr = locid_pixel_ctr_map[locid]

        #minx = min(minx, xctr)
        #miny = min(miny, yctr)
        #maxx = max(maxx, xctr)
        #maxy = max(maxy, yctr)

        pixels.add((xctr, yctr))
        data.append({'day':int(p[0]), 'muni':locid_muni_map[locid], 'coords':(xctr, yctr) })

    return pixels, data#, [minx, maxx, miny, maxy]

def aggregate_data(pixels, data):
    agg_data  = [ dict() for i in range(data[-1]['day'] + 2) ]
    for datum in data:
        day = datum['day']
        if datum['coords'] in agg_data[day]: 
            agg_data[day][datum['coords']]['cases'] += 1 
            #agg_data[day+1][datum['coords']] = 0 
        else:
            agg_data[day][datum['coords']] = dict()
            agg_data[day][datum['coords']]['muni'] = datum['muni']
            agg_data[day][datum['coords']]['cases'] = 1 

    json_data = []
    for day in range(len(agg_data)):
        json_data.append([])
        for coord in agg_data[day].keys():
            json_data[day].append([coord[0], coord[1], agg_data[day][coord]['cases'], agg_data[day][coord]['muni']])
            #json_data[day].append({'x':coord[0], 'y':coord[1], 'cases':agg_data[day][coord]})

    return json_data

epi_data_file = 'prevalence5490.out'
pixels, data = get_data(epi_data_file)
json_data = aggregate_data(pixels, data)
print json.dumps(json_data)

#output_data = [{'day':n, 'data':[{'muni':name, 'cases':num},{},{}]}, {}, {} ]
#output_data = [{'day':n, 'data':[{'x':x_val, 'y':y_val, 'cases':num},{},{}]}, {}, {} ]














