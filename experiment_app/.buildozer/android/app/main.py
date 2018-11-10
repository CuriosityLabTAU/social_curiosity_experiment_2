# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy_communication import *
from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')
Config.write()


class Start(BoxLayout):
    pass

class Wait(BoxLayout):
    pass

class Q_1(BoxLayout):
    pass

class Q_2(BoxLayout):
    pass

class Q_3(BoxLayout):
    pass

class Q_4(BoxLayout):
    pass

class TabletApp(App):
    def build(self):

        self.the_app = self
        self.basic_server_ip = '192.168.0.'

        self.server_ip_end = 100

        self.strat_screen = Start()
        self.wait_screen = Wait()
        self.q_1=Q_1()
        self.q_2=Q_2()
        self.q_3=Q_3()
        self.q_4=Q_4()


        # defines the screen manager, moves between forms
        self.sm = ScreenManager()

        # connects each form to a screen
        screen = Screen(name='strat_screen')
        screen.add_widget(self.strat_screen)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        screen = Screen(name='wait_screen')
        screen.add_widget(self.wait_screen)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        screen = Screen(name='q_1')
        screen.add_widget(self.q_1)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        screen = Screen(name='q_2')
        screen.add_widget(self.q_2)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        screen = Screen(name='q_3')
        screen.add_widget(self.q_3)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        screen = Screen(name='q_4')
        screen.add_widget(self.q_4)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        self.try_connection()

        return self.sm

    # ==========================================================================
    # ==== communicatoin to twisted server  KC: KivyClient KL: KivyLogger=====
    # ==========================================================================

    def try_connection(self):
        server_ip = self.basic_server_ip + str(self.server_ip_end)
        # server_ip = '127.0.0.1'

        KC.start(the_parents=[self], the_ip=server_ip)  # 127.0.0.1
        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir,
                 the_ip=server_ip)

    def failed_connection(self):
        print("failed_connection", self.server_ip_end)
        self.server_ip_end += 1
        if self.server_ip_end < 120:
            self.try_connection()
        else:
           self.screen_manager.get_screen('ScreenRegister').ids['callback_label'].text = 'stand alone ' + str(self.server_ip_end)

    def success_connection(self):
        self.server_ip_end = 99
        # self.screen_manager.current = 'Screen2'

    def on_connection(self):
        KL.log.insert(action=LogAction.data, obj='TabletApp', comment='start')
        print("the client status on_connection ", KC.client.status)
        if (KC.client.status == True):
            self.screen_manager.get_screen('ScreenRegister').ids['callback_label'].text = 'connected'

    def select_condition(self,spinner_inst):
        print("select_condition",spinner_inst.text)
        self.condition = spinner_inst.text
        KL.log.insert(action=LogAction.data, obj='select_condition', comment=str(spinner_inst.text))

    # def register_tablet(self):
    #     print("trying to register tablet. KC.client.status is ", KC.client.status)
    #     tablet_id = self.screen_manager.current_screen.ids['tablet_id'].text
    #     group_id = self.screen_manager.current_screen.ids['group_id'].text
    #     message = {'tablet_to_manager': {'action': 'register_tablet',
    #                                      'parameters': {'group_id': group_id, 'tablet_id': tablet_id}}}
    #     #if KC.client.status == True:
    #     if self.condition == 'robot':
    #         message_str = str(json.dumps(message))
    #         print("register_tablet", message_str)
    #         KC.client.send_message(message_str)
    #     else:
    #         self.screen_manager.current = 'ScreenDyslexia'

    def send_answer_to_ros(self,_answer):
        KC.client.send_message(_answer)
        # print _answer


    # ==========================================================================
    # ========================= App functions====================
    # ==========================================================================

    def start(self):
        # self.sm.current = "wait_screen"
        if KC.client.status == True:
            self.sm.current = "wait_screen"





    def begin_answering(self):
        self.current_question=1

        self.sm.current = "q_1"


    def next_question(self,_answer):
        self.send_answer_to_ros(_answer)

        if self.current_question%4 ==0:
            self.sm.current = "wait_screen"

        else:
            self.current_question += 1

            next_question="q_"+ str(self.current_question)
            self.sm.current = next_question




    # def data_received(self, data):
    #     print ("robotator_app: data_received", data)
    #     self.screen_manager.get_screen('ScreenRegister').ids['callback_label'].text = data
    #     try:
    #         json_data = [json.loads(data)]
    #     except:
    #         json_data = []
    #         spl = data.split('}{')
    #         print(spl)
    #         for k in range(0, len(spl)):
    #             the_msg = spl[k]
    #             if k > 0:
    #                 the_msg = '{' + the_msg
    #             if k < (len(spl) - 1):
    #                 the_msg = the_msg + '}'
    #             json_msg = json.loads(the_msg)
    #             json_data.append(json_msg)
    #             # print("data_received err", sys.exc_info())
    #
    #     for data in json_data:
    #         print("data['action']", data['action'])
    #         if (data['action'] == 'registration_complete'):
    #             self.screen_manager.get_screen('ScreenRegister').data_received(data)
    #             print("registration_complete")
    #
    #         if (data['action'] == 'show_screen'):
    #             print(data)
    #             self.screen_manager.current = data['screen_name']
    #
    #             if 'role' in data:
    #                 self.screen_manager.current_screen.update_role_bias(role=data['role'], bias=int(data['bias']))
    #
    #         if (data['action'] == 'start_timer'):
    #             self.screen_manager.current_screen.ids['timer_time'].start_timer(int(data['seconds']))
    #
    #         if data['action'] == 'set_widget_text':
    #             self.screen_manager.current_screen.ids[data['widget_id']].text = data['text']





if __name__ == "__main__":
    TabletApp().run()  # the call is from main.py