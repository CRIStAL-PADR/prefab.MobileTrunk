# coding: utf8
#!/usr/bin/env python3
import Sofa
from splib3.numerics import RigidDof, Quat
from splib3.animation import animate
from splib3.constants import Key
from stlib3.scene import Scene
from math import *


def recv(data, datafield):
    t = data.tolist()
    datafield[0].value = [t[0], t[1], t[2]]
    datafield[1].value = [t[3], t[4], t[5]]

class SummitxlROSController(Sofa.Core.Controller):
    """A Simple keyboard controller for the SummitXL
       Key UP, DOWN, LEFT, RIGHT to move
    """
    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, *args, **kwargs)
        self.robot = kwargs["robot"]
        self.robot.linear_vel[0] = 0
        self.robot.angular_vel[2] = 0
        self.dt = 0
        self.wheel_ray = 0.0015

    def move(self, fwd, angle):
        """Move the robot using the forward speed and angular speed)"""
        robot = RigidDof(self.robot.Chassis.position)
        robot.translate(robot.forward * fwd)
        robot.rotateAround([0, 1, 0], angle)

        with self.robot.Chassis.WheelsMotors.angles.position.writeable() as angles:
            #Make the wheel turn according to forward speed
            # TODO: All the value are random, need to be really calculated
            angles += (fwd/self.wheel_ray)

            #Make the wheel turn in reverse mode according to turning speed
            # TODO: the value are random, need to be really calculated
            angles[0] += (angle)
            angles[2] += (angle)
            angles[1] -= (angle)
            angles[3] -= (angle)

    def onAnimateBeginEvent(self, event):
        """At each time step we move the robot by the given forward_speed and angular_speed)
           TODO: normalize the speed by the dt so it is a real speed
        """
        self.dt = event['dt']
        self.robot.linear_vel[0] = self.robot.linear_vel[0]*self.dt
        self.robot.angular_vel[2] = self.robot.angular_vel[2] * self.dt
        self.move(self.robot.linear_vel[0], self.robot.angular_vel[2])
