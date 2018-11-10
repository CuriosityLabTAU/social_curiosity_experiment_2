import os
import threading
import time
import sys
import json


def intro(subject_id=0, nao_info=[('192.168.0.100','center')]):
    start_working(subject_id, nao_info)
    time.sleep(60)


def start_working(subject_id, nao_info):
    print 'intro'+str(nao_info)

    gender= nao_info[-1][0]

    nao_info=nao_info[:-1]


    def worker1():
        os.system('roscore')

    #make the class instance for nao_ros
    def worker2(_nao):
        if _nao[0]=='0':
            return
        os.system('python nao_ros.py' + ' '+ _nao[0]+' '+_nao[1])

    def worker22(_nao):
        if _nao[0] == '0':
            return
        os.system('python nao_subconscious.py' + ' '+ _nao[0]+' '+_nao[1])

    def worker3():
        os.system('python dynamics.py'+' '+ str(len(nao_info))+','+gender)

    def worker4():
        os.system('python next_robot.py')

    def worker5():
        dict_to_pass={}
        for i in range((len(nao_info))):
            dict_to_pass[nao_info[i][2]]=nao_info[i][1]
        str_to_pass=json.dumps(dict_to_pass)

        print('worker 5', str_to_pass)
        os.system('python pupel_ros.py' + ' ' +"'"+str_to_pass+"'")

    def worker6():
        os.system('python twisted_server_ros.py')


    # def worker1():
    #     os.system('roslaunch multi_camera_affdex multi_camera_affdex.launch')
    #
    # def worker2():
    #     os.system('roslaunch skeleton_markers markers.launch')
    #     return
    #


    def worker7():
        os.system('rosbag record -a -o data/social_curiosity_big_experiment_' + str(subject_id) + '.bag')




    t1 = threading.Thread(target=worker1)
    # t1.start()
    # threading._sleep(0.2)
    #
    for nao in nao_info:
        print 'nao' + str(nao)
        t22 = threading.Thread(target=worker22, args=(nao,))
        t22.start()
        threading._sleep(2.5)

    for nao in nao_info:
        print 'nao'+str(nao)
        t2 = threading.Thread(target=worker2,args=(nao,))
        t2.start()
        threading._sleep(2.5)



    t3 = threading.Thread(target=worker3)
    t3.start()
    threading._sleep(0.2)

    t4 = threading.Thread(target=worker4)
    t4.start()
    threading._sleep(0.2)

    t5 = threading.Thread(target=worker5)
    t5.start()
    threading._sleep(0.2)

    t6 = threading.Thread(target=worker6)
    t6.start()
    threading._sleep(0.2)

    t7 = threading.Thread(target=worker7)
    t7.start()
    threading._sleep(0.2)

if len(sys.argv) > 1:
    print('sys.argv', sys.argv)
    nao_arg_list=[element.split('@') for element in sys.argv[2:]]
    intro(int(sys.argv[1]), nao_arg_list)
else:
    intro()
