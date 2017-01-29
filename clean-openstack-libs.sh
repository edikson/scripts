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
sudo pop uninstall -y keystoneauth1
sudo pip uninstall -y keystonemiddleware
sudo pip uninstall -y os-vif
sudo pip uninstall -y os-win
sudo pip uninstall -y os-brick
sudo pip uninstall -y pyroute2
sudo pip uninstall -y oslo.policy
sudo pip uninstall -y tooz
sudo pip uninstall -y XStatic-roboto-fontface

sudo apt-get -y remove rabbitmq-server
sudo apt-get -y remove redis
sudo apt-get -y remove etcd
sudo apt-get -y remove rabbitmq-server memcached
rm -rf /etc/neutron
rm -rf /etc/cinder
rm -rf /etc/keystone
rm -rf /etc/glance

