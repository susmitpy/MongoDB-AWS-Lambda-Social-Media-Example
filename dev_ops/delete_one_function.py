#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 19:42:22 2019

@author: susmitvengurlekar
"""

"""
aws lambda delete-function
--function-name 'create_profile_post'
"""
import sys
import os
os.chdir("../aws_lambda_functions/new")
pwd = os.getcwd()
cd_cmd = f"cd {pwd}"
prefix = "/Users/susmitvengurlekar/.local/bin/aws lambda delete-function --function-name {}"
comb_cmd =  cd_cmd +" && {}"
os.system(comb_cmd.format(prefix.format(sys.argv[1])))
            


