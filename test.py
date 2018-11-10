import rospy
from std_msgs.msg import String
from naoqi import ALProxy
import sys
import random
import time
import json
import threading



class NaoNode():

    def __init__(self, _robot_ip=str,_node_name=str):
        self.port = 9559
        self.robot_ip=_robot_ip
        self.node_name=_node_name

        #motionProxy
        self.motionProxy  = ALProxy("ALMotion", self.robot_ip, self.port)

        # postureProxy
        self.postureProxy = ALProxy("ALRobotPosture", self.robot_ip, self.port)

        # animatedSpeech
        self.animatedSpeech = ALProxy("ALAnimatedSpeech", self.robot_ip, self.port)

        # managerProxy
        self.managerProxy = ALProxy("ALBehaviorManager", self.robot_ip, self.port)

        #texttospeech
        self.tts = ALProxy("ALTextToSpeech", self.robot_ip, self.port)

        #trackerProxy
        self.trackerProxy = ALProxy("ALTracker", self.robot_ip, self.port)

        #AutonomousLife
        self.autonomous = ALProxy("ALAutonomousLife", self.robot_ip, self.port)

        # PostureProxy
        self.postureProxy = ALProxy("ALRobotPosture", self.robot_ip, 9559)

        # PostureProxy
        self.systemProxy = ALProxy("ALSystem", self.robot_ip, 9559)

        self.tts.setParameter("speed", 85)
        #LEDS Api:

        self.leds = ALProxy("ALLeds", self.robot_ip, self.port)
        names1 = ["FaceLed0", "FaceLed4"]
        names2 = ["FaceLed1", "FaceLed3", "FaceLed5", "FaceLed7"]
        names3 = ["FaceLed2", "FaceLed6"]
        names4 = ["ChestLeds"]


        self.leds.createGroup("leds1", names1)
        self.leds.createGroup("leds3", names3)
        self.leds.createGroup("leds2", names2)
        self.leds.createGroup("leds4", names4)






        # wake_up
        self.wake_up()




    def parse_behavior(self, _dict):
        return json.dumps(_dict)

    def parse_message(self, message):
        # message is json string in the form of:  {'action': 'run_behavior', 'parameters': ["movements/introduction_all_0",...]}
        # eval the action and run with parameters.
        # For example, eval result could look like: self,say_text_to_speech(['hello','how are you?'])
        message = str(message.data)

        # message = str(message)  #FOR TEST!!!!!!!!!!


        message_dict = json.loads(message)


        action = str(message_dict['action'])
        if 'parameters' in message_dict:
            parameters = message_dict['parameters']
        else:
            parameters = ""
        # print(str("self." + action + "('" + str(parameters) + "')"))
        eval(str("self." + action + "(" + str(parameters) + ")"))

    def run_behavior(self, parameters):
        ''' run a behavior installed on nao. parameters is a behavior. For example "movements/introduction_all_0" '''
        try:
            behavior = str(parameters[0])
            if len(parameters) > 1:
                if parameters[1] == 'wait':
                    self.managerProxy.runBehavior(behavior)

                else:
                    self.managerProxy.post.runBehavior(behavior)
            else:
                self.managerProxy.post.runBehavior(behavior)

            self.back_to_live()

        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e



    def say_text_to_speech (self, parameters):
        # make nao say the string text
        # parameters in the form of ['say something','say something','say something']
        for text in parameters:
            print("say_text_to_speech", text)
            self.tts.say (str(text))

    def set_autonomous_state_off(self):
        # put nao in autonomous state
        # parameters in the form of ['solitary','disabled']
        # http://doc.aldebaran.com/2-1/naoqi/core/autonomouslife.html
        self.autonomous.setState('disabled')

    def rest(self):
        self.motionProxy.rest()

    def wake_up(self):
        self.motionProxy.wakeUp()

    def open_hand(self, parameters):
        print('open_hand', parameters)
        hand_name = parameters[0]
        self.motionProxy.openHand('RHand')

    def look_at(self, parameters):
        vect2 = parameters[0]
        fractionmaxspeed = parameters[1]
        use = parameters[2]
        self.trackerProxy.lookAt(vect2, fractionmaxspeed, use)

    def point_at(self,parameters):
        print('pointAt', parameters)
        effector = 'RArm'
        vect = parameters[0]
        fractionmaxspeed = parameters[1]
        use = parameters[2]
        self.trackerProxy.pointAt(effector, vect, fractionmaxspeed, use)

    def change_pose(self, data_str):
        # data_str = 'name1, name2;target1, target2;pMaxSpeedFraction'
        # print data_str
        info = data_str.split(';')
        pNames = info[0].split(',')
        pTargetAngles = [float(x) for x in info[1].split(',')]
        # pTargetAngles = [x * almath.TO_RAD for x in pTargetAngles]  # Convert to radians
        pMaxSpeedFraction = float(info[2])
        # print(pNames, pTargetAngles, pMaxSpeedFraction)
        self.motionProxy.post.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)
        self.back_to_live()

    def change_pose_util(self, data_str):
        # data_str = 'name1, name2;target1, target2;pMaxSpeedFraction'
        # print data_str
        info = data_str.split(';')
        pNames = info[0].split(',')
        pTargetAngles = [float(x) for x in info[1].split(',')]
        # pTargetAngles = [x * almath.TO_RAD for x in pTargetAngles]  # Convert to radians
        pMaxSpeedFraction = float(info[2])
        # print(pNames, pTargetAngles, pMaxSpeedFraction)
        self.motionProxy.post.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)

    def animated_speech(self,parameters):
        # make nao say the string text
        # parameters in the form of ['say something',pitchShift=float]
        text=str(parameters)
        # pitch=parameters[1]
        print("say_text_to_animated_speech", text)
        self.animatedSpeech.say(text, {"pitchShift": 1.0})

    def get_angles(self,parameters):
        caller=self.node_name+','+parameters
        names = "Body"
        use_sensors = False
        print("get_angles")
        use_sensors = True
        # string_to_pub = json.dumps([[caller], self.motionProxy.getAngles(names, use_sensors),self.motionProxy.getBodyNames(names)])
        string_to_pub = json.dumps([[caller],self.motionProxy.getAngles(names, use_sensors)])
        print string_to_pub
        self.publisher.publish(string_to_pub)


    def move_to_pose(self,direction):
        direction=direction[0]

        if direction == 'right':
            self.change_pose_util('HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;-0.88,0.01,0.93,0.26,-0.45,-1.2,0.01,0.29,-0.6,0.2,-1.53,1.41,0.84,0.0,-0.6,0.0,-1.53,1.41,0.85,0.01,0.96,-0.29,0.53,1.26,-0.05,0.3;0.2')

        elif direction == 'center':
            self.change_pose_util('HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;-0.02,0.2,0.93,0.26,-0.45,-1.21,0.01,0.29,-0.6,0.2,-1.53,1.41,0.84,-0.0,-0.6,-0.2,-1.53,1.41,0.85,0.01,0.96,-0.3,0.53,1.24,-0.04,0.3;0.08')

        elif direction == 'left':
            self.change_pose_util('HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;0.88,0.01,0.92,0.27,-0.47,-1.22,0.01,0.29,-0.6,0.0,-1.53,1.41,0.84,0.0,-0.6,-0.2,-1.53,1.41,0.85,0.01,0.96,-0.3,0.53,1.24,-0.04,0.3;0.2')

        self.back_to_live()

    def look_to_other_way(self,relative_to):
        relative_to=relative_to[0]


        angles=self.motionProxy.getAngles("Body", True)
        basepose_HeadYaw = angles[0]
        basepose_HeadPitch = angles[1]

        if relative_to == "right":
            self.change_pose_util('HeadYaw,HeadPitch;' + str(basepose_HeadYaw + 1.18) + ',' + str(basepose_HeadPitch - 0.2) + ';0.08')
        elif relative_to == "center":
            sign = random.choice((-1, 1))
            self.change_pose_util('HeadYaw,HeadPitch;' + str(basepose_HeadYaw + sign * (0.4)) + ',' + str(basepose_HeadPitch + 0.2) + ';0.08')
        elif relative_to == "left":
            self.change_pose_util('HeadYaw,HeadPitch;' + str(basepose_HeadYaw - 1.18) + ',' + str(basepose_HeadPitch - 0.2) + ';0.08')

        self.back_to_live()

    def agree(self):
        counter = 0
        angles=self.motionProxy.getAngles("Body", True)
        basepose = angles[1]
        while counter < 3:
            self.change_pose_util('HeadPitch;' + str(basepose + 0.2) + ';0.08')
            time.sleep(0.5)
            self.change_pose_util('HeadPitch;' + str(basepose - 0.2) + ';0.08')
            time.sleep(0.5)
            self.change_pose_util('HeadPitch;' + str(basepose) + ';0.08')
            counter += 1

        self.back_to_live()


    def look_down(self):
        angles = self.motionProxy.getAngles("Body", True)
        basepose = angles[1]
        self.change_pose_util('HeadPitch;' + str(basepose + 0.2) + ';0.08')
        time.sleep(3)
        self.change_pose_util('HeadPitch;' + str(basepose) + ';0.08')

        self.back_to_live()

    def look_up(self):
        angles = self.motionProxy.getAngles("Body", True)
        basepose = angles[1]
        self.change_pose_util('HeadPitch;' + str(basepose - 0.4) + ';0.08')
        time.sleep(6)
        self.change_pose_util('HeadPitch;' + str(basepose) + ';0.08')

        self.back_to_live()


    def disagree(self):
        counter = 0
        angles=self.motionProxy.getAngles("Body", True)
        basepose = angles[0]
        print basepose
        while counter < 3:
            self.change_pose_util('HeadYaw;' + str(basepose + 0.2) + ';0.08')
            time.sleep(0.5)
            self.change_pose_util('HeadYaw;' + str(basepose - 0.2) + ';0.08')
            time.sleep(0.5)
            self.change_pose_util('HeadYaw;' + str(basepose) + ';0.08')
            counter += 1

        self.back_to_live()

    def blink(self):
        self.leds.off("leds1")
        self.leds.off("leds2")
        self.leds.off("leds3")
        self.leds.on("leds3")
        self.leds.on("leds2")
        self.leds.on("leds1")


    def close_eyes(self):
        rDuration = 0.75
        self.leds.post.fadeRGB("FaceLed0", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed1", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed2", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed3", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed4", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed5", 0x000000, rDuration)
        self.leds.post.fadeRGB("FaceLed6", 0x000000, rDuration)
        self.leds.fadeRGB("FaceLed7", 0x000000, rDuration)
        time.sleep(2)
        self.leds.on("leds3")
        self.leds.on("leds2")
        self.leds.on("leds1")

    def move_head_naturally(self,_current_relationship):
        current_relationship=float(_current_relationship[0])
        if current_relationship==-1:
            factor=1
        else:
            factor= max(0.3, 1-current_relationship)

        angles=self.motionProxy.getAngles("Body", True)
        basepose_HeadYaw = angles[0]
        basepose_HeadPitch = angles[1]

        self.change_pose_util('HeadYaw,HeadPitch;' + str(min(max(basepose_HeadYaw + factor*random.uniform(-0.25,0.25),-1.05),1.05)) +',' + str(min(max(basepose_HeadYaw + factor*random.uniform(-0.1,0.1),-0.15),0.3)) + ';0.045')

    def back_to_live(self):
        time.sleep(2)
        self.publisher_to_nao.publish(self.parse_behavior({'action':'natural_motion'}))

    def end_work(self):

        if self.node_name != '3':
            # Sitdown
            self.postureProxy.goToPosture("Sit", 1.0)

        else:
            self.postureProxy.goToPosture("Crouch", 1.0)

        # rest
        self.rest()

strat=NaoNode('192.168.0.102','aa')  #FOR TEST!!!!!!!!!!
strat.animated_speech('Thought I would contribute to this discussion. My day was kinda average but more on the down side. Woke up with horrible anxiety and restless legs which lasted all morning so was kinda hard looking after my daughter. When she went down for nap I did as well. My sister tried texting me to come over with her son to play with my daughter but I didnt hear the fone because of being asleep and when I woke it was too late in the day for the catch up. When my daughter went to bed I managed to waater the back gardern as it really needed it. Half if not nearly all my flowers and plants are dead as of me not watering them. Another job that needs to be done but is too overwhelming for me to do is weeding so im going to call someone to do that for me. I relaxed this evening with a few movies on tv and going to go to sleep soon. Hope others had a bit better day than I did')








# print np.array([[0 , 0.6 , 0.3 , 0.9],[0.45 , 0  ,0.75  ,0.5],[0.15,0.9,0,0.1]])            1
# print np.array([[0 , 0.9 , 0.15 , 0.5],[0.75 , 0  ,0.45  ,0.9],[0.3, 0.6, 0, 0.1]])         2
# print np.array([[0 , 0.45 , 0.75 , 0.5],[0.6 , 0  ,0.3  ,0.1], [0.9, 0.15, 0 , 0.9]])           3
# print np.array([[0 , 0.3 , 0.6 , 0.9],[0.15 , 0  ,0.9  ,0.1],[0.45 , 0.75 , 0 ,0.5]])         4
# print np.array([[0 , 0.75 , 0.45 , 0.1],[0.9 , 0  ,0.15  ,0.5],[0.6, 0.3 ,0, 0.9]])         5







