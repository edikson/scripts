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


class NeutronCleaner():

    def __init__(self):
        creds = credentials()
        tenant_name = creds['project_name']
        auth_url = creds['auth_url'] + "/v2.0"
        print creds
        self.neutron = client.Client('2.0', username=creds['username'],
             password=creds['password'], auth_url=auth_url,
             tenant_name=tenant_name)

    def clean(self):
        name = 'NETWORK-1'
        networks = self.neutron.list_networks(name=name)['networks']
        for net in networks:
            print(net)
            ports = self.neutron.list_ports(network_id=net['id'])
            ports = ports['ports']
            for port in ports:
                print(port['device_owner'], port['id'])
                if port['device_owner'] == 'network:router_interface':
                    for fip in port['fixed_ips']:
                        subnet_msg = {'subnet_id': fip['subnet_id']}
                        self.neutron.remove_interface_router(
                            port['device_id'], body=subnet_msg)
                elif port['device_owner'] == 'network:router_gateway':
                    pass
                else:
                    #ry:
                    self.neutron.delete_port(port['id'])
                    #xcept neutron_common.exceptions.PortNotFoundClient:
                    #ass
            subnets = self.neutron.list_subnets(network_id=net['id'])
            subnets = subnets['subnets']
            for subnet in subnets:
                print(subnet)
                self.neutron.delete_subnet(subnet['id'])
        return
        """
            print(net)
            network_id = net['id']
            ports = self.neutron.list_ports(network_id=network_id)
            ports = ports['ports']
            for port in ports:
                if port['device_owner'] == 'network:router_interface':
                    print(port['device_owner'], port['id'], port['device_id'])
                elif port['device_owner'] == 'network:dhcp':
                    print(port['device_owner'], port['id'])
                else:
                    print(port['device_owner'], port['id'])
                    print("->  ", port)
            for subnet in net['subnets']:
                print("    ", subnet)
        """

def main():
    obj = NeutronCleaner()
    obj.clean()

if __name__ == '__main__':
    sys.exit(main())
