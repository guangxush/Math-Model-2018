# -*- encoding:utf-8 -*-
# import numpy as np
import math
import numpy as np
from numpy import random,mat
import collections
from short_path import dijkstra_all_minpath


# 从文件中读取距离数据，转换成二维向量
def process_value():
    fr = open('../data/city_dist.txt', 'r')
    city_dist = dict()
    city_name = ['heb', 'bj&tj', 'wlmq', 'sh', 'zz', 'xa', 'wh', 'cq', 'cd', 'ls', 'gz&sz', 'km']
    city_num = len(city_name)
    city_city_array = []
    i = 0
    for line in fr.readlines():
        # print line
        j = 0
        city_array = []
        for dist in line.strip('\n').split('	'):
            # print(dist)
            if i <= j:
                city_array.append(float(dist))
                city_dist['(' + str(i) + ',' + str(j) + ')'] = float(dist)
            else:
                city_array.append(float(0))
                city_dist['(' + str(i) + ',' + str(j) + ')'] = float(0)
            j += 1
        city_city_array.append(city_array)
        i += 1
    # print(city_city_array)
    # for city_city in city_city_array:
    #     for city in city_city:
    #         print city,
    #     print
    fr.close()
    return city_city_array


# 计算城市的带宽
def cal_city_value(city_city_array):
    # city_city_array = process_value()
    city_city_value_array = []
    for city_city in city_city_array:
        city_value_array = []
        for city in city_city:
            if (city <= 600) & (city != 0):
                city_value = 32
            elif (city >= 600) & (city <= 1200):
                city_value = 16
            elif (city >= 1200) & (city <= 3000):
                city_value = 8
            elif city >= 3000 or city == 0:
                city_value = 0
            city_value_array.append(city_value)
        city_city_value_array.append(city_value_array)
    # for city_value_array in city_city_value_array:
    #     for city_value in city_value_array:
    #         print city_value,
    #     print
    return city_city_value_array


# 计算城市的人口系数
def cal_population():
    population = [1064, 3735, 268, 2420, 972, 883, 1071, 3048, 1717, 55, 2595, 673]
    popu_popu_array = []
    i = j = 0
    for popu_i in population:
        i += 1
        popu_array = []
        for popu_j in population:
            j += 1
            if i < j:
                popu_array.append(math.sqrt(popu_i*popu_j))
            else:
                popu_array.append(0.0)
        j = 0
        popu_popu_array.append(popu_array)
    # for popu_array in popu_popu_array:
    #     for popu in popu_array:
    #         print popu,
    #     print
    return popu_popu_array


# 计算城市人口系数*人口容量
def array_mul_array(array1, array2):
    array_array_result = []
    for i in range(len(array1)):
        array_result = []
        for j in range(len(array1[i])):
            array_result.append(array1[i][j]*array2[i][j])
        array_array_result.append(array_result)
    return array_array_result


# 打印数组
def print_dim2_array(array_array):
    for array in array_array:
        for i in array:
            print(i),
        print
    print


# 按照系数大小排序
def value_sort(city_mul_popu_value):
    city_value = dict()
    i = 0
    for city_mul_popus in city_mul_popu_value:
        # print line
        j = 0
        for city_mul_popu in city_mul_popus:
            print(city_mul_popu),
            # if i <= j:
            city_value[str(i)+','+str(j)] = float(city_mul_popu)
            j += 1
        i += 1
        print
    # print(city_value)
    city_value_sort = collections.OrderedDict(sorted(city_value.items(), key=lambda x: x[1], reverse=True))
    # print(city_value_sort)
    for k, v in city_value_sort.items():
        print(k, v)
    return city_value_sort


# 最小生成树改进算法选择分数较高的城市
def select_top_city(city_value_sort, city_num):
    result_dict = dict()
    city_label = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    city_label_dict = dict()
    for city in city_label:
        city_label_dict[city] = 0
    # city_used = []
    count = 0
    for k, v in city_value_sort.items():
        count += 1
        if count > city_num:
            break
        # print(k, v)
        city_1 = int(k.split(',')[0])
        city_2 = int(k.split(',')[1])
        city_label_dict[city_1] = city_label_dict[city_1] + 1
        city_label_dict[city_2] = city_label_dict[city_2] + 1
        if city_1 in city_label:
            # city_used.append(city_1)
            city_label.remove(city_1)
        if city_2 in city_label:
            # city_used.append(city_2)
            city_label.remove(city_2)
        print(str(city_1)+','+str(city_2))
        result_dict[k] = v
        city_value_sort.pop(k)
    # print()
    # print(city_label)
    # print()
    # city_value_sort表示剩余元素
    # result_dict表示最后要的元素
    # print(city_used)
    result_dict_sort = collections.OrderedDict(sorted(result_dict.items(), key=lambda x: x[1], reverse=True))
    residual = city_num - len(city_label)
    count = residual
    # print("--------------")
    # for k,v in city_label_dict.items():
    #     print k,v
    # print(city_value_sort)
    for i in range(residual):
        if count > city_num or not city_label:
            break
        for k, v in city_value_sort.items():
            city_1 = int(k.split(',')[0])
            city_2 = int(k.split(',')[1])
            # 如果找到了含有当前city_label剩余元素的元素
            if city_1 in city_label or city_2 in city_label:
                if city_1 in city_label:
                    city_label_dict[city_1] = city_label_dict[city_1] + 1
                    city_label.remove(city_1)
                    # city_used.append(city_1)
                    # city_label.remove(city_1)
                if city_2 in city_label:
                    city_label_dict[city_2] = city_label_dict[city_2] + 1
                    city_label.remove(city_2)
                    # city_used.append(city_2)
                    # city_label.remove(city_2)
                print(str(city_1) + ',' + str(city_2))
                # 删除元素部分
                # 首先把之前排好序的字典倒排序，系数小的在前，系数大的在后
                selected_dict_sort = collections.OrderedDict(sorted(result_dict.items(), key=lambda x: x[1], reverse=False))
                # selected_dict_sort表示已经排好的元素
                # print('****************')
                # print(selected_dict_sort)
                # print('****************')
                # 去已经排好的字典中查找元素
                for k1, v1 in selected_dict_sort.items():
                    city_1 = int(k1.split(',')[0])
                    city_2 = int(k1.split(',')[1])
                    # 如果在数量都大于一次，那么把它剔除
                    if city_label_dict[city_1] > 1 and city_label_dict[city_2] > 1:
                        selected_dict_sort.pop(k1)
                        city_label_dict[city_1] = city_label_dict[city_1] - 1
                        city_label_dict[city_2] = city_label_dict[city_2] - 1
                        print(k1+"已经删除！")
                        break
                        # 相应的地方也要剔除
                        city_value_sort.pop(k)
                # 新元素加入其中
                # result_dict_sort.popitem()  # 去掉最后一个元素
                result_dict = selected_dict_sort
                result_dict[k] = v
                print(k+"已经添加！")
                # city_value_sort.pop(k)
        count += 1
    result_dict_sort = collections.OrderedDict(sorted(result_dict.items(), key=lambda x: x[1], reverse=True))
    print("最终筛选结果为：")
    for k, v in result_dict_sort.items():
        print(k, v)
    return result_dict_sort


# 字典中的元素放入到数组里面
def dict_to_array(result_dict, city_mul_popu_value):
    # 创建一个大小一样的空数组
    city_mul_popu_value_new = []
    city_mul_popu_value_key = []
    city_mul_popu_value_isnull = []
    for city_mul_popus in city_mul_popu_value:
        city_mul_popu_value_new_sub = []
        city_mul_popu_value_key_sub = []
        city_mul_popu_value_isnull_sub = []
        for city_mul_popu in city_mul_popus:
            city_mul_popu_value_new_sub.append(0)
            city_mul_popu_value_key_sub.append(0)
            city_mul_popu_value_isnull_sub.append(0)
        city_mul_popu_value_new.append(city_mul_popu_value_new_sub)
        city_mul_popu_value_key.append(city_mul_popu_value_key_sub)
        city_mul_popu_value_isnull.append(city_mul_popu_value_isnull_sub)
    # print_dim2_array(city_mul_popu_value_new)
    for k, v in result_dict.items():
        print(k, v)
        city_1 = int(k.split(',')[0])
        city_2 = int(k.split(',')[1])
        city_mul_popu_value_new[city_1][city_2] = v
        city_mul_popu_value_key[city_1][city_2] = k
        city_mul_popu_value_isnull[city_1][city_2] = 1
    return city_mul_popu_value_key, city_mul_popu_value_new, city_mul_popu_value_isnull


# 三角矩阵转换成邻接矩阵
def triangle2rectangle(city_mul_popu_value_new):
    city_mul_popu_value_rec = []
    i = 0
    for city_mul_popu_value in city_mul_popu_value_new:
        i += 1
        city_mul_popu_value_rec_sub = []
        for count in range(i):
            city_mul_popu_value_rec_sub.append(0)
        for city_mul_popu in city_mul_popu_value:
            city_mul_popu_value_rec_sub.append(city_mul_popu)
        city_mul_popu_value_rec.append(city_mul_popu_value_rec_sub)
    '''city_mul_popu_value_rec_sub = []
    for count in range(i):
        city_mul_popu_value_rec_sub.append(0)
    city_mul_popu_value_rec.append(city_mul_popu_value_rec_sub)'''
    return city_mul_popu_value_rec


# 转换成带权值的邻接矩阵
def to_adjacency_matrix(city_mul_popu_isnull_rec):
    city_mul_popu_isnull_adg = []
    for city_mul_popu_isnull_rec_sub in city_mul_popu_isnull_rec:
        city_mul_popu_isnull_adg_sub = []
        for items in city_mul_popu_isnull_rec_sub:
            if items == 0:
                items = 999999
            city_mul_popu_isnull_adg_sub.append(items)
        city_mul_popu_isnull_adg.append(city_mul_popu_isnull_adg_sub)
    return city_mul_popu_isnull_adg


# 转换成带权值的对称邻接矩阵
def to_adjacency_symmetry_matrix(city_mul_popu_isnull_rec):
    symmetry_array = []
    for city_mul_popu_isnull_rec_sub in city_mul_popu_isnull_rec:
        symmetry_array_sub = []
        for items in city_mul_popu_isnull_rec_sub:
            symmetry_array_sub.append(0)
        symmetry_array.append(symmetry_array_sub)
    i = 0
    for city_mul_popu_isnull_rec_sub in city_mul_popu_isnull_rec:
        j = 0
        for items in city_mul_popu_isnull_rec_sub:
            if i == j:
                symmetry_array[i][j] = 0
            elif i > j:
                symmetry_array[i][j] = city_mul_popu_isnull_rec[j][i]
            else:
                symmetry_array[i][j] = city_mul_popu_isnull_rec[i][j]
            j += 1
        i += 1
    # print_dim2_array(symmetry_array)
    return symmetry_array


# 计算每个点的直接连接数目
def cal_connection_count(symmetry_array):
    city_label = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    city_connect = dict()
    city_label_count = 0
    for city_sub in symmetry_array:
        count = 0
        for city in city_sub:
            if city == 1:
                count += 1
        city_connect[city_label[city_label_count]] = count
        city_label_count += 1
    city_connect_sort = collections.OrderedDict(sorted(city_connect.items(), key=lambda x: x[1], reverse=True))
    for k, v in city_connect_sort.items():
        print(k, v)
    return city_connect_sort


# 路径系数表
def cal_coefficient(city_connect_sort, city_value_array, symmetry_array, max_length):
    # 生成一维最大长度为max_length的数组
    max_length_array = []
    for i in range(max_length):
        max_length_array.append(0)
    # path_array, path_result = dijkstra_all_minpath(key, symmetry_array)
    # 定义一个系数空数组
    connect_coefficient = []
    for city_value_array_sub in city_value_array:
        connect_coefficient_sub = []
        for items in city_value_array_sub:
            connect_coefficient_sub.append([])
        connect_coefficient.append(connect_coefficient_sub)
    print(connect_coefficient)
    update_symmetry_array = symmetry_array
    # 逐一筛选，选出元素并填充到数组
    for iterator in range(12):
        key = city_connect_sort.popitem()
        path_array, path_result = dijkstra_all_minpath(key[0], symmetry_array)
        for path in path_result:
            print(path)
            length = len(path)-1
            count = 0
            for path_items in path:
                if count < length:
                    print(path_items)
                    connect_coefficient[int(path[count])][int(path[count+1])].append(int(1))
                count += 1
        update_symmetry_array = update_city_value(update_symmetry_array, key[0])
        print(str(key[0]) + "已经被计算，图被更新！")
        print(path_result)
    print(connect_coefficient)
    return connect_coefficient


# 路径最大长度查询
def get_max_length(city_connect_sort, symmetry_array):
    update_symmetry_array = symmetry_array
    max_length = 0
    for i in range(12):
        key = city_connect_sort.popitem()
        path_array, path_result = dijkstra_all_minpath(key[0], update_symmetry_array)
        for path in path_result:
            if max_length < len(path):
                max_length = len(path)
        update_symmetry_array = update_city_value(update_symmetry_array, key[0])
        print(str(key[0]) + "已经被计算，图被更新！")
        print(path_result)
    return max_length


# 更新一个节点的系数
def update_city_value(symmetry_array, key):
    i = 0
    for symmetry_array_sub in symmetry_array:
        j = 0
        for items in symmetry_array_sub:
            if i == key or j == key:
                symmetry_array[i][j] = 999999
            j += 1
        i += 1
    # print_dim2_array(symmetry_array)
    return symmetry_array


if __name__ == '__main__':
    city_city_array = process_value()
    print_dim2_array(city_city_array)

    city_value_array = cal_city_value(city_city_array)
    print_dim2_array(city_value_array)

    popu_popu_array = cal_population()
    print_dim2_array(popu_popu_array)

    city_mul_popu_value = array_mul_array(popu_popu_array, city_value_array)
    print_dim2_array(city_mul_popu_value)

    city_value_sort = value_sort(city_mul_popu_value)
    result_dict = select_top_city(city_value_sort, 16)
    print("最终筛选结果为："+str(len(result_dict)))
    print(result_dict)

    city_mul_popu_value_key, city_mul_popu_value_new, city_mul_popu_value_isnull = dict_to_array(result_dict, city_mul_popu_value)
    print_dim2_array(city_mul_popu_value_new)
    print_dim2_array(city_mul_popu_value_key)

    # city_mul_popu_value_rec = triangle2rectangle(city_mul_popu_value_new)
    # city_mul_popu_key_rec = triangle2rectangle(city_mul_popu_value_key)
    # city_mul_popu_isnull_rec = triangle2rectangle(city_mul_popu_value_isnull)
    # print_dim2_array(city_mul_popu_value_rec)
    # print_dim2_array(city_mul_popu_key_rec)
    # print_dim2_array(city_mul_popu_isnull_rec)

    city_mul_popu_isnull_adg = to_adjacency_matrix(city_mul_popu_value_isnull)
    print_dim2_array(city_mul_popu_isnull_adg)

    symmetry_array = to_adjacency_symmetry_matrix(city_mul_popu_isnull_adg)
    symmetry_array_use = to_adjacency_symmetry_matrix(city_mul_popu_isnull_adg)
    print_dim2_array(symmetry_array_use)
    # dijkstra_all_minpath(0, symmetry_array)
    # print("------------")
    # dijkstra_all_minpath(11, symmetry_array)
    city_connect_sort = cal_connection_count(symmetry_array)
    city_connect_sort_use = cal_connection_count(symmetry_array)
    # key = city_connect_sort.popitem()
    # print(key[0])
    # cal_coefficient(symmetry_array, key[0])
    # update_symmetry_array = update_city_value(symmetry_array, key[0])
    # cal_coefficient(update_symmetry_array, key[0])

    max_length = get_max_length(city_connect_sort, symmetry_array)
    print(max_length)
    # top_city = select_top_city(city_value_sort)
    # print_dim2_array(top_city)
    connect_coefficient = cal_coefficient(city_connect_sort_use, city_value_array, symmetry_array_use, max_length)
    print_dim2_array(connect_coefficient)