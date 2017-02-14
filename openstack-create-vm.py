import re
import sys
import time
import os_client_config
#from cinderclient.client import client as cinderclient
from novaclient import client as novaclient


def get_cloud_config(cloud='devstack-admin'):
    return os_client_config.OpenStackConfig().get_one_cloud(cloud=cloud)


def credentials(cloud='devstack-admin'):
    """Retrieves credentials to run functional tests"""
    return get_cloud_config(cloud=cloud).get_auth_args()


def create_vm():
    creds = credentials()
    print(creds)
    auth_url = creds['auth_url'] + "/v2.0"
    nova = novaclient.Client('2', creds['username'], creds['password'], 'demo', auth_url)
    print(nova.servers.list())
    print(nova.flavors.list())
    print(nova.images.list())
    print(nova.keypairs.list())
    image = nova.images.find(name="cirros-0.3.4-x86_64-uec")
    print(image)
    # get the flavor
    flavor = nova.flavors.find(name="m1.tiny")
    print(flavor)
    network = nova.networks.find(label='private')
    print(network)
    nics = [{'net-id': network.id}]
    print(nics)
    server = nova.servers.create(name = 'test', image = image.id, flavor = flavor.id, nics = nics)
    print(server)

if __name__ == '__main__':
    create_vm()
    sys.exit()
