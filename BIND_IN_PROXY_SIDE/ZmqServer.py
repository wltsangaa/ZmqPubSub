import time
import random
import zmq
import threading
import os

class ZmqServer(object):
    # Class Definition Initialization
    def __init__(self, strSerPubAddr='tcp://127.0.0.1:23456', strMode = 'CONNECT_TO_PUB_SOCKET'):
        # Create ZmqContext + Socket
        self.objContext = zmq.Context()
        self.socketSerPub = self.objContext.socket(zmq.PUB)
        if 'BIND_NEW_PUB_SOCKET' == strMode: self.socketSerPub.bind(strSerPubAddr)
        elif 'CONNECT_TO_PUB_SOCKET' == strMode: self.socketSerPub.connect(strSerPubAddr)
        else: raise(BaseException("WRONG CLASS CALL"))
        self.boolGlobalRunning = True

    # Publish Message With Corresponding Topic
    def publishMessage(self, strTopic, strMsg):
        self.socketSerPub.send_string("%s[S|E|P|E|R|A|T|E]%s" % (str(strTopic), str(strMsg)))
        print("%s[S|E|P|E|R|A|T|E]%s" % (str(strTopic), str(strMsg)))
    
    def stop(self):
        self.boolGlobalRunning = False
        self.objContext.destroy()
        os._exit(1)

    # Forever loop Example
    def runExample(self):
        intStart = 1
        while self.boolGlobalRunning:
            intTopicIDExample = random.randrange(0,3)
            listTopicExample = ["[TopicA]","[TopicB]","[TopicC]"]
            strMessageExample = str(intStart)+"-"+str(random.randrange(11111,99999))
            intStart+=1
            # print("%s %s" % (listTopicExample[intTopicIDExample], strMessageExample))
            self.publishMessage(listTopicExample[intTopicIDExample], strMessageExample)
            time.sleep(3)

    # Forever loop Example In A New Thread
    def runExampleInNewThread(self):
        exampleThreadHandler = threading.Thread(
            target=self.runExample,
        )
        exampleThreadHandler.start()


# Example 1
temp = ZmqServer(strMode = 'CONNECT_TO_PUB_SOCKET')
# Example In Running a loop send message
temp.runExampleInNewThread()
# Example In Sending Single Message
temp.publishMessage(strTopic="[TopicA]", strMsg="This Example Is Nice")

# # Example 2
# temp2 = ZmqServer(strSerPubAddr='tcp://127.0.0.1:65432', strMode='CONNECT_TO_PUB_SOCKET')
# while True:
#     temp2.publishMessage(strTopic="[TopicA]", strMsg="This Example Is Nice")
#     time.sleep(5)

