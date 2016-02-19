#!/usr/bin/env python
# Max Huang 

"""
vSphere Python SDK program for listing Datastores in Datastore Cluster
python ./query_datastore.py -s lglag075.corp.com -u 'CORP\nxxx' -p 'xxx'
"""
import argparse
import atexit

from pyVmomi import vim
from pyVmomi import vmodl
from pyVim import connect
import ssl


def get_args():
    """
   Supports the command-line arguments listed below.
   """
    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')

    parser.add_argument('-s', '--host',
                        required=True, action='store',
                        help='Remote host to connect to')

    parser.add_argument('-o', '--port',
                        type=int, default=443,
                        action='store', help='Port to connect on')

    parser.add_argument('-u', '--user', required=True,
                        action='store',
                        help='User name to use when connecting to host')

    parser.add_argument('-p', '--password',
                        required=True, action='store',
                        help='Password to use when connecting to host')

    args = parser.parse_args()
    return args


def main():
    """
   Simple command-line program for listing Datastores in Datastore Cluster
   https://github.com/vmware/pyvmomi/issues/24

   """

    args = get_args()

    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=args.host,
                                                user=args.user,
                                                pwd=args.password,
                                                port=int(args.port),
                                                sslContext=context)
        if not service_instance:
            print("Could not connect to the specified host using "
                  "specified username and password")
            return -1
        atexit.register(connect.Disconnect, service_instance)
        # Retrieve content.
        dc = service_instance.content.rootFolder.childEntity[0]
        print('datacenter name is: {0}'.format(dc.name))
        ds_clusters = dc.datastoreFolder.childEntity[0].childEntity[0]
        for ds_cluster in ds_clusters.childEntity:
            for datastore in ds_cluster.childEntity:
                su = datastore.summary
                usage = (su.capacity - su.freeSpace) / float(su.capacity)
                print('Datastore "{0}" usage: {1:.2f}%'.format(
                    datastore.name, usage * 100))
    except vmodl.MethodFault as error:
        print "Caught vmodl fault : " + error.msg
        return -1
    return 0

# Start program
if __name__ == "__main__":
    main()
