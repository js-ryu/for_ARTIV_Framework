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
To get up and running quickly, you can use the following command to start outputting your GPS data onto ROS topics. ```nmea_serial_driver.launch``` 파일에 각종 파라미터들에 대한 기본값이 지정되어 있다. 기본값으로 당신의 GPS가 /dev/artivGPS(using symlink)에 연결되어 있고, and is communicating at 115200 baud.
  
```$ roslaunch artiv_nmea_driver nmea_serial_driver.launch```

## Published Topics
- gps_fix ([sensor_msgs/NavSatFix](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html))

  - GPS position fix reported by the device. This will be published with whatever positional and status data was available even if the device doesn't have a valid fix. Invalid fields may contain NaNs.

- gps_vel (geometry_msgs/TwistStamped)

  - Velocity output from the GPS device. Only published when the device outputs valid velocity information. The driver does not calculate the velocity based on only position fixes.

- gps_spd (Float64)
  - Speed output from the GPS device. Only published when the device outputs valid speed information.

- gps_deg (Float64)
  - heading

- gps_yaw (Float64)
  - heading

- utm_fix (PoseStamped)
  - 현재 위치를 utm 좌표계로 publish. (존은 생략) 단순 x, y 좌표만 출력
  
  



time_reference (sensor_msgs/TimeReference)
The timestamp from the GPS device is used as the time_ref.







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
