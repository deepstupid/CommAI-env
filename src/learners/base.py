# Copyright (c) 2016-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import subprocess


class BaseLearner:
    def try_reward(self, reward):
        if reward is not None:
            self.reward(reward)

    def reward(self, reward):
        # YEAH! Reward!!! Whatever...
        pass

    def next(self, input):
        # do super fancy computations
        # return our guess
        return input


class RemoteLearner(BaseLearner):
    def __init__(self, cmd, port='5556'):
        try:
            import zmq
        except ImportError:
            raise ImportError("Must have zeromq for remote learner.")

        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % port)

        # launch learner
        subprocess.Popen(cmd.split())
        handshake_in = self.socket.recv_string()
        assert handshake_in == 'hello'  # handshake

    # send to learner, and get response;
    def next(self, input):
       	#print("send: ", input)
       	self.socket.send(input[0].encode())
        reply = self.socket.recv().decode()
        return reply

    def try_reward(self, reward):
        #print("reward: ", reward)
        reward = reward if reward is not None else 0
        self.socket.send(bytearray([reward]))
