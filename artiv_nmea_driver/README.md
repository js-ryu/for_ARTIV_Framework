artiv_nmea_driver
===============
이 패키지는 ARTIV_Framework를 위한 NMEA ROS 드라이버입니다.

[nmea_navsat_driver](http://wiki.ros.org/nmea_navsat_driver)([melodic-devel](https://github.com/ros-drivers/nmea_navsat_driver/tree/melodic-devel))를 수정하여 만들어졌으며, 원작자의 정보는 아래와 같습니다.

- Maintainer: Ed Venator <evenator AT gmail DOT com>
- Author: Eric Perko <eric AT ericperko DOT com>, Steven Martin
- License: BSD
- Source: git https://github.com/ros-drivers/nmea_navsat_driver.git (branch: melodic-devel)
---------------------------------------------------------------------------------------------
  
## Sample Usage

1. 다운받은 ```artiv_nmea_driver``` 폴더를 ```~/catkin_ws(or another catkin workspace)/src```로 옮깁니다.
2. 터미널을 여시고 ~/catkin_ws/src(or your path)/artiv_nmea_driver/scripts로 들어가셔서 chmod +x nmea_serial_driver.py로 권한을 줍니다.
3. 우리에게 너무나도 익숙한 ros1 실행, catkin_make and source devel/setup.bash!
4. ```$ roslaunch artiv_nmea_driver nmea_serial_driver.launch```

To get up and running quickly, you can use the following command to start outputting your GPS data onto ROS topics. ```nmea_serial_driver.launch``` 파일에 각종 파라미터들에 대한 기본값이 지정되어 있다. 기본값으로 당신의 GPS가 /dev/artivGPS(using symlink)에 연결되어 있고, and is communicating at 115200 baud.
  

## Published Topics
- gps_fix ([sensor_msgs/NavSatFix](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html))
  - GPS position fix reported by the device. This will be published with whatever positional and status data was available even if the device doesn't have a valid fix. Invalid fields may contain NaNs.

- gps_vel ([geometry_msgs/TwistStamped](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html))
  - Velocity output from the GPS device. Only published when the device outputs valid velocity information. The driver does not calculate the velocity based on only position fixes. 단위는 m/s.

- gps_spd ([std_msgs/Float64](http://docs.ros.org/en/melodic/api/std_msgs/html/msg/Float64.html))
  - Speed output from the GPS device. Only published when the device outputs valid speed information. 단위는 km/h.

- gps_deg ([std_msgs/Float64](http://docs.ros.org/en/melodic/api/std_msgs/html/msg/Float64.html))
  - 차량의 heading 각을 표현하였음. 단위는 deg이며, 범위는 0° to 360°이다. 북쪽 0°, 동쪽 90°, 남쪽 180°, 서쪽 270°

- gps_yaw ([std_msgs/Float64](http://docs.ros.org/en/melodic/api/std_msgs/html/msg/Float64.html))
  - 차량의 heading 각을 deg와는 다른 형태로 표현하였음. 단위는 deg이며, 범위는 -180° to 180°이다. 동쪽 0°, 북쪽 90°, 남쪽 -90°, 서쪽 180° or -180° / +x축을 기준으로 위쪽 양수, 아래쪽 음수

- utm_fix ([geometry_msgs/PoseStamped](http://docs.ros.org/en/melodic/api/geometry_msgs/html/msg/PoseStamped.html))
  - 현재 위치를 utm 좌표계로 publish. (존은 생략) 단순 x, y 좌표만 출력.
  
- time_reference ([sensor_msgs/TimeReference](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/TimeReference.html))
  - The timestamp from the GPS device is used as the time_ref.

---------------------------------------------------------------------------------------------

### Open Source Information
Software License Agreement (BSD License)

Copyright (c) 2013, Eric Perko  
All rights reserved

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
- Neither the names of the authors nor the names of their affiliated organizations may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
