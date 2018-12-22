import numpy as np
from numpy.random import choice
import time
import rospy
from std_msgs.msg import String
import operator
import sys
from random import randint



class next_robot():
    def __init__(self):

        self.next_robot_data = {'left': 0, 'center': 0, 'right': 0}
        self.present_direction = 0
        self.position = {0: 'left', 1: 'center', 2: 'right'}
        self.position_inv = {'left': 0, 'center': 1 , 'right':2 }

        self.counter=0

        #ros:
        rospy.init_node('next_robot')

        self.publisher_next=rospy.Publisher('next_robot', String, queue_size=10)
        self.publisher_log= rospy.Publisher('log', String, queue_size=10)


        rospy.Subscriber('get_next', String, self.choose_next_robot)
        rospy.Subscriber('eye_tracking', String, self.update_next_robot)
        rospy.spin()

    def update_next_robot(self, data):

        if data != 'None':
            direction=data.data
            if direction != None:
                self.next_robot_data[direction] += 1

    def choose_next_robot(self, data):

        if data.data=='reset':
            self.next_robot_data = {'left': 0, 'center': 0, 'right': 0}
            return


        if data.data!="h":
            last_robot=int(data.data)
        else:
            last_robot="h"

        # list of counts
        robot_counts = [0, 0, 0]
        for r in self.position.keys():
            if r != last_robot:
                robot_counts[r] = self.next_robot_data[self.position[r]]

        chosen_robot = np.argmax(robot_counts)

        if chosen_robot == last_robot:
            chosen_robot = (last_robot+1) %3

        self.next_robot_data = {'left': 0, 'center': 0, 'right': 0}


        self.publisher_next.publish(str(chosen_robot))
        self.publisher_log.publish('robot_counts:'+str(robot_counts))




start=next_robot()

