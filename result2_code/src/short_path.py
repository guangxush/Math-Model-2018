# -*- encoding:utf-8 -*-
_ = inf = 999999  # inf


def dijkstra_all_minpath(start, matrix):
    length = len(matrix)  # 该图的节点数
    path_array = []
    temp_array = []
    path_array.extend(matrix[start])  # 深复制
    temp_array.extend(matrix[start])  # 深复制
    temp_array[start] = inf  # 临时数组会把处理过的节点的值变成inf，表示不是最小权值的节点了
    already_traversal = [start]  # start已处理
    path_parent = [start] * length  # 用于画路径，记录此路径中该节点的父节点
    path_result = []
    while len(already_traversal) < length:
        i = temp_array.index(min(temp_array))  # 找最小权值的节点的坐标
        temp_array[i] = inf
        path = [str(i)]  # 用于画路径
        k = i
        while path_parent[k] != start:  # 找该节点的父节点添加到path，直到父节点是start
            path.append(str(path_parent[k]))
            k = path_parent[k]
        path.append(str(start))
        path.reverse()  # path反序产生路径
        print(str(i) + ':', '->'.join(path))  # 打印路径
        if path not in path_result:
            path_result.append(path)
        already_traversal.append(i)  # 该索引已经处理了
        for j in range(length):
            if j not in already_traversal:
                if (path_array[i] + matrix[i][j]) < path_array[j]:
                    path_array[j] = temp_array[j] = path_array[i] + matrix[i][j]
                    path_parent[j] = i  # 说明父节点是i
    return path_array, path_result


# 邻接矩阵
adjacency_matrix = [[0, 10, _, 30, 100],
                    [10, 0, 50, _, _],
                    [_, 50, 0, 20, 10],
                    [30, _, 20, 0, 60],
                    [100, _, 10, 60, 0]
                    ]
print(dijkstra_all_minpath(4, adjacency_matrix))
