#!/usr/bin/python

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

muni_pop_file = 'population_size_by_municipality'
muni_sizes = dict()

for line in file(muni_pop_file):
    muni, size = map(int,line.strip().split(','))
    muni_sizes[muni] = size

muni_lookup_file = '../geo_data/muni_lookup'
muni_names = dict()
header = True

for line in file(muni_lookup_file):
    if header:
        header = False
        continue
    p = line.strip().split('\t')
    muni, name = int(p[0]), p[3]
    muni_names[muni] = name

print 'index id pop name'
for i, m in enumerate(munis):
    print i, m, muni_sizes[m], muni_names[m]
