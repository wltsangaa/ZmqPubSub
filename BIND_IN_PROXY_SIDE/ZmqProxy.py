#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
import os

class ZmqProxy(object):
    # Class Definition Initialization
    def __init__(self, strAddrForSubConnect="tcp://*:65432", strAddrForPubConnect="tcp://*:23456"):
        # Create ZmqContext + Socket
        self.objContext = zmq.Context()
        self.strAddrForSubConnect = strAddrForSubConnect
        self.strAddrForPubConnect = strAddrForPubConnect
        self.socketForSubConnect = None
        self.socketForPubConnect = None

    def start(self):
        # Socket facing producers, let other subscriber connect it
        print("=> Socket facing producers, let other subscriber connect it")
        self.socketForSubConnect = self.objContext.socket(zmq.XPUB)
        self.socketForSubConnect.bind(self.strAddrForSubConnect)
        # Socket facing consumers, let publisher connect it
        print("=> Socket facing consumers, let publisher connect it")
        self.socketForPubConnect = self.objContext.socket(zmq.XSUB)
        self.socketForPubConnect.bind(self.strAddrForPubConnect)
        # Build the Proxy
        print("=> Build the Proxy, Processing......")
        zmq.proxy(self.socketForSubConnect, self.socketForPubConnect)

    def stop(self):
        self.socketForSubConnect.close()
        self.socketForPubConnect.close()
        self.objContext.term()
        os._exit(1)
