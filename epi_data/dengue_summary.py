#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import os

counter = 0
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
locid_xy_map = dict()
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
        locid_xy_map[locid]   = (float(p[2]), float(p[3]))
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
epi_data_file = 'prevalence5490.out'
header = True
fi = file(epi_data_file)

week_ctr = 0

def next_data(fi):
    global week_ctr
    global httpd
    print week_ctr
    week_ctr += 1
    line = fi.readline()
    p = line.strip().split(',')
    if p[0] == 'time':
        line = fi.readline()
        p = line.strip().split(',')
    data = []
    day = int(p[0])
    if day >= 365:
        httpd.server_close()
        httpd.stopped = True
        
    locid = int(p[3])
    data.append([ p[0], locid_muni_map[locid], locid_xy_map[locid] ] )
    starting_day = day
    fileSize = os.fstat(fi.fileno()).st_size

    while day < starting_day + 7:
        file_loc = fi.tell()

        if  file_loc == fileSize:
            fi.seek(0)

        line = fi.readline()
        p = line.strip().split(',')
        day = int(p[0])
        #print day
        if day >= starting_day + 7:
            fi.seek(file_loc)
            break
        else:
            locid = int(p[3])
            data.append([ p[0], locid_muni_map[locid], locid_xy_map[locid] ] )
    return data

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  

    def do_GET(self):
        global counter
        global fi
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path.endswith("next"):
            print "got a request..\n";
            data = next_data(fi)
            self.wfile.write("[");
            for i,d in enumerate(data):
                self.wfile.write('{ "day": ' + d[0] + ', "muni": ' + str(d[1]) + ', "x":' + str(d[2][0]) + ', "y":' + str(d[2][1]) +' }' );
                if i < len(data) -1:
                    self.wfile.write(',')
            self.wfile.write("]")
            print "done sending request..\n";
        elif self.path.endswith("yuc_muni2.json"):
            self.wfile.write(file("../yuc_muni2.json").read())
        else:
            self.wfile.write(file("../mex.html").read())
        
        return


print('Server listening on port 8000...')
httpd = SocketServer.TCPServer(('', 8000), Handler)
httpd.serve_forever()

