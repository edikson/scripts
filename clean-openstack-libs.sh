#!/bin/bash

echo "Cleaning all openstack dependencies"

pip search oslo | grep -B1 '^\s*INSTALLED' | grep '^o' | awk '{ print $1}' | xargs sudo pip uninstall -y
pip search python- | grep -B1 '^\s*INSTALLED' | grep '^p' | awk '{ print $1}' | xargs sudo pip uninstall -y
sudo pip uninstall -y oauth2client
sudo pip uninstall -y os_client_config apiclient
sudo pip uninstall -y neutron_lib
sudo pip uninstall -y glance_store
sudo pip uninstall -y virtualenv
sudo pip uninstall -y amqp
sudo pip uninstall -y neutron_lib
sudo pip uninstall -y requests_mock
sudo pip uninstall -y ipdb
sudo pip uninstall -y libvirt_python
sudo pip uninstall -y ryu
sudo pip uninstall -y dnspython
sudo pip uninstall -y qpid_python
sudo pip uninstall -y ipython_genutils
sudo pip uninstall -y ipython
sudo pip uninstall -y msgpack_python
sudo pip uninstall -y pymysql
sudo apt-get remove rabbitmq-server
sudo apt-get remove redis
sudo apt-get remove etcd

