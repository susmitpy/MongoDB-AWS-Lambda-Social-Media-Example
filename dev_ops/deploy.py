#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 19:42:22 2019

@author: susmitvengurlekar
"""

"""
aws lambda create-function
--function-name 'create_profile_post'
 --runtime 'python3.7'
 --role 'arn:aws:iam::218641615626:role/service-role/dummy-role-2oajn09q'
 --handler 'awscli.handler'
 --environment '{"Variables":{"un":"aws","pw":"aws_flyer"}}'
 --zip-file fileb://./zips/create_profile_post.zip
"""
import os
os.chdir("../aws_lambda_functions/new")
pwd = os.getcwd()
classes_layer="arn:aws:lambda:ap-south-1:218641615626:layer:classes:9"
mongo_layer="arn:aws:lambda:ap-south-1:218641615626:layer:mongo_engine_dependency:1"
cd_cmd = f"cd {pwd}"
prefix = "/Users/susmitvengurlekar/.local/bin/aws lambda create-function"
fn = "--function-name '{}'"
r = "--runtime 'python3.7'"
role = "--role 'arn:aws:iam::218641615626:role/service-role/dummy-role-2oajn09q'"
handler = "--handler '{}.lambda_handler'"
env = "--environment '{\"Variables\":{\"un\":\"aws\",\"pw\":\"aws_flyer\"}}'"
file = "--zip-file fileb://./zips/{}"
layers = f"--layers {mongo_layer} {classes_layer}"

zip_cmd = "zip ./zips/{}.zip {}"

comb_cmd = cd_cmd + " && {}"



for py in os.listdir():
        if py[-2:] == "py":
            os.system(comb_cmd.format(zip_cmd.format(py[:-3],py)))
            cmds = [prefix, fn.format(py[:-3]), r, role, handler.format(py[:-3]), env,layers, file.format(py[:-2] + "zip")]
            cmd = " ".join(cmds)
            os.system(comb_cmd.format(cmd))
            os.system(comb_cmd.format(f"mv {py} ../"))
