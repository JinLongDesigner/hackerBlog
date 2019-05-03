#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@Author: xxlin
@LastEditors: xxlin
@Date: 2019-04-10 13:27:59
@LastEditTime: 2019-05-03 00:22:39
'''

import os
import sys

from gevent import monkey
monkey.patch_all()
from ujscanner.lib.controller.engine import run
from ujscanner.lib.core.common import banner, outputscreen, setPaths
from ujscanner.lib.core.data import cmdLineOptions, conf, paths
from ujscanner.lib.core.option import initOptions
from ujscanner.lib.parse.cmdline import cmdLineParser




def main():
    """
    main fuction of dirmap 
    """

    # anyway output thr banner information
    banner() 

    # set paths of project 
    paths.ROOT_PATH = os.getcwd() 
    setPaths()
    
    # received command >> cmdLineOptions
    cmdLineOptions.update(conf.webConfig)
    
    # loader script,target,working way(threads? gevent?),output_file from cmdLineOptions
    # and send it to conf
    initOptions(cmdLineOptions)

    # run!
    run()

if __name__ == "__main__":
    main()
