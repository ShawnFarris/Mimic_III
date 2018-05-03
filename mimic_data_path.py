#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:55:55 2018

@author: shawn
"""

import json
import os

mimic_data_path = input("Enter path to Mimic data(csv): ")
if mimic_data_path[0] == mimic_data_path[-1] == "'" or mimic_data_path[0] == mimic_data_path[-1] == '"':
    mimic_data_path = mimic_data_path[1:-1]

folder_paths = {'mimic_data_path':mimic_data_path}
# Save in Seperate JSON
with open(os.getcwd() + '/folder_paths.json','w') as fp:
    json.dump(folder_paths, fp)
    