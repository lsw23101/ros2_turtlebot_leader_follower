from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # 첫 번째 터틀심 노드를 실행
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim1',
            output='screen'
        ),
        # 두 번째 터틀봇 생성
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', 
                 '{"x": 2.0, "y": 2.0, "theta": 0.0, "name": "turtle2"}'],
            output='screen'
        ),
        # 첫 번째 터틀의 색깔 변경
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/turtle1/set_pen', 'turtlesim/srv/SetPen', 
                 '{"r": 255, "g": 0, "b": 0, "width": 2, "off": 0}'],  # 빨간색
            output='screen'
        ),
        # 두 번째 터틀의 색깔 변경
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/turtle2/set_pen', 'turtlesim/srv/SetPen', 
                 '{"r": 0, "g": 0, "b": 255, "width": 2, "off": 0}'],  # 파란색
            output='screen'
        ),
    ])
