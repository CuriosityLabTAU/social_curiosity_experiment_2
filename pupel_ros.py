import zmq
import numpy as np
import rospy
from std_msgs.msg import String
import msgpack as serializer
import sys
import json


##sudo /opt/pupil_capture/pupil_capture



class pupel_ros():
    def __init__(self,pos_data=None):

        self.current_position = 'None'
        self.current_status   = False

        #info
        if pos_data is None:
            self.pos_dict = {
                'Which': 0,
                'Howie': 1,
                'Where': 2
            }
        else:
            self.pos_dict = json.loads(pos_data)
        self.position = {0: 'left', 1: 'center', 2: 'right'}


        print self.pos_dict

        # ros:
        rospy.init_node('pupel_node')
        self.publisher_eye_tracking = rospy.Publisher('eye_tracking', String, queue_size=10)

        #start listener

        self.pupel_listener()


    def pupel_listener(self):
        ctx = zmq.Context()
        # The requester talks to Pupil remote and receives the session unique IPC SUB PORT
        requester = ctx.socket(zmq.REQ)
        ip = 'localhost'  # If you talk to a different machine use its IP.
        port = 50020  # The port defaults to 50020 but can be set in the GUI of Pupil Capture.
        requester.connect('tcp://%s:%s' % (ip, port))
        requester.send_string('SUB_PORT')
        sub_port = requester.recv_string()

        # ...continued from above
        subscriber = ctx.socket(zmq.SUB)
        subscriber.connect('tcp://%s:%s' % (ip, sub_port))
        subscriber.set(zmq.SUBSCRIBE, 'surface')  # receive all notification messages
        # subscriber.set(zmq.SUBSCRIBE, 'notify') #receive logging error messages
        # subscriber.set(zmq.SUBSCRIBE, '') #receive everything (don't do this)
        # you can setup multiple subscriber sockets
        # Sockets can be polled or read in different threads.

        # we need a serializer
        print 'pupel is on'

        while True:
            topic, payload = subscriber.recv_multipart()
            message = serializer.loads(payload)
            # print (topic,':',message)
            try:
                current_position    = message['name']
                current_status = message['gaze_on_srf'][0]['on_srf']

                if current_position != self.current_position or current_status!=self.current_status:
                    # print message['name'], ":", message['gaze_on_srf'][0]['on_srf'], type(current_status)
                    # else:
                    #     self.publisher_eye_tracking.publish('None')

                    self.current_position=current_position
                    self.current_status  =current_status

                    if current_status:
                        self.publisher_eye_tracking.publish(str(self.position[int(self.pos_dict[current_position])]))

            except:
                all



if len(sys.argv) > 1:
    start=pupel_ros(sys.argv[1])
else:
    start = pupel_ros()
