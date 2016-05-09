#!/bin/bash

sudo ovs-ofctl dump-flows -O Openflow13 br-int | sed 's/duration=[0-9]*\.[0-9]*s, //'
