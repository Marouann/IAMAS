#!/bin/bash

java -jar ../server.jar -l ../levels/$1.lvl -c "python searchclient/searchclient.py -$2 --max-memory 2048" -g 150 -t 450 >> res.dat
