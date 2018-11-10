import numpy as np
import time
import rospy
from std_msgs.msg import String
import operator
import sys
import json
import random
import pandas as pd
from numpy.random import choice

# class dynamics():
#     def __init__(self):
#         rospy.init_node('test2')
#
#         self.publisher_alive = rospy.Publisher('test', String, queue_size=10)
#
#
#
#
#         rospy.Subscriber('tablet_game', String, self.update_current_answer)
#
#         rospy.spin()
#
#
#     def update_current_answer(self,data):
#         if data.data=='1':
#             self.publisher_alive.publish('123')
#
#
#
# # a=dynamics()
# #
# # a=dynamics()
# import json
# cinfig_hist_data={'nao_ip_experimenter':'192.168.0.101','nao_ip_left':'192.168.0.104','nao_ip_right':'192.168.0.102','nao_ip_center':'192.168.0.103','nao_name_left':'Howie','nao_name_right':'Where','nao_name_center':'Which'}
# # try:
# #     with open('cinfig_hist_data.json') as data_file:
# #         cinfig_hist_data = json.load(data_file)
# # except:
# #     'IOError'
# #     cinfig_hist_data = {'nao_ip_experimenter':'192.168.0.', 'nao_ip_left': '192.168.0.', 'nao_ip_right': '192.168.0.', 'nao_ip_center': '192.168.0.',
# #                         'nao_name_left': 'Howie', 'nao_name_right': 'Which', 'nao_name_center': 'Where'}
# #
# # print cinfig_hist_data['nao_ip_experimenter']
#
#
# with open('cinfig_hist_data.json', 'w') as outfile:
#     json.dump(cinfig_hist_data, outfile)
from random import randint

print (randint(1, 4))