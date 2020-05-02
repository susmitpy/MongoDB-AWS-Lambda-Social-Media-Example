#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 11:40:50 2019

@author: susmitvengurlekar
"""

import os
from subprocess import Popen, PIPE

ignore = ["deploy", "delete", "delete_one_function","endpoint_url","new","aws_interaction.",".DS_St",""]
users_api = "ouygzsw277"
fields_api = "pv2zaakas1"

p = Popen(["/Users/susmitvengurlekar/.local/bin/aws", 'apigateway', 'get-resources', '--rest-api-id',users_api], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output = p.stdout.readlines()

os.chdir("../aws_lambda_functions/")
funcs = [i[:-3] for i in os.listdir() if i[:-3] not in ignore]

std_link = "https://ouygzsw277.execute-api.ap-south-1.amazonaws.com/alpha"

to_write = "final String {} = \"{}\";\n"

file = open("aws_interaction.txt","w")


for o in output:
    s = o.decode()
    row = s.split("\t")
    if row[-1].strip().replace("-","_") in funcs:
        func_name = row[-1].strip().replace("-","_")
        invoke_link = std_link+row[-2]
        file.write(to_write.format(func_name,invoke_link))
        
file.close()
     
        
