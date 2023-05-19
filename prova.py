import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from time import sleep

positions = [
    [0.0,0.5],
    [0.5,0.0],
    [0.0,0.5],   
    [0.5,0.0],
    [1.0,0.0],
    [0.0,1.0]
]
positions_volta = [
    [5.54, 5.54]
]

dist_segura = 0.1
vel = 0.5

class GazeboRoda(Node):
    def __init__(self):
        super().__init__("Vai Teia")
        self.cmd_vel_publish = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.odom2 = self.create_subscription(Pose, "/turtle1/pose", self.prova, 10)
        self.get_logger().info("rodano")
    

    def prova(self, pose:Pose): 
        pos_atual = 0
        x = pose.x
        y = pose.y
        soma_x = 0
        soma_y = 0
        delta_y = 0.5
        delta_x = 0.5


        vel_msg = Twist()

        for i in range(0, len(positions_volta)):
            soma_x += positions_volta[i][0]
            soma_y += positions_volta[i][0]
        
        if abs(delta_y + soma_y - y) > dist_segura:
            vel_msg.linear.x = 0.0
            vel_msg.linear.y = vel
        elif abs(delta_x + soma_x - x) > dist_segura:
            vel_msg.linear.x = vel
            vel_msg.linear.y = 0.0
        else:
            vel_msg.linear.x = 0.0
            vel_msg.linear.y = 0.0
            
            positions_volta.append(positions[0])
            positions.pop(0)
            pos_atual+=1
            delta_x += positions[0][0]
            delta_x += positions[0][1]
            
        
        self.cmd_vel_publish.publish(vel_msg)
        self.get_logger().info(f"x={round(x, 2)},y={round(y, 2)}")

def main(args=None):
    rclpy.init(args=args)
    node = GazeboRoda()
    rclpy.spin(node)
    rclpy.shutdown