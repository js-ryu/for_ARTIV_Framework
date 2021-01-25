artiv_nmea_driver
===============
This package is the NMEA ROS driver for ARTIV_Framework.

It was created by modifying [nmea_navsat_driver](http://wiki.ros.org/nmea_navsat_driver)([melodic-devel](https://github.com/ros-drivers/nmea_navsat_driver/tree/melodic-devel), VER 0.5.2), and the information of the original author is as follows.

- Maintainer: Ed Venator <evenator AT gmail DOT com>
- Author: Eric Perko <eric AT ericperko DOT com>, Steven Martin
- License: BSD
- Source: git https://github.com/ros-drivers/nmea_navsat_driver.git (branch: melodic-devel)
---------------------------------------------------------------------------------------------
  
## Sample Usage

1. Move the downloaded ```artiv_nmea_driver``` folder to ```~/catkin_ws(or another catkin workspace)/src```.

2. Open a terminal and go to ``~/catkin_ws/src(or your path)/artiv_nmea_driver/scripts`` .

3. Give permission using ```chmod +x nmea_serial_driver.py```.

4. Run ROS1, ```catkin_make```, and source!

5. Executing using the launch file.  
```$ roslaunch artiv_nmea_driver nmea_serial_driver.launch```

Default values for various parameters are specified in the ```nmea_serial_driver.launch``` file. By default your GPS is connected to ```/dev/artivGPS```(using symlink), and is communicating at 115200 baud.
  
## Published Topics

- gps_fix ([sensor_msgs/NavSatFix](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html))
  - GPS position fix reported by the device. This will be published with whatever positional and status data was available even if the device doesn't have a valid fix. Invalid fields may contain NaNs.

- gps_vel ([geometry_msgs/TwistStamped](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html))
  - Velocity output from the GPS device. Only published when the device outputs valid velocity information. The driver does not calculate the velocity based on only position fixes. The unit is m/s.

- gps_spd ([std_msgs/Float64](http://docs.ros.org/en/melodic/api/std_msgs/html/msg/Float64.html))
  - Speed output from the GPS device. Only published when the device outputs valid speed information. The unit is km/h.

- gps_deg ([std_msgs/Float64](http://docs.ros.org/en/melodic/api/std_msgs/html/msg/Float64.html))
  - Expressed the vehicle's heading angle. The unit is deg, and the range is 0° to 360°. 0° is north, 90° is east, 180° is south, and 270° is west.

- gps_yaw ([std_msgs/Float64](http://docs.ros.org/en/melodic/api/std_msgs/html/msg/Float64.html))
  - The heading angle of the vehicle is expressed in a different form than ```gps_deg```(for path tracking part). The unit is deg, and the range is -180° to 180°. 0° is east, 90° is north, -90° is south, and 180° or -180° are west. The upper part is positive and the lower part is negative based on the +x axis.

- utm_fix ([geometry_msgs/PoseStamped](http://docs.ros.org/en/melodic/api/geometry_msgs/html/msg/PoseStamped.html))
  - Present location in UTM coordinate system. The UTM zone is omitted and only the x and y coordinates are expressed.
    
- time_reference ([sensor_msgs/TimeReference](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/TimeReference.html))
  - The timestamp from the GPS device is used as the time_ref.

## Error Types
In accordance with the operating conditions of the warning device in the ARTIV_Framework, the following type of error is output.

- Type 1(Fatal) : Invaild Checksum, Device Connection Fail
- Type 2(Error) : Value Error, HDOP exceeds 3, RTK is not Fixed

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
