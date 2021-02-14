#!/bin/bash

sudo nmap -sn $1/24 | grep MAC > ./data/mac_log.txt

