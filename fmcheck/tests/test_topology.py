"""
Unit group functionality of topology.
"""

import pytest
from fmcheck.topology import Topology
from fmcheck.host import Host
from fmcheck.link import Link
from fmcheck.switch import Switch
import json
import logging
import requests
import requests_mock
#
import os
import json


def read_json(filename):
    mock_response_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(mock_response_file, 'r') as f:
        return json.load(f)

def return_props():
    return {'controller': [{'ip': '127.0.0.2', 'name': 'c2'}], 'link': [{'source_port': 1, 'source': 'noviflow100', 'destination_port': 1, 'destination': 'noviflow200'}, {'source_port': 1, 'source': 'noviflow200', 'destination_port': 1, 'destination': 'noviflow100'}], 'switch': [{'name': 's11', 'dpid': '64', 'ip': '172.24.86.98', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}, {'name': 's11', 'dpid': 'C8', 'ip': '172.24.86.99', 'password': 'noviflow', 'type': 'ovs', 'protocols': 'OpenFlow13', 'user': 'superuser'}], 'host': [{'ip': '127.0.0.2', 'name': 'h1'}]}


def get_link_info():
    return read_json('./mock_responses/config_oflows.json')


def get_link_info_sr():
    return read_json('./mock_responses/config_oflows_sr.json')



def get_shard_response():
    return read_json('./mock_responses/shard.json')
 
@requests_mock.Mocker()
def test_validate_nodes(m):
    props = return_props();
    if props.get('link'):
        for properties in props['link']:
            new_host = Topology(properties);

    
    m.register_uri('GET', 'http://127.0.0.1:8181/jolokia/read/org.opendaylight.controller:Category=ShardManager,name=shard-manager-operational,type=DistributedOperationalDatastore', json=get_shard_response(), status_code=200)
    m.register_uri('GET', 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/flow:1', status_code=200, json=get_link_info())
    m.register_uri('GET', 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/flow:1:sr', status_code=200, json=get_link_info_sr())
    output = new_host.validate_links();
    assert output is False

@requests_mock.Mocker()
def test_validate_cluster(m):
    props = return_props();
    if props.get('controller'):
        for properties in props['controller']:
            new_host = Topology(properties);
                
    m.register_uri('GET', 'http://127.0.0.1:8181/jolokia/read/org.opendaylight.controller:Category=ShardManager,name=shard-manager-operational,type=DistributedOperationalDatastore', json=get_shard_response(), status_code=200)
    output = new_host.validate_cluster();
    assert output is True


"""def test_load_links():
    props = return_props();
    if props.get('link'):
        for properties in props['link']:
            new_host = Topology(properties);


    output = new_host.load_links();
    print output;

def test_get_master_controller_name():
    props = return_props();
    if props.get('switch'):
        for properties in props['switch']:
            switch  = Switch(properties);
            print switch.name
        
    if props.get('controller'):
        for properties in props['controller']:
            new_host  = Topology(properties);
            new_host.switches_by_openflow_name[switch.openflow_name] = switch
            new_host.switches[switch.name] = switch
            new_host.switches_by_dpid[switch.dpid] = switch

    output = new_host.get_master_controller_name('openflow:100');
    print output;

test_get_master_controller_name();"""
