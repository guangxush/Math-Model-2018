# -*- encoding:utf-8 -*-
# import numpy as np
import collections


def value_sort():
    fr = open('../data/city_value.txt', 'r')
    fw = open('../data/city_value_sort.txt', 'w')
    city_value = dict()
    city_name = ['heb', 'bj&tj', 'wlmq', 'sh', 'zz', 'xa', 'wh', 'cq', 'cd', 'ls', 'gz&sz', 'km']
    city_num = len(city_name)
    i = 0
    for line in fr.readlines():
        # print line
        i += 1
        j = 0
        for dist in line.strip('\n').split('	'):
            # print(dist)
            j += 1
            if i < j:
                city_value['('+str(i)+','+str(j)+')'] = float(dist)
    print(city_value)
    city_value_sort = collections.OrderedDict(sorted(city_value.items(), key=lambda x: x[1], reverse=True))
    print(city_value_sort)
    for k, v in city_value_sort.items():
        print(k, v)
        fw.write(str(k) + str(v) + '\n')
    fr.close()
    fw.close()
    return


if __name__ == '__main__':
    value_sort()