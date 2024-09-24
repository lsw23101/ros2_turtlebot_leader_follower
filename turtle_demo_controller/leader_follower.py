#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

# turtle1의 위치를 받아와 turtle2의 선속도와 각속도를 제어할 예정

class Controller_Node(Node):
    def __init__(self):
        super().__init__('turt_controller')
        self.get_logger().info("Node Started")
        

        # 터틀봇의 처음 위치는 turtle1:(5,5)  turtle2:(2,2)
        self.target_x = 2.0  # Adjust as needed
        self.target_y = 2.0  # Adjust as needed

        # Publisher and Subscriber        
        # sub은 터틀1의 위치를 받아오고, 또 자신인 터틀2의 pose를 받아올 sub도 필요
        # pub은 터틀2의 속도를 퍼블리쉬

        # 얘는 목표 포지션을 받아와서 멤버변수로 저장하고 끝
        self.target_pose_sub = self.create_subscription(Pose, "/turtle1/pose", self.target_pose_callback, 10)
        # 얘가 기존 제어하는 콜백함수
        self.my_pose_sub = self.create_subscription(Pose, "/turtle2/pose", self.my_pose_callback, 10)
        self.my_vel_command = self.create_publisher(Twist, "/turtle2/cmd_vel", 10)

    def target_pose_callback(self, msg: Pose):
        self.get_logger().info(f"가야하는 곳=({msg.x},{msg.y})")
        self.target_x = msg.x
        self.target_y = msg.y 

    def my_pose_callback(self, msg: Pose):
        self.get_logger().info(f"Current x={msg.x} current y={msg.y} and current angle = {msg.theta}")
        # Calculate errors in position
        err_x = self.target_x - msg.x
        err_y = self.target_y - msg.y 
        err_dist = (err_x**2+err_y**2)**0.5
        
        # Distance error (magnitude of the error vector)
        
        self.get_logger().info(f"Error in x {err_x} and error in y {err_y}")

        # Desired heading based on the position error
        desired_theta = math.atan2(err_y, err_x)
        
        # Error in heading
        err_theta = desired_theta - msg.theta
       
        # Handle wrap-around issues (e.g., if error jumps from +pi to -pi) # 각도의 범위를 +-파이로 조정
        while err_theta > math.pi:
            err_theta -= 2.0 * math.pi
        while err_theta < -math.pi:
            err_theta += 2.0 * math.pi
        
        self.get_logger().info(f"Desired Angle = {desired_theta} current angle {msg.theta} Error angle {err_theta}")
        # P (ID not required) for linear velocity (distance control)

        Kp_dist = 0.9
            
        # P (ID not required) constants for angular velocity (heading control)
        Kp_theta = 2
        

        # TODO: Add integral and derivative calculations for complete PID

        # PID control for linear velocity
        #l_v = Kp_dist * abs(err_x) # + Ki_dist * integral_dist + Kd_dist * derivative_dist
        if err_dist < 1.0:
            l_v = 0.0  # 너무 가까우면 선속도를 0으로
        else:
            l_v = Kp_dist * err_dist # + Ki_dist * integral_dist + Kd_dist * derivative_dist

        # PID control for angular velocity
        a_v = Kp_theta * err_theta  

        # Send the velocities
        self.my_velocity_cont(l_v, a_v)


    def my_velocity_cont(self, l_v, a_v):
        self.get_logger().info(f"Commanding liner ={l_v} and angular ={a_v}")
        my_msg = Twist()
        my_msg.linear.x = l_v
        my_msg.angular.z = a_v
        self.my_vel_command.publish(my_msg)

def main(args=None):
    rclpy.init(args=args)
    pid_control = Controller_Node()
    rclpy.spin(pid_control)
    pid_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
