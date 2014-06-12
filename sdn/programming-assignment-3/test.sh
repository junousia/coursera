#!/bin/bash

pkill python

cp firewall.py ~/pox/pox/misc
cp firewall-policies.csv ~/pox/pox/misc
python ~/pox/pox.py forwarding.l2_learning misc.firewall &
sudo mn --topo single,8 --controller remote --mac
