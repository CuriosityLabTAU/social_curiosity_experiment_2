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
from random import shuffle,randint


# from nao_ros import NaoNode
# nao=NaoNode('192.168.0.100','left')


class dynamics():
    def __init__(self,_info):
        #      |left | center | right |human
        #left  |
        #center|
        #right |
        number_of_naos=int(_info.split(',')[0])

        self.last_robot=None

        self.next_robot=None

        self.experimenter_nao=3

        self.is_stop = 0

        self.gender=_info.split(',')[1]

        self.number_of_naos=number_of_naos

        self.experiment_step=0

        self.interval=0

        self.current_answer=None

        self.matrix = self.bin_matrix(np.random.rand(3, 4))

        self.behaviors={
                        0:{
                        "left"  :[{'action':'run_behavior','parameters':['social_curiosity2/close_hands']}],
                        "center":[{'action':'run_behavior','parameters':['social_curiosity2/close_hands']}],
                        "right" :[{'action':'run_behavior','parameters':['social_curiosity2/close_hands']}]},

                        1: {
                        "left":   [{'action': 'look_to_other_way', 'parameters': ['left']}],
                        "center": [{'action': 'look_to_other_way', 'parameters': ['center']}],
                        "right":  [{'action': 'look_to_other_way', 'parameters': ['right']}]},

                        2: {
                        "left": [{'action': 'disagree'}],
                        "center": [{'action': 'disagree'}],
                        "right": [{'action': 'disagree'}]},

                        3: {
                        "left":   [{'action': 'run_behavior', 'parameters': ['social_curiosity2/scratching']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/scratching']}],
                        "right":  [{'action': 'run_behavior', 'parameters': ['social_curiosity2/scratching']}]},

                        4: {
                        "left":   [{'action':'open_hands'}],
                        "center": [{'action':'open_hands'}],
                        "right":  [{'action':'open_hands'}]},

                        5:{
                        "left"  :[{'action':'agree'}],
                        "center":[{'action':'agree'}],
                        "right" :[{'action':'agree'}]},

                        6:{
                        "left":   [{'action': 'run_behavior', 'parameters': ['social_curiosity2/right_forward']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/center_forward']}],
                        "right":  [{'action': 'run_behavior', 'parameters': ['social_curiosity2/left_forward']}]},

                        7:{
                        "left"  :[{'action': 'run_behavior', 'parameters': ['social_curiosity2/right_reaching']}],
                        "center":[{'action': 'run_behavior', 'parameters': ['social_curiosity2/center_reaching']}],
                        "right" :[{'action': 'run_behavior', 'parameters': ['social_curiosity2/left_reaching']}]},

                        8:{
                        "left":   [{'action':'hands_on_hips'}],
                        "center": [{'action':'hands_on_hips'}],
                        "right":  [{'action':'hands_on_hips'}]},

                        9:{
                        "left": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/clapping']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/clapping']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/clapping']}]},

                        10:{
                        "left": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/shrugging']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/shrugging']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/shrugging']}]},

                        11:{
                        "left": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/cover_eyes']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/cover_eyes']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/cover_eyes']}]},

                        12:{
                        "left": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/make_fist']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/make_fist']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/make_fist']}]},

                        13:{
                        "left": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/point_right']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/point_center']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['social_curiosity2/point_left']}]},

                        14: {
                            "left": [{'action': 'look_up'}],
                            "center": [{'action': 'look_up'}],
                            "right": [{'action': 'look_up'}]},

                        15: {
                            "left": [{'action': 'look_down'}],
                            "center": [{'action': 'look_down'}],
                            "right": [{'action': 'look_down'}]}}

        self.metadata_for_experiment_steps = {
                                        0: {'matrix':self.bin_matrix(np.array([[0 , 0.7 , 0.9 , 0.9],[0.9 , 0  ,0.1  ,0.5],[0.7,0.1,0,0.1]])),
                                            'turns' :{'number':4, 'first':0,'place_of_h':[2]},
                                            'question_time':[0,1,2,3],
                                            'experimenter_before':None,
                                            'experimenter_after' :[[{'action': 'run_behavior', 'parameters':['experimenter/2_'+self.gender]},68]]},

                                        1: {'matrix': self.bin_matrix(np.array([[0 , 0.75 , 0.45 , 0.1],[0.9 , 0  ,0.15  ,0.5],[0.6, 0.3 ,0, 0.9]])),
                                            'turns': {'number':8, 'first':1,'place_of_h':[3,6]},
                                            'question_time': [0,1,2,3],
                                            'experimenter_before': None,
                                            'experimenter_after': [[{'action': 'run_behavior', 'parameters':['experimenter/3']},5]]},

                                        2: {'matrix': self.bin_matrix(np.array([[0 , 0.9 , 0.15 , 0.5],[0.75 , 0  ,0.45  ,0.9],[0.3, 0.6, 0, 0.1]])),
                                            'turns': {'number':8, 'first':2,'place_of_h':[3,6]},
                                            'question_time': [0,1,2,3],
                                            'experimenter_before': [[{'action': 'run_behavior', 'parameters':['experimenter/4']},5]],
                                            'experimenter_after': [[{'action': 'run_behavior', 'parameters':['experimenter/3']},5]]},

                                        3: {'matrix': self.bin_matrix(np.array([[0 , 0.45 , 0.75 , 0.5],[0.6 , 0  ,0.3  ,0.1], [0.9, 0.15, 0 , 0.9]])),
                                            'turns': {'number':8, 'first':'h','place_of_h':[3,6]},
                                            'question_time': [0,1,2,3],
                                            'experimenter_before': [[{'action': 'run_behavior', 'parameters':['experimenter/4.1']},5]],
                                            'experimenter_after': [[{'action': 'run_behavior', 'parameters':['experimenter/3']},5]]},

                                        4: {'matrix': self.bin_matrix(np.array([[0 , 0.3 , 0.6 , 0.9],[0.15 , 0  ,0.9  ,0.1],[0.45 , 0.75 , 0 ,0.5]])),
                                            'turns': {'number':8, 'first':0,'place_of_h':[3,6]},
                                            'question_time': [0,1,2,3],
                                            'experimenter_before': [[{'action': 'run_behavior', 'parameters':['experimenter/4']},5]],
                                            'experimenter_after': [[{'action': 'run_behavior', 'parameters':['experimenter/5_'+self.gender]},10]]}}

        self.questions= {
                                0: [[{'action': 'run_behavior', 'parameters': ['experimenter/7']},6]],
                                1: [[{'action': 'run_behavior', 'parameters': ['experimenter/8']}, 5]],
                                2: [[{'action': 'run_behavior', 'parameters': ['experimenter/9_'+self.gender]}, 4]],
                                3: [[{'action': 'run_behavior', 'parameters': ['experimenter/10_'+self.gender]}, 4]]}

        self.discrete_behaviors=sorted(self.behaviors.keys())

        self.probs_from_AMT = pd.read_csv('probs_from_AMT.csv')

        self.transformation={0:{1:'left',2:'center','h':'right',},
                             1:{0:'right',2:'left','h':'center'},
                             2:{1:'right',0:'center','h':'left'}}

        self.position={0:'left',1:'center',2:'right'}

        self.next_robot_data={'left':[],'center':[],'right':[]}

        self.present_direction=0

        #ros:
        rospy.init_node('dynamics')
        self.publisher ={}
        self.publisher_alive   ={}
        self.publisher_blinking={}

        for nao in range(number_of_naos):
            name = 'to_nao_' + str(nao)
            print name
            self.publisher[nao]=rospy.Publisher(name, String, queue_size=10)

        #alive & blinking
        for nao in range(number_of_naos):
            name_alive   = 'alive'    + str(nao)
            name_blinking= 'blinking' + str(nao)
            self.publisher_alive[nao]    = rospy.Publisher(name_alive, String, queue_size=10)
            self.publisher_blinking[nao] = rospy.Publisher(name_blinking, String, queue_size=10)



        self.publisher_get_next = rospy.Publisher('get_next', String, queue_size=10)
        self.publisher_score = rospy.Publisher('correct_answer', String, queue_size=10)
        self.publisher_log= rospy.Publisher('log', String, queue_size=10)



        # rospy.Subscriber('the_flow', String, self.flow_handler)
        rospy.Subscriber('tablet_game', String, self.update_current_answer)

        rospy.Subscriber('alive', String, self.alive)
        rospy.Subscriber('next_step', String, self.run_dynamics)
        rospy.Subscriber('stop', String, self.stop)


        rospy.Subscriber('next_robot', String, self.update_next_robot)
        rospy.spin()

    def parse_behavior(self, _dict):
        return json.dumps(_dict)

    def flow_handler(self,data):
        step=data.data

    def alive(self,data):
        print 'alive in dynamics'
        for nao in range(self.number_of_naos):
            self.publisher_alive[nao].publish(self.parse_behavior({'action': 'alive'}))
            self.publisher_blinking[nao].publish(self.parse_behavior({'action': 'blinking'}))


    def stop(self,data):
        self.is_stop=1
        self.publisher_log.publish('experiment_stop')

        for nao in range(self.number_of_naos):
            self.publisher[nao].publish(self.parse_behavior({'action': 'end_work'}))


    def run_dynamics(self,data):
        #for AMT movies:
        if data.data == 'AMT':
            self.run_dynamics_for_AMT(data)
            return

        print 'dynamics' + str(data.data)
        self.experiment_step=int(data.data)
        self.publisher_log.publish('start:'+str(self.experiment_step))


        #prams for step:
        params_for_step=self.metadata_for_experiment_steps[self.experiment_step]
        self.matrix=params_for_step['matrix']

        if self.is_stop == 1:
            return

        ## introduction
        introduction_prams=params_for_step['experimenter_before']
        if introduction_prams !=None:
            self.publisher[3].publish(self.parse_behavior(introduction_prams[0][0]))
            time.sleep(introduction_prams[0][1])

        time.sleep(2.5)

        ## main
        for turn in range(params_for_step['turns']['number']):
            self.publisher_log.publish('turn:'+str(turn)+':start')

            if self.is_stop==1:
                return

            if turn==0:
                main_robot = params_for_step['turns']['first']
                self.last_robot=main_robot
                self.publisher_get_next.publish('reset')

            else:
                if turn not in params_for_step['turns']['place_of_h']:
                    self.next_robot= None
                    self.publisher_get_next.publish(str(self.last_robot))

                else:
                    self.publisher_get_next.publish('reset')
                    self.next_robot= 'h'


                while self.next_robot==None:
                    pass

                main_robot = self.next_robot
                self.last_robot=main_robot

            self.publisher_log.publish('turn:'+str(turn)+':start:main:'+str(main_robot))


            secondary_robots = [0, 1, 2]

            print main_robot

            #config robots
            if main_robot!='h':
                secondary_robots.remove(main_robot)

            #main robot - main behavior
            if main_robot!='h':
                behavior_n=randint(1, 4)
                self.publisher[main_robot].publish(self.parse_behavior({'action':'run_behavior','parameters':['social_curiosity2/talk/'+str(behavior_n)]}))
                self.publisher[main_robot].publish(self.parse_behavior({'action':'change_current_relationship','parameters':[str(1.0)]}))
                self.publisher_log.publish('main:behavior:' + str(behavior_n))

            #secondary_robots look at main robot
            for robot in secondary_robots:
                time.sleep(1)
                self.publisher[robot].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[robot][main_robot]]}))

            time.sleep(8)

            #secondary_robots look at main behaviour
            if main_robot=='h':
                place_in_matrix=3
            else:
                place_in_matrix=main_robot

            back_to_sit_bol=[0,0,0]
            for robot in secondary_robots:
                relationship=self.matrix[robot,place_in_matrix]
                direction_for_behavior=self.transformation[robot][main_robot]
                chosen_behaviour=self.choose_behaviour(relationship)

                behavior=random.choice(self.behaviors[chosen_behaviour][direction_for_behavior])

                self.publisher[robot].publish(self.parse_behavior({'action':'change_current_relationship','parameters':[str(relationship)]}))
                self.publisher[robot].publish(self.parse_behavior(behavior))
                self.publisher_log.publish('secondary:'+str(robot)+'behavior:' + str(self.parse_behavior(behavior)+':relationship:'+str(relationship)))


                if behavior in [{'action': 'run_behavior', 'parameters': ['social_curiosity2/neutral']},{'action': 'run_behavior', 'parameters': ['social_curiosity2/right_lean_back']},{'action': 'run_behavior', 'parameters': ['social_curiosity2/left_lean_back']}]:
                    back_to_sit_bol[robot]=1

                time.sleep(1.5)

            time.sleep(4)

            self.publisher_log.publish('all:back_to_sit')

            for robot in [0,1,2]:
                # change_current_relationship
                self.publisher[robot].publish(self.parse_behavior({'action': 'change_current_relationship', 'parameters': [str(-1.0)]}))
                #go to sit
                if back_to_sit_bol[robot]==1:
                    self.publisher[robot].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': ['social_curiosity2/back_to_sit']}))
                else:
                    self.publisher[robot].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': ['social_curiosity2/back_to_sit_2']}))


            time.sleep(2.5)

        #sit befor questions
        for robot in [0, 1, 2]:
            self.publisher[robot].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': ['social_curiosity2/back_to_sit_2']}))



        #question asking
        q_order=params_for_step['question_time']
        if params_for_step['question_time'] !=None:
            self.publisher_log.publish('question:start')

            self.question_time(q_order)

            self.publisher_log.publish('question:end')

        if self.is_stop == 1:
            return

        for robot in [0, 1, 2]:
            self.publisher[robot].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': ['social_curiosity2/back_to_sit_2']}))

        ## end phrase
        end_phrase = params_for_step['experimenter_after']
        if end_phrase != None:
            self.publisher[3].publish(self.parse_behavior(end_phrase[0][0]))
            time.sleep(end_phrase[0][1])

        self.publisher_log.publish('end:'+str(self.experiment_step))


    def question_time(self,order):

        if self.is_stop == 1:
            return

        ## introduction
        if self.experiment_step==0:
            self.publisher[3].publish(self.parse_behavior({'action': 'run_behavior', 'parameters':['experimenter/1_'+self.gender]}))
            time.sleep(28)
        else:
            self.publisher[3].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': ['experimenter/6_'+self.gender]}))
            time.sleep(11)
        print  'question_time'

        for q in order:
            if self.is_stop == 1:
                return


            self.current_answer = None
            # experimenter
            #params:
            question=self.questions[q]
            correct_robot_answer=self.correct_robot_answer(self.matrix,q)

            self.publisher_log.publish('question:start:'+str(q))

            # experimenter ask question:
            self.publisher[3].publish(self.parse_behavior(question[0][0]))
            time.sleep(question[0][1])

            #all robot look at subject:
            all_robots=[0,1,2]
            shuffle(all_robots)
            for robot in all_robots:
                time.sleep(0.5)
                self.publisher[robot].publish(self.parse_behavior({'action':'change_current_relationship','parameters':[str(1)]}))
                self.publisher[robot].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[robot]['h']]}))
            print 'wating for : '+ str(q)

            while self.current_answer ==None:
                pass

            self.publisher_log.publish('question:answer:'+str(self.current_answer)+':correct:'+str(correct_robot_answer))

            for robot in [0,1,2]:
                self.publisher[robot].publish(self.parse_behavior({'action': 'change_current_relationship', 'parameters': [str(-1)]}))


            #answer time
            if self.current_answer==correct_robot_answer:
                self.publisher_score.publish('correct')
                parameter=random.choice(['Sit/Gestures/Me_7'])
                self.publisher[correct_robot_answer].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': [parameter]}))
                time.sleep(2)

                parameter=random.choice(['experimenter/11','experimenter/11_'+self.gender])
                self.publisher[3].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': [parameter]}))
                time.sleep(5)


            else:
                robot = [0, 1, 2]
                robot.remove(correct_robot_answer)
                if self.current_answer!=-1:

                    self.publisher[self.current_answer].publish(self.parse_behavior({'action': 'disagree'}))
                    self.publisher[self.current_answer].publish(self.parse_behavior({'action':'change_current_relationship','parameters':[str(1)]}))
                    time.sleep(7)
                    for r in robot:
                        self.publisher[r].publish(self.parse_behavior({'action': 'move_to_pose','parameters': [self.transformation[r][correct_robot_answer]]}))
                        time.sleep(0.3)
                    time.sleep(0.5)
                    parameter=random.choice(['Sit/Gestures/Me_7'])
                    self.publisher[correct_robot_answer].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': [parameter]}))
                    self.publisher[self.current_answer].publish(self.parse_behavior({'action':'change_current_relationship','parameters':[str(-1)]}))

                    time.sleep(2)


                    parameter = random.choice(['experimenter/12', 'experimenter/12_' + self.gender])

                    self.publisher[3].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': [parameter]}))
                    time.sleep(5)

                else:

                    for r in robot:
                        self.publisher[r].publish(self.parse_behavior({'action': 'move_to_pose','parameters': [self.transformation[r][correct_robot_answer]]}))
                        time.sleep(0.2)

                    time.sleep(1.5)

                    parameter=random.choice(['Sit/Gestures/Me_7'])
                    self.publisher[correct_robot_answer].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': [parameter]}))

                    time.sleep(1)

                    parameter = random.choice(['experimenter/12'])
                    self.publisher[3].publish(self.parse_behavior({'action': 'run_behavior', 'parameters': [parameter]}))

                    time.sleep(5)




    def correct_robot_answer(self,_matrix,n_question):
            if n_question==0:
                return np.argmax((_matrix.sum(axis=0))[0:3])

            elif n_question==1:
                return np.argmin((_matrix.sum(axis=0))[0:3])

            elif n_question == 2:
                return np.argmax(_matrix[:, 3])

            elif n_question == 3:
                return np.argmin(_matrix[:, 3])



    def run_dynamics_for_AMT(self, data):
        robots = [0, 1]


        for i in range(15,16):

            # secondary_robots look at main robot
            self.publisher[0].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[0][1]]}))
            time.sleep(1.5)

            self.publisher[1].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[1][0]]}))

            time.sleep(3)


            direction_for_behavior = self.transformation[1][0]

            behavior = self.behaviors[i][direction_for_behavior][0]
            self.publisher[1].publish(self.parse_behavior(behavior))
            # self.publisher[1].publish(self.parse_behavior({'action': 'look_up'}))


            print i

            time.sleep(6)

            self.publisher[0].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[0][2]]}))
            time.sleep(1.5)
            self.publisher[1].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[1]['h']]}))

            time.sleep(8)


    def test(self,aa):
        print 'here'
        self.publisher['left'].publish('{\"action\": \"wake_up\"}')
        # time.sleep(5)

        # self.publisher['left'].publish('{\"action\": \"move_to_pose\", \"parameters\": \"\\\"''right''\\\"\"}')
        # self.publisher['left'].publish('{\"action\": \"look_to_other_way\", \"parameters\": \"\\\"''right''\\\"\"}')
        self.publisher['left'].publish('{\"action\": \"disagree\"}')

        time.sleep(20)

        self.publisher['left'].publish('{\"action\": \"rest\"}')

    def choose_behaviour(self,relationship):
        probability_distribution=self.probs_from_AMT[str(relationship)].tolist()
        list_of_candidates=self.discrete_behaviors
        draw = np.random.choice(list_of_candidates, 1, p=probability_distribution)
        return draw[0]

    def bin_matrix(self,_matrix):
        number_of_bins = 9
        bins = [i * (1.0 / number_of_bins) for i in xrange(number_of_bins + 1)]
        labels = [(bins[i] + bins[i + 1]) / 2.0 for i in xrange(number_of_bins)]
        labels = list(np.around(np.array(labels), 3))
        matrix=_matrix

        for i in range(_matrix.shape[0]):
            for j in range(_matrix.shape[1]):
                for _bin in range(len(bins) - 1):
                    if matrix[i, j] >= bins[_bin] and matrix[i, j] < bins[_bin + 1]:
                       matrix[i, j] = labels[_bin]
        matrix[0,0]=0
        matrix[1,1]=0
        matrix[2,2]=0

        return matrix

    def update_current_answer(self,data):
        try:
            self.current_answer=int(data.data)
        except:
            all

    def update_next_robot(self,data):
        if data.data !='h':
            self.next_robot=int(data.data)
        else:
            self.next_robot = data.data

if len(sys.argv) > 1:
    start=dynamics((sys.argv[1]))
# else:
#     start=dynamics(1)
    # start.test()
