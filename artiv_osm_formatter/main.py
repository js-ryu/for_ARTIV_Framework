import OSMHandler

import sys
import math
import numpy as np
from haversine import haversine

import time

before_time = time.time()
start_time = before_time

meter_cut = 1

script = sys.argv[0]
filename_input = sys.argv[1:]

if len(filename_input) == 0:
    output = open("A2_LINK_output.osm", mode='wt')
    file_name = "A2_LINK.osm"

elif len(filename_input) == 1:
    output = open(filename_input[0][:-4] + "_output.osm", mode='wt')
    file_name = filename_input[0]    

elif len(filename_input) == 2:
    output = open(filename_input[1], mode='wt')
    file_name = filename_input[0]   

else:
    raise Exception('Invalid Arguments')


#새로 만든 node의 id가 기존의 id와 겹치지 않게 조정
def check_new_id(nid, id_list):
    if np.isin(-nid, id_list):
        nid += 1

    else:
        return nid

    return check_new_id(nid, id_list)


if __name__ == '__main__':

    #기존 osm 데이터 parsing
    osm_data = OSMHandler.OSM_data(file_name)

    nodes = []
    ways = []
    new_nodes = []
    new_ways = []

    for data in osm_data:
        if data[0] == 'node' :
            nodes.append(data[1:4])

        elif data[0] == 'way' :
            ways.append(data)

    nodes = np.array(nodes)    

    node_ids = nodes[:,0]




    now_time = time.time()
    sec = now_time - before_time
    print("Process 1")
    print("현재까지", now_time-start_time,"초, 이전 과정과", sec,"초 차이")
    print("")
    before_time = now_time

    #node 세분화

    id_count = 200000

    for way in ways:
        ref_nodes = way[2] #way를 구성하는 nodes
        
        #print(ref_nodes)
        cnt = 0

        ref_nodes_num = len(ref_nodes)

        every_nodes_for_each_way = []

        #노드 간격 파악 후 세분화
        while cnt < ref_nodes_num - 1:
            id1, id2 = ref_nodes[cnt], ref_nodes[cnt+1]

            temp_nodes = dict()

            id1_idx = np.where(nodes[:,0] == id1)
            temp_nodes['id1'] = nodes[id1_idx][0][1:]

            id2_idx = np.where(nodes[:,0] == id2)
            temp_nodes['id2'] = nodes[id2_idx][0][1:]

            #node 간 거w리를 haversine 공식으로 계산
            temp_dist = haversine(temp_nodes['id1'], temp_nodes['id2'], unit = 'm')

            #설정한 간격 이하로 노드 간격을 맞추기 위해 필요한 노드의 개수
            n = math.ceil((1/meter_cut)*temp_dist + 1) 

            #새로운 nodes 형성
            temp_new_nodes = []

            temp_point_x = (temp_nodes['id1'][0])
            temp_point_y = (temp_nodes['id1'][1])
            temp_new_nodes.append([id1, temp_point_x,temp_point_y])

            for k in range(1,n-1):
                temp_point_x = (temp_nodes['id1'][0]*(n-1-k) + temp_nodes['id2'][0]*k)/(n-1)
                temp_point_y = (temp_nodes['id1'][1]*(n-1-k) + temp_nodes['id2'][1]*k)/(n-1)
                temp_new_nodes.append([0, temp_point_x,temp_point_y])

            every_nodes_for_each_way.extend(np.array(temp_new_nodes))

            cnt += 1

            #way내 마지막 node
            if cnt == ref_nodes_num - 1:
                every_nodes_for_each_way.append(np.array([id2, temp_nodes['id2'][0],temp_nodes['id2'][1]]))
        
        every_nodes_for_each_way = np.array(every_nodes_for_each_way)

        #새로운 nodes에 id 부여

        no_id_idx = np.isin(every_nodes_for_each_way[:,0], 0)

        for i, tf in enumerate(no_id_idx):
            if tf:
                id_count = check_new_id(id_count, node_ids)
                every_nodes_for_each_way[i][0] = -id_count
                id_count += 1

        #way에 새로 만들어진 node들을 추가
        temp_id_list = every_nodes_for_each_way[:,0]
        temp_id_list = list(temp_id_list.astype(int))

        way[2] = temp_id_list

        

        new_nodes.extend(every_nodes_for_each_way)
        #for w_node in every_nodes_for_each_way:
        #    new_nodes.append(['node', w_node[0], w_node[1], w_node[2], 0, {}])
        
    now_time = time.time()
    sec = now_time - before_time
    print("Process 2")
    print("현재까지", now_time-start_time,"초, 이전 과정과", sec,"초 차이")
    print("")
    before_time = now_time

    #중복 노드 제거
    new_nodes = np.array(new_nodes)

    nodes_uni = [tuple(row) for row in new_nodes]
    nodes_uni = list(set(nodes_uni))

    now_time = time.time()
    sec = now_time - before_time
    print("Process 3")
    print("현재까지", now_time-start_time,"초, 이전 과정과", sec,"초 차이")
    print("")
    before_time = now_time
    

    text = ["<?xml version='1.0' encoding='UTF-8'?>\n", "<osm version='0.6' upload='false' generator='JOSM'>\n"]

    for nd in nodes_uni:
        text.append("  <node id='{0}' lat='{1}' lon='{2}' />\n".format(int(nd[0]), nd[1], nd[2]))


    now_time = time.time()
    sec = now_time - before_time
    print("Process 4")
    print("현재까지", now_time-start_time,"초, 이전 과정과", sec,"초 차이")
    print("")
    before_time = now_time



    for w in ways:
        text.append("  <way id='{0}' action='modify'>\n".format(w[1]))
        for nd in w[2]:
            text.append("    <nd ref='{0}' />\n".format(nd))
        keys=[]
        keys = w[4].keys()
        for key in keys:
            text.append("    <tag k='{0}' v='{1}' />\n".format(key, w[4][key]))
        text.append("  </way>\n")

                        
    text.append("</osm>")

    for line in text:
        output.write(line)


output.close()

now_time = time.time()
sec = now_time - before_time
print("Process 5")
print("현재까지", now_time-start_time,"초, 이전 과정과", sec,"초 차이")
print("")
before_time = now_time
print("DONE!")
