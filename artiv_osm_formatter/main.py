import OSMHandler

import argparse
import math
import numpy as np
from haversine import haversine

#Arguments Parsing
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', nargs='*', help='file_names', default=[], dest='file_names')
parser.add_argument('--option', '-o', nargs='*', help='options', default=[], dest='options')

filename_input = parser.parse_args().file_names
option_input = parser.parse_args().options

if len(filename_input) == 0:
    output = open("A2_LINK_output.osm", mode='wt')
    file_name = "A2_LINK.osm"
    lane_file_name = "B2_SURFACELINEMARK.osm"
    print("----------ARTIV_OSM_FORMATTER----------")
    print('LINK File : "A2_LINK.osm"')
    print('LANE File : "B2_SURFACELINEMARK.osm"')
    print('Output File : "A2_LINK_output.osm"')
    print("")

elif len(filename_input) == 1:
    output = open(filename_input[0][:-4] + "_output.osm", mode='wt')
    file_name = filename_input[0]   
    lane_file_name = "B2_SURFACELINEMARK.osm"
    print("----------ARTIV_OSM_FORMATTER----------")
    print('LINK File :', filename_input[0])
    print('LANE File : "B2_SURFACELINEMARK.osm"')
    print('Output File :', filename_input[0][:-4] + "_output.osm")
    print("")

elif len(filename_input) == 2:
    output = open(filename_input[0][:-4] + "_output.osm", mode='wt')
    file_name = filename_input[0]   
    lane_file_name = filename_input[1]
    print("----------ARTIV_OSM_FORMATTER----------")
    print('LINK File :', filename_input[0])
    print('LANE File :', filename_input[1])
    print('Output File :', filename_input[0][:-4] + "_output.osm")
    print("")

elif len(filename_input) == 3:
    output = open(filename_input[2], mode='wt')
    file_name = filename_input[0]   
    lane_file_name = filename_input[1]
    print("----------ARTIV_OSM_FORMATTER----------")
    print('LINK File :', filename_input[0])
    print('LANE File :', filename_input[1])
    print('Output File :', filename_input[2])
    print("")

else:
    raise Exception('Invalid Arguments')


if len(option_input) == 0:
    node_interval = 1
    lane_change_nodes = 20


elif len(option_input) == 1:
    node_interval = float(option_input[0])
    lane_change_nodes = 20

elif len(option_input) == 2:
    node_interval = float(option_input[0])
    lane_change_nodes = int(option_input[1])

else:
    raise Exception('Invalid Arguments')

print('Node Interval :', node_interval, 'meter(s)')
print('# of Lane Change Nodes :', lane_change_nodes)
print("")


#새로 만드는 id가 기존의 id와 겹치지 않게 조정하는 함수
def check_new_id(nid, id_list):
    if np.isin(-nid, id_list):
        nid += 1

    else:
        return nid

    return check_new_id(nid, id_list)


if __name__ == '__main__':
    #기존 주행유도선 파일 데이터 parsing
    osm_data = OSMHandler.OSM_data(file_name)

    nodes = []
    ways = []
    new_nodes = []
    way_id_lst = []

    for data in osm_data:
        if data[0] == 'node' :
            nodes.append(data[1:4])

        elif data[0] == 'way' :
            ways.append(data)
            way_id_lst.append(data[1])

    nodes = np.array(nodes)    
    node_ids = nodes[:,0]

    #node 세분화
    id_count = 200000 #새로 만드는 node ID는 200000부터 시작 

    for way in ways:
        ref_nodes = way[2] #way를 구성하는 nodes
 
        cnt = 0
        ref_nodes_num = len(ref_nodes)
        every_nodes_for_each_way = []

        #node 간격 파악 후 세분화
        while cnt < ref_nodes_num - 1:
            id1, id2 = ref_nodes[cnt], ref_nodes[cnt+1]

            temp_nodes = dict()

            id1_idx = np.where(nodes[:,0] == id1)
            temp_nodes['id1'] = nodes[id1_idx][0][1:]

            id2_idx = np.where(nodes[:,0] == id2)
            temp_nodes['id2'] = nodes[id2_idx][0][1:]

            #node 간 거리를 haversine 공식으로 계산
            temp_dist = haversine(temp_nodes['id1'], temp_nodes['id2'], unit = 'm')

            #설정한 간격 이하로 노드 간격을 맞추기 위해 필요한 노드의 개수
            n = math.ceil((1/node_interval)*temp_dist + 1) 

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
        
        #pyroutelib3 사용을 위해 way에 태그 추가
        way[3] += 1
        way[4]['highway'] = 'trunk'

        new_nodes.extend(every_nodes_for_each_way)

    #중복 노드 제거
    new_nodes = np.array(new_nodes)

    nodes_uni = [tuple(row) for row in new_nodes]
    nodes_uni = list(set(nodes_uni))

    nodes_np = np.array(nodes_uni)

    #노드 세분화 완료, 차선변경 WAY제작 시작
    lane_data = OSMHandler.OSM_data(lane_file_name)

    left_change = [] #왼쪽으로만 차선 변경이 가능할 경우 right to left
    right_change = [] #오른쪽으로만 차선 변경이 가능할 경우 left to right
    both_change = [] #양쪽으로 차선 변경이 가능할 경우 

    #차선 변경 가능한 경우 파싱
    for data in lane_data:
        if data[0] == 'way' :
            if data[4]['Type'] == '212': #백색 점선 
                try:
                    both_change.append((data[4]['L_LinkID'], data[4]['R_LinkID']))
                except: #점선이지만 양쪽에 주행유도선이 없는경우도 있음.. e.g. roundabout
                    pass

            elif data[4]['Type'] == '223': #백색 좌점혼선
                try:
                    right_change.append((data[4]['L_LinkID'], data[4]['R_LinkID']))
                except:
                    pass

            elif data[4]['Type'] == '224': #백색 우점혼선
                try:                
                    left_change.append((data[4]['L_LinkID'], data[4]['R_LinkID']))
                except:
                    pass

    #주행유도선 불러와서 차선 변경 WAY추가 
    lane_id_count = 100000 #새로 만드는 way ID는 200000부터 시작 
    new_lane_ways = []

    for both in both_change:
        left, right = both[0], both[1]

        for way in ways:
            if way[4]['ID'] == left:
                left_link = way[2] #way를 구성하는 노드 list를 저장
            if way[4]['ID'] == right:
                right_link = way[2] #way를 구성하는 노드 list를 저장

        left_len = len(left_link)
        right_len = len(right_link)

        #left to right way make
        if left_len < 11: #10칸의 여유를 두기 위해 11보다 작으면 패스 
            pass
        else:
            if right_len < 31:
                pass
            else:
                max_idx = min(left_len, right_len-lane_change_nodes)

                for i in range(10, max_idx, lane_change_nodes):
                    lane_id_count = check_new_id(lane_id_count, way_id_lst)

                    new_lane_ways.append(['way', -lane_id_count, [left_link[i], right_link[i+lane_change_nodes]], 3, {'Maker' : 'ARTIV_osm_formatter', 'LinkType' : 'lane_change', 'highway' : 'living_street'}])

                    lane_id_count += 1

        #right to left way make
        if right_len < 11: #10칸의 여유를 두기 위해 11보다 작으면 패스 
            pass
        else:
            if left_len < 31:
                pass
            else:
                max_idx = min(right_len, left_len-lane_change_nodes)

                for i in range(10, max_idx, lane_change_nodes):
                    lane_id_count = check_new_id(lane_id_count, way_id_lst)

                    new_lane_ways.append(['way', -lane_id_count, [right_link[i], left_link[i+lane_change_nodes]], 3, {'Maker' : 'ARTIV_osm_formatter', 'LinkType' : 'lane_change', 'highway' : 'living_street'}])

                    lane_id_count += 1


    for left_ele in left_change:
        left, right = left_ele[0], left_ele[1]

        for way in ways:
            if way[4]['ID'] == left:
                left_link = way[2] #way를 구성하는 노드 list를 저장
            if way[4]['ID'] == right:
                right_link = way[2] #way를 구성하는 노드 list를 저장

        left_len = len(left_link)
        right_len = len(right_link)

        #right to left way make
        if right_len < 11: #10칸의 여유를 두기 위해 11보다 작으면 패스 
            pass
        else:
            if left_len < 31:
                pass
            else:
                max_idx = min(right_len, left_len-lane_change_nodes)

                for i in range(10, max_idx, lane_change_nodes):
                    lane_id_count = check_new_id(lane_id_count, way_id_lst)

                    new_lane_ways.append(['way', -lane_id_count, [right_link[i], left_link[i+lane_change_nodes]], 3, {'Maker' : 'ARTIV_osm_formatter', 'LinkType' : 'lane_change', 'highway' : 'living_street'}])

                    lane_id_count += 1

    for right_ele in right_change:
        left, right = right_ele[0], right_ele[1]

        for way in ways:
            if way[4]['ID'] == left:
                left_link = way[2] #way를 구성하는 노드 list를 저장
            if way[4]['ID'] == right:
                right_link = way[2] #way를 구성하는 노드 list를 저장

        left_len = len(left_link)
        right_len = len(right_link)

        #left to right way make
        if left_len < 11: #10칸의 여유를 두기 위해 11보다 작으면 패스 
            pass
        else:
            if right_len < 31:
                pass
            else:
                max_idx = min(left_len, right_len-lane_change_nodes)

                for i in range(10, max_idx, lane_change_nodes):
                    lane_id_count = check_new_id(lane_id_count, way_id_lst)

                    #global path planning 과정에서 차선 변경 way에는 가중치를 다르게 줄 수 있도록
                    #'highway' : 'ARTIV_lane_change' 태그 추가 
                    new_lane_ways.append(['way', -lane_id_count, [left_link[i], right_link[i+lane_change_nodes]], 3, {'Maker' : 'ARTIV_osm_formatter', 'LinkType' : 'lane_change', 'highway' : 'ARTIV_lane_change'}])

                    lane_id_count += 1

    #새로 만든 lane way를 기존 way에 추가
    ways.extend(new_lane_ways)

    # OSM 작성 시작
    text = ["<?xml version='1.0' encoding='UTF-8'?>\n", "<osm version='0.6' upload='false' generator='JOSM'>\n"]

    for nd in nodes_uni:
        text.append("  <node id='{0}' lat='{1}' lon='{2}' />\n".format(int(nd[0]), nd[1], nd[2]))

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

print("All processes have ended!")
