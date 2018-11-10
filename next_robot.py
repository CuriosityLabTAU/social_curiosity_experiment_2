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

        # print('update:', self.next_robot_data)

        # else:
        #     direction = 'None'
        #
        # if self.present_direction==0:
        #     if direction== 'None':
        #         return
        #     else:
        #         self.next_robot_data[direction].append(time.time())
        #         self.present_direction=direction
        #
        # else:
        #     self.next_robot_data[self.present_direction][-1] -= time.time()
        #
        #     if direction== 'None':
        #         self.present_direction = 0
        #
        #     else:
        #         self.next_robot_data[direction].append(time.time())
        #         self.present_direction = direction



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

        # # self.update_next_robot() #finish counting the time
        #
        # #agregat data
        # next_robot_sum=[[],[],[]]
        # for v in list(self.next_robot_data):
        #     self.next_robot_data[v] = -1 * sum(self.next_robot_data[v])
        #     next_robot_sum[self.position_inv[v]]=self.next_robot_data[v]
        #
        # if np.std(self.next_robot_data.values()) < 1:
        #     # if there is no significant one -choose randomly
        #     robots = [0, 1, 2]
        #
        #     if last_robot !="h":
        #         robots.remove(last_robot)
        #
        #
        #     robot_number = choice(robots)
        #
        #     chosen_robot = robot_number
        #
        # else:
        #     if last_robot!="h":
        #         next_robot_sum[last_robot]=0
        #
        #     chosen_robot=np.argmax(next_robot_sum)

        #restart next_robot_data
        self.next_robot_data = {'left': 0, 'center': 0, 'right': 0}

        # print 'next_robot:-=----',next_robot
        # next_robot=str(randint(0, 3))
        # if next_robot=='3':
        #     next_robot='h'
        # print 'mext robot```````````````````:', next_robot
        # if self.counter % 4==0:
        #     chosen_robot='h'
        # self.counter+=1

        self.publisher_next.publish(str(chosen_robot))
        self.publisher_log.publish('robot_counts:'+str(robot_counts))
        # return self.position.keys()[self.position.values().index(chosen_robot)]



start=next_robot()

