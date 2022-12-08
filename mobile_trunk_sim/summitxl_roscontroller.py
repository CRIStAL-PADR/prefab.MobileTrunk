# coding: utf8
#!/usr/bin/env python3
import numpy as np
from turtle import distance
import Sofa
from splib3.numerics import RigidDof
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from wheels_angles_compute import twistToWheelsAngularSpeed, move
import time
from math import *
import queue


q = queue.Queue()

def send(data):
    """This is a message to hold data from an IMU (Inertial Measurement Unit)

    Accelerations should be in m/s^2
    and rotational velocity should be in rad/sec


    Args:
        data[0]: Orientation
        data[1] : angular_vel
        data[2] : linear_acceleration

    Returns:
        msg: return  data as ros msg
    """
    msg = Imu()
    msg.orientation.x = data[0].value[0]
    msg.orientation.y = data[0].value[1]
    msg.orientation.z = data[0].value[2]
    msg.orientation.w = data[0].value[3]

    msg.angular_velocity.x = data[1].value[0]
    msg.angular_velocity.y = data[1].value[1]
    msg.angular_velocity.z = data[1].value[2]

    msg.linear_acceleration.x = data[2].value[0]
    msg.linear_acceleration.y = data[2].value[1]
    msg.linear_acceleration.z= data[2].value[2]

    msg.header.stamp.sec =  int(data[3].value[0])
    msg.header.stamp.nanosec = int(data[3].value[1])

    return msg

def vel_send(data):
    """ Returns the velocity of
        the robot in the simulation
    Args:
        data (list): list containing the fields and values of the velocity of the
                     robot in simulation

    Returns:
            Objet de type geometry_msgs.msg.Twist
    """
    msg = Twist()
    msg.linear.x = data[0].value[0]
    msg.linear.y = data[0].value[1]
    msg.linear.z = data[0].value[2]

    msg.angular.x = data[1].value[0]
    msg.angular.y = data[1].value[1]
    msg.angular.z = data[1].value[2]
    return msg

def vel_recv(data, datafield):
    """Function called by the RosReceiver. It
        allows to recover the velocity fields of the
        real robot

    Args:
        data (geometry_msgs.msg.Twist): Real robot velocity data
        datafield (_type_): Data allowing to store the real robot
                                velocity
    """
    datafield[0].value = [data.linear.x ,data.linear.y, data.linear.z]
    datafield[1].value = [data.angular.x ,data.angular.z, data.angular.y]

def odom_recv(data, datafield):
    """ Function called by the RosReceiver. It
        allows to recover the odometry fields of the
        real robot

    Args:
        data (nav_msgs.msg.Odometry): Real robot odometer data
        datafield (nav_msgs.msg.Odometry): Data allowing to store the
                              odometery of the real robot.
                              Is used by the roscontroller
    sim_position = [x , y , z]   avec y = 0.0
    reel_position = [x, y, z]    avec z = 0.
    => sim_position = [reel_position.y ,reel_position.z, reel_position.x]

    sim_orientation = [ x, y, z, w] with  x = 0. and z = 0.
    reel_orientation = [x, y, z, w] with  x = 0. and y = 0.
    => sim_orientation = [reel_orientation.x, reel_orientation.z, reel_orientation.y,
                            reel_orientation.w]
    """
    datafield[0].value = [data.header.stamp.sec ,data.header.stamp.nanosec]
    datafield[1].value = [data.pose.pose.position.y,data.pose.pose.position.z,
                          data.pose.pose.position.x]

    datafield[2].value = [data.pose.pose.orientation.x,data.pose.pose.orientation.z,
                          data.pose.pose.orientation.y,data.pose.pose.orientation.w ]
    datafield[3].value = [data.twist.twist.linear.x, 0 ,0]
    datafield[4].value = [0, 0, data.twist.twist.angular.z]


def position_and_orientation_send(data):
    msg = Odometry()
    #odom position x y z
    msg.pose.pose.position.x = data[0].value[0]/1000
    msg.pose.pose.position.z = data[0].value[2]/1000
    msg.pose.pose.position.y = data[0].value[1]/1000

    #odom orientation x y z w
    msg.pose.pose.orientation.x = data[1].value[0]
    msg.pose.pose.orientation.z = data[1].value[1]
    msg.pose.pose.orientation.y = data[1].value[2]
    msg.pose.pose.orientation.w = data[1].value[3]
    #print(msg.pose.pose.position)
    return msg
    
def odom_send(data):
    """ Returns the odometry of
        the robot in the simulation
    Args:
        data (list): list containing the fields and values of the odometry of the
                     robot in simulation

    Returns:
            Objet de type nav_msgs.msg.Odometry
    """
    msg = Odometry()
    msg.header.stamp.sec = int(data[0].value[0])
    msg.header.stamp.nanosec = int(data[0].value[1])

    #odom position x y z
    msg.pose.pose.position.x = data[1].value[2]
    msg.pose.pose.position.z = data[1].value[1]
    msg.pose.pose.position.y = data[1].value[0]

    #odom orientation x y z w
    msg.pose.pose.orientation.x = data[2].value[0]
    msg.pose.pose.orientation.z = data[2].value[1]
    msg.pose.pose.orientation.y = data[2].value[2]
    msg.pose.pose.orientation.w = data[2].value[3]

    #odom linear & angular vel
    #linear vel
    msg.twist.twist.linear.x = data[3].value[0]
    msg.twist.twist.linear.y = data[3].value[1]
    msg.twist.twist.linear.z = data[3].value[2]

    #angular vel
    msg.twist.twist.angular.x = data[4].value[0]
    msg.twist.twist.angular.y = data[4].value[1]
    msg.twist.twist.angular.z = data[4].value[2]
    return msg

class SummitxlROSController(Sofa.Core.Controller):
    """A Simple keyboard controller for the SummitXL
       Key UP, DOWN, LEFT, RIGHT to move
    """
    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, *args, **kwargs)
        self.robot = kwargs["robot"]
        self.robotToSim = kwargs["robotToSim"]
        self.flag = True
        # self.robot.robot_linear_x = 0.
        # self.robot.robot_angular_z  = 0.
        self.time_now = None
        #self.time_s = None
        self.time_s = time.time()
        self.positon_inital=[self.robot.Chassis.Base.position.position.value[0][0],
                            self.robot.Chassis.Base.position.position.value[0][1],
                            self.robot.Chassis.Base.position.position.value[0][2]]
        self.dt = 0
        self.sofa_time = 0
        self.robot_time = 0
        self.timeToSpeed =  {}
        self.angular_speed = 0
        self.linear_speed = 0

    def init_pose(self):
        """
            Allows to initialize the position of the simulation
            robot in sofa_ using the position of the real robot
        """

        if self.flag:
            
            with self.robot.Chassis.Base.position.position.writeable() as summit_pose:
                #position x, y z

                summit_pose[0][0] = self.robot.reel_position[0]
                summit_pose[0][1] = self.robot.reel_position[1]
                summit_pose[0][2] = self.robot.reel_position[2]

                #orientaion x y z w
                summit_pose[0][3] = self.robot.reel_orientation[0]
                summit_pose[0][4] = self.robot.reel_orientation[1]
                summit_pose[0][5] = self.robot.reel_orientation[2]
                summit_pose[0][6] = self.robot.reel_orientation[3]
            self.flag = False
            print("init summit_xl pose")


    def onAnimateBeginEvent(self, event):
        """ At each time step we move the robot by the given
            forward_speed and angular_speed)
        """
        if self.robotToSim:
            if self.time_now is not None:
                t = float(self.robot.timestamp.value[0])+float(self.robot.timestamp.value[1])/1000000000  - self.time_now
                self.time_now = float(self.robot.timestamp.value[0])+float(self.robot.timestamp.value[1])/1000000000
               #######################"
                if t > 100:
                    t = 0
                else:
                    dt = event['dt']
                    self.sofa_time +=dt
                    self.robot_time +=t
                    # print("self.robot_time = ", self.robot_time, "----->", self.robot.robot_angular_vel[2], self.robot.robot_linear_vel[0],
                    #                         "||||","self.sofa_time = ", self.sofa_time )
                    #print(round(self.sofa_time, 2), round(self.robot_time,2))
                    #print(self.sofa_time, " ---------", t)
                    q.put([self.robot_time, self.robot.robot_angular_vel[2], self.robot.robot_linear_vel[0], t])
                    self.timeToSpeed.update({round(self.robot_time, 2):(t, self.robot.robot_angular_vel[2], self.robot.robot_linear_vel[0])})    
            else:
                t=0
                self.time_now = float(self.robot.timestamp.value[0])+float(self.robot.timestamp.value[1])/1000000000

        if not self.robotToSim:
            self.time_s = time.time()
            if self.time_now is not None:
                dt = self.time_s - self.time_now
                self.time_now = time.time()
            else:
                dt = 0
                self.time_now = time.time()
            robot_time = self.time_s
            with self.robot.timestamp.writeable() as t:
                t[0] = int(robot_time)
                t[1] = 0
     
        for i in range(0,4):
            self.robot.sim_orientation[i] = self.robot.Chassis.Base.position.position.value[0][3+i]

        for i in range(0,3):
            self.robot.sim_position[i] = self.robot.Chassis.Base.position.position.value[0][i]

    
        if not self.flag and not q.empty():
            if q.queue[0][0] - self.sofa_time <= 0.001:
                item = q.get()
                if self.sofa_time <= item[0] :
                    print(item[0]-self.sofa_time, '     ', self.sofa_time, '   ', item[0] )
                    self.angular_speed = item[1]
                    self.linear_speed = item[2]
                    wheels_angular_speed = twistToWheelsAngularSpeed(self.angular_speed,
                                                                self.linear_speed)
                    move(self.robot.Chassis.WheelsMotors.angles.rest_position, wheels_angular_speed, item[3])
        # Wait to start receiving data from ROS to initialize the position
        # of the robot in the simulation with the position of the real robot
        if self.robot.reel_position[0] != 0:
            self.init_pose()