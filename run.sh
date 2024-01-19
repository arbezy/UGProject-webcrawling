#!/bin/bash

VISITS=100

rm -rf results
mkdir -p results

echo "testing 123"

for i in {0..99}; do
	while read url; do
        python3 main.py $i https://$url
		# I think these kill lines are unecessary? as dumpcap killed elsewhere at least
		killall -9 dumpcap
		killall -9 python3
    done <urls.txt
done
