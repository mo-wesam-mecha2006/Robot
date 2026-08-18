import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist #this is used to import Twist is a standard ROS2 message type used to describe velocity commands.
from turtlesim.msg import Color  #Color is a message type specific to the turtlesim package . that has has three fields: r, g, b — each a uint8 (0–255), representing the color of the background the turtle is currently over.
from std_msgs.msg import String #this makes the string messages easier to be print later 

import sys #gives access to system-level things, here specifically sys.stdin (the keyboard input stream).
import termios #lets you read/change terminal settings (like whether it waits for Enter or not).
import tty #a helper that makes switching to "raw mode" one line instead of many.
import select #lets you check "is there data waiting to be read?" without actually blocking to wait for it.


class RobotTrialNode(Node):
    def __init__(self):
        super().__init__('robot_trial_node')


        self.declare_parameter("cmd_vel_topic",'/turtle1/cmd_vel')
        self.declare_parameter('color_sensor_topic', '/turtle1/color_sensor')
        self.declare_parameter('dominant_color_topic', '/dominant_color')

        cmd_vel_topic = self.get_parameter('cmd_vel_topic').get_parameter_value().string_value
        color_sensor_topic = self.get_parameter('color_sensor_topic').get_parameter_value().string_value
        dominant_color_topic = self.get_parameter('dominant_color_topic').get_parameter_value().string_value


        self.cmd_vel_pub = self.create_publisher(Twist, cmd_vel_topic, 10)
        self.color_sub = self.create_subscription(Color, color_sensor_topic, self.color_callback, 10)
        self.dominant_pub = self.create_publisher(String, dominant_color_topic, 10)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
      key = self.get_key()
      msg = Twist()

      if key == 'w':
        msg.linear.x = 2.0
      elif key == 's':
        msg.linear.x = -2.0
      elif key == 'a':
        msg.angular.z = 2.0
      elif key == 'd':
        msg.angular.z = -2.0
      else:
        return  # no key pressed, don't publish

      self.cmd_vel_pub.publish(msg)

    def color_callback(self,msg):
       r, g, b = msg.r, msg.g, msg.b


       # here will difine with color is dominant 
       if r >= g and r >= b:
        major_color = "Red"
       elif g >= r and g >= b:
        major_color = "Green"
       else:
        major_color = "Blue"

       # Action 1: log it
       self.get_logger().info(f"Major color: {major_color} (r={r}, g={g}, b={b})")

       # Action 2: publish it
       out_msg = String()
       out_msg.data = major_color
       self.dominant_pub.publish(out_msg)
       
    def get_key(self):
      fd = sys.stdin.fileno() #takes the input from the keyboard and .fileno() gets its underlying file descriptor — a low-level integer handle the OS uses to identify that input stream. You need this because termios functions work with file descriptors, not Python objects.
      old_settings = termios.tcgetattr(fd) # this line save the old terimnal setting to restore it after you finish the program 
      try:
        tty.setraw(fd)
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)      #select.select(read_list, write_list, error_list, timeout) — you're only checking readability, so the other two lists are empty [].
        if rlist:
            key = sys.stdin.read(1)   #This is the piece that makes it non-blocking — without it, sys.stdin.read(1) would just freeze the program until someone pressed something.
        else:
            key = ''
      finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)#Regardless of what happened above (success or error), this restores the terminal back to its original saved settings — turning off raw mode so your terminal behaves normally again afterward.
        return key        # return the key wether it's (w s d a) or nothing 


def main(args=None):
    rclpy.init(args=args)
    node = RobotTrialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



    