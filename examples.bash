#!/bin/bash
#
# Starting API
python2 main.py 5000 &
sleep 2
#
# POST method predict
curl -d '[
    {"Name": "erika"}

]' -H "Content-Type: application/json" \
     -X POST http://localhost:5000/predict && \
    echo -e "\n -> predict OK"

# kill runing API
for i in $(ps -elf | grep "python2 main.py 9999" | grep -v grep | cut -d " " -f 4); do
    kill -9 $i
done
