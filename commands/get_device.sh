#!/bin/bash

sudo nmap -sn $1/24 | grep 192 > ./data/device_log.txt