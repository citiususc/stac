#!/usr/bin/env python

import json
import yaml
import sys

with open (sys.argv[1], "r") as myfile:
    text = myfile.read()
    data = yaml.load(text)
    out = json.dumps(data)
 
    print(out)
