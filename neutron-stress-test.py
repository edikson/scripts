#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# neutron subnet-list | grep SUBNET- | gawk '{print "neutron subnet-delete "$2}' | bash
# neutron port-list | grep "                             " | gawk '{print "neutron port-delete "$2}' | bash

import sys
import time
import os_client_config
from neutron.agent.common import utils
from neutron.common import config as common_config
from neutronclient.neutron import client
from dragonflow.common import common_params

def get_cloud_config(cloud='devstack-admin'):
    return os_client_config.OpenStackConfig().get_one_cloud(cloud=cloud)

def credentials(cloud='devstack-admin'):
    """Retrieves credentials to run functional tests"""
    return get_cloud_config(cloud=cloud).get_auth_args()


class StressTest():

    def __init__(self):
        creds = credentials()
        tenant_name = creds['project_name']
        auth_url = creds['auth_url'] + "/v2.0"
        print creds
        self.neutron = client.Client('2.0', username=creds['username'],
             password=creds['password'], auth_url=auth_url,
             tenant_name=tenant_name)

    def create_get_router(self, name):
        routers = self.neutron.list_routers(name=name)
        routers = routers['routers']
        if len(routers) > 0:
            return routers[0]['id']

        router={'name': name, 'admin_state_up': True}
        new_router = self.neutron.create_router({'router': router})
        self.router_id = new_router['router']['id']
        return self.router_id

    def create_get_net(self, name):
        networks = self.neutron.list_networks(name=name)['networks']
        networks_count = len(networks)
        if networks_count > 0:
            return networks[0]['id']
        network={'name': name, 'admin_state_up': True, 'shared': True}
        network = self.neutron.create_network({'network': network})
        return network['network']['id']

    def create_subnet_and_link_to_router(self, router_id, network_id, name, ip_net):
        subnet = {
            'cidr': ip_net,
            'name': name,
            'ip_version': 4,
            'network_id': network_id
        }
        subnet = self.neutron.create_subnet(body={'subnet': subnet})
        subnet_id = subnet['subnet']['id']
        self.neutron.add_interface_router(router_id, body={'subnet_id': subnet_id})

    def create_subnet(self, router_id, network_id, name, ip_net):
        subnet = {
            'cidr': ip_net,
            'name': name,
            'ip_version': 4,
            'network_id': network_id
        }
        subnet = self.neutron.create_subnet(body={'subnet': subnet})
        #subnet_id = subnet['subnet']['id']

    def test1(self):
        router_id = self.create_get_router('ROUTER-1')
        #print("router_id", router_id)
        for j in range(2,4):
            network_id = self.create_get_net('NETWORK-'+str(j))
            #print("network_id", network_id)
            start = time.time()
            for i in range(100):
                ip_net = "".join(('1.', str(j), '.', str(i), '.0/24'))
                self.create_subnet_and_link_to_router(router_id, network_id, 'SUBNET-'+str(j)+'-'+str(i), ip_net)
            end = time.time()
            total = end-start
            print("time spend to create 100 subnets: " + str(int(total)))

def main():
    test = StressTest()
    test.test1()

if __name__ == '__main__':
    sys.exit(main())
