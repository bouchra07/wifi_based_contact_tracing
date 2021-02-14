#!/bin/bash

ip -br link show wlp2s0 | awk '{ print $3 }' > ./data/current_user.txt
