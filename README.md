# turtlebot_encrypted_control

# git pull, push 하는법,,,
https://shortcuts.tistory.com/8

# install
```
$ mkdir my_ws/src  
$ cd ~/my_ws/src  
$ git clone https://github.com/Nicoala231/turtlebot_encrypted_control/
```
git pull을 하면 폴더가 생성 x
# Requirement
ros2 (현:foxy)
turtlesim package

# Usage
1. 배쉬 실행
```
rosfoxy / source ./install/setup.bash
```

2. 터틀봇 두개 소환하는 런치 파일 실행  
```
ros2 launch turtle_demo_controller two_turtle.launch.py
```

3. 터틀봇1을 움직일 노드파일 실행
new terminal:  
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap /cmd_vel:=/turtle1/cmd_vel
```

5. leader-follower 노드 실행
new terminal:  
```
ros2 run turtle_demo_controller leader_follower
```

# ToDo
- publisher subcriber 나눠서 plant contoller 파트 나누기
- 암호 적용하기
- 


# Reference

https://github.com/roboticvedant/ROS2_turtlesim_PID_demo
