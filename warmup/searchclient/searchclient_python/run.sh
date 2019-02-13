#!/bin/bash

for level in friendofBFS.lvl friendofDFS.lvl
do
	echo "$level bfs" >> res.dat
	java -jar ../server.jar -l ../levels/$level -c "python searchclient/searchclient.py -bfs --max-memory 2048" -g 150 -t 300 >> res.dat
	echo "$level dfs" >> res.dat
	java -jar ../server.jar -l ../levels/$level -c "python searchclient/searchclient.py -dfs --max-memory 2048" -g 150 -t 300 >> res.dat
done
