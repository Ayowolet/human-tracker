#!/usr/bin/env python3
"""
 Copyright (c) 2018 Intel Corporation.

 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys
import logging as log
from openvino.inference_engine import IENetwork, IECore
from utils import *

class Network:
    """
    Load and configure inference plugins for the specified target devices 
    and performs synchronous and asynchronous modes for the specified infer requests.
    """

    def __init__(self):
        ### TODO: Initialize any class variables desired ###
        self.plugin = None
        self.network = None
        self.input_blob = None
        self.output_blob = None
        self.exec_network = None
        self.infer_request = None
        
    def load_model(self,model_archref=None, device='CPU', cpu_ext=None):
        ### TODO: Load the model ###
        if not model_archref:
            raise Exception("ref to model not provided ""(e.g model.xml)")
            
        bin_ = model_archref.split('.')[0]+'.bin'

        #loading the network with the IENetwork class
        self.network = IENetwork(model_archref,bin_)
        
        #Initializing the IECore
        self.plugin = IECore()
        
        #check for supported layers
        supported_layers = self.plugin.query_network(network=self.network, device_name=device)
        
        #check for unsupported layers
        unsupported_layers = [l for l in self.network.layers.keys() if l not in supported_layers]
        
        ### TODO: Add any necessary extensions ###
        if len(unsupported_layers) > 0 and cpu_ext and "CPU" in device:
            self.plugin.add_extension(cpu_ext,device)
        else:
            raise FileNotFoundError("either CPU extention wasn't specified and unsupported layers are present or you did't specify device to be cpu")
            
        # Load IENetwork into IECore
        self.exc_net = self.plugin.load_network(self.network, device,num_requests=1)
        
        #get input and output blobs
        self.input_blobs  = next(iter(self.network.inputs))
        self.output_blobs = sorted(self.network.outputs)
        ### TODO: Return the loaded inference plugin ###
        ### Note: You may need to update the function parameters. ###
        return

    def get_input_shape(self):
        ### TODO: Return the shape of the input layer ###
        return self.network.inputs[self.input_blobs].shape

    def exec_net_sync(self,image):
        ### TODO: Start an asynchronous request ###
        self.sync_out = self.exc_net.infer(inputs={self.input_blobs:image})
        
    def exec_net_async(self,image,id_):
        ### TODO: Start an asynchronous request ###
        print(id_)
        self.exc_net.start_async(request_id=id_,
                                 inputs={self.input_blobs:image})
        ### TODO: Return any necessary information ###
        ### Note: You may need to update the function parameters. ###
        return

    def wait(self,id_):
        ### TODO: Wait for the request to be complete. ###
        ### TODO: Return any necessary information ###
        ### Note: You may need to update the function parameters. ###
        return self.exc_net.requests[id_].wait(-1)

    def get_output(self,id_=None):
        ### TODO: Extract and return the output results
        ### Note: You may need to update the function parameters. ###
#         return self.exec_network.requests[0].outputs[self.output_blob
        print('final get output {}'.format(0))
        if id_ != None:
            return list(self.exc_net.requests[0].outputs.values())
        else:
#             print('sync out is {}'.format(self.sync_out))
            return list(self.sync_out.values())