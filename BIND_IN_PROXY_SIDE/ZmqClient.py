#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 01:17:27 2021

@author: william
"""

import zmq


class ZmqClient(object):
    # Class Definition Initialization
    def __init__(self, strSubscribeAddr="tcp://127.0.0.1:65432"):
        # Create ZmqContext + Socket
        self.socketSubscribe = zmq.Context().socket(zmq.SUB)
        self.socketSubscribe.connect(strSubscribeAddr)
        self.boolRunning = True

    # subscribe message
    def subscribeTopic(self, strTopic):
        self.socketSubscribe.setsockopt_string(zmq.SUBSCRIBE, strTopic)#str(strTopic+"[S|E|P|E|R|A|T|E]"))
        while self.boolRunning:
            strMsgRecv = self.socketSubscribe.recv()
            # strMsgRecv = self.socketSubscribe.recv_string()
            print('[Subscriber] Received message: %s' % strMsgRecv)
            strTopic, strMsg = strMsgRecv.split(b"[S|E|P|E|R|A|T|E]")
            # After get the subscription message, do something
            ExampleClass.PrintMe("Topic[%s] Msg[%s]" % (strTopic, strMsg))

    def stop(self):
        self.boolRunning = False

################################
class ExampleClass(object):
    def PrintMe(strInput):
        print(strInput)
################################


# A publisher has no connected subscribers, then it will simply drop all messages.
# If you’re using TCP, and a subscriber is slow, messages will queue up on the publisher.
# In the current versions of ØMQ, filtering happens at the subscriber side, not the publisher side.

# Example
temp = ZmqClient()
temp.subscribeTopic("[TopicA]")



