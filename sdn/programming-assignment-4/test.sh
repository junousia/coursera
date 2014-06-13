#!/bin/bash
cp topologySlice.py ~/pox/pox/misc/
cp mininetSlice.py ~/pox/pox/misc/
cd ~/pox/
python ./pox.py log.level --DEBUG misc.topologySlice &
sleep 1
cd ~/pox/pox/misc
sudo python mininetSlice.py
sleep 5
sudo mn -c
sudo fuser -k 6633/tcp
sudo pkill -9 python
