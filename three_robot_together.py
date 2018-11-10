from naoqi import ALProxy
import time

time.sleep(10)

##story file

text_file = open("text.txt", 'r')



IP_1='192.168.0.110'
IP_2='192.168.0.101'
IP_3='192.168.0.102'

PORT=9559

####Initialize the API's
tts_1 = ALProxy("ALAnimatedSpeech", IP_1, PORT)
tts_2 = ALProxy("ALAnimatedSpeech", IP_2, PORT)
tts_3 = ALProxy("ALAnimatedSpeech", IP_3, PORT)

proxy_1 = ALProxy("ALLeds", IP_1, PORT)
proxy_2 = ALProxy("ALLeds", IP_2, PORT)
proxy_3 = ALProxy("ALLeds", IP_3, PORT)

#text:
text=text_file.read()
text = text.split('\n')

#parms:
name = 'FaceLeds'


###speech:
n = 0
proxy_1.off(name)
proxy_2.off(name)
proxy_3.off(name)

for t in text:

    if n%3 ==0:
        proxy_1.on(name)
        tts_1.say(t)
        n+=1
        proxy_1.off(name)

    elif n%3 ==1:
        proxy_2.on(name)
        tts_2.say(t,{"pitchShift":1.05})
        n += 1
        proxy_2.off(name)


    elif n % 3 == 2:
        proxy_3.on(name)
        tts_3.say(t,{"pitchShift":1.01})
        n += 1
        proxy_3.off(name)
