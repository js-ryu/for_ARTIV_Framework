ReadMe 작성중..

블로그 글 참조

[ARTIV_OSM_FORMATTER [PART 1]](https://dgist-artiv.github.io/hdmap/2021/02/06/artiv-osm-formatter-part1.html)
[ARTIV_OSM_FORMATTER [PART 2]](https://dgist-artiv.github.io/hdmap/2021/02/09/artiv-osm-formatter-part2.html)


### USAGE

--file 혹은 -f 인자를 통해 ```<--input_link_file--> <--input_lane_file--> <--output__file_name-->```을 지정할 수 있고, --option 혹은 -o 인자를 통해 ```<--node_interval--> <--#_of_lane_change_nodes-->```을 지정할 수 있다.

기본값은 아래와 같다.
```
LINK File : "A2_LINK.osm"
LANE File : "B2_SURFACELINEMARK.osm"
Output File : "A2_LINK_output.osm"

Node Interval : 1 meter(s)
# of Lane Change Nodes : 20
```

- **사용 예시**
	- ```python3 main.py``` -> 기본값으로 실행
	- ```python3 main.py -f input.osm lane.osm``` -> LINK File : input.osm / LANE File : lane.osm / Output File : input_output.osm, 나머지는 기본값
	- ```python3 main.py --option 0.5``` -> Node Interval : 0.5미터, 나머지는 기본값
	- ```python3 main.py -f input.osm lane.osm test_out.osm -o 0.3 30``` -> LINK File : input.osm / LANE File : lane.osm / Output File : test_out.osm / Node Interval : 0.3미터, # of Lane Change Nodes : 30개

