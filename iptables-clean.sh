#!/bin/bash

sudo iptables -F
sudo iptables -t nat -F
sudo iptables -t filter -F
sudo iptables -t mangle -F
sudo iptables -X
sudo iptables -t nat -X
sudo iptables -t filter -X
sudo iptables -t mangle -X

