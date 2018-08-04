"""
Unit test openflow functionality of fmcheck.
"""

import pytest
from fmcheck import openflow
from fmcheck.controller import Controller
import requests
import requests_mock
#from unittest import mock
#from mock import patch
import logging
#from fmcheck.test_flow import get_raw_fm_data as get_test_of_fm
import os
import json


def read_json(filename):
    mock_response_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(mock_response_file, 'r') as f:
        return json.load(f)


def get_single_props():
    return {'controller': [{'ip': '127.0.0.2', 'name': 'c2'}], 'link': [{'source_port': 1, 'source': 'noviflow100', 'destination_port': 1, 'destination': 'noviflow200'}, {'source_port': 1, 'source': 'noviflow200', 'destination_port': 1, 'destination': 'noviflow100'}], 'switch': [{'name': 'noviflow100', 'dpid': '64', 'ip': '172.24.86.98', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}, {'name': 'noviflow200', 'dpid': 'C8', 'ip': '172.24.86.99', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}]}



def get_test_path():
    return """{"paths":{"path":[{"name":"derect-test-path","lumina-flowmanager-path-nodetonode:match":{},"lumina-flowmanager-path-nodetonode:egress":{},"provider":"nodetonode","constraints":{},"endpoint2":{"node":"openflow:11"},"endpoint1":{"node":"openflow:12"}}]}}"""


def get_test_of_fm():
    return read_json('./mock_responses/config_of_fm.json')

def get_test_of_config():
    return read_json('./mock_responses/config_of_conf.json')

def get_test_of_opera():
    return read_json('./mock_responses/config_of_op.json')

def get_test_topo():
    return read_json('mock_responses/config_oflows_sr.json')

def get_raw_operational_data():
    return read_json('mock_responses/config_flows.json')


@requests_mock.Mocker()
def test_get_api(m):
    props = get_single_props()
    new_controller = Controller(props.get('controller')[0], props.get('controller')[0].get('controller_vip'))
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/config/opendaylight-inventory:nodes', status_code=200, json=get_raw_operational_data())
    data = openflow.get_from_api(new_controller, 'http://127.0.0.2:8181/restconf/config/opendaylight-inventory:nodes') 
    assert data


@requests_mock.Mocker()
def test_get_topology(m):
    props = get_single_props()
    new_controller = Controller(props.get('controller')[0], props.get('controller')[0].get('controller_vip'))
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/operational/network-topology:network-topology/topology/flow:1:sr', status_code=200, json=get_test_topo())
    data = openflow.get_topology(new_controller, "flow:1:sr")
    print data
    assert data is not None


@requests_mock.Mocker()
def test_get_config_openflow(m):
    props = get_single_props()
    new_controller = Controller(props.get('controller')[0], props.get('controller')[0].get('controller_vip'))
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/config/opendaylight-inventory:nodes', status_code=200, json=get_test_of_config())
    data = openflow.get_config_openflow(new_controller)
    print data 
    assert 'nodes' in data  and 'node' in data['nodes']

@requests_mock.Mocker()
def test_get_opera_openflow(m):
    props = get_single_props()
    new_controller = Controller(props.get('controller')[0], props.get('controller')[0].get('controller_vip'))
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/operational/opendaylight-inventory:nodes', status_code=200, json=get_test_of_opera())
    data = openflow.get_operational_openflow(new_controller)
    print data 
    assert 'nodes' in data  and 'node' in data['nodes']

"""
#E       NoMockAddress: No mock address: GET http://127.0.0.2:8181/restconf/config/lumina-flowmanager-path:paths
@requests_mock.Mocker()
def test_get_fm_openflow(m):
    props = get_single_props()
    new_controller = Controller(props.get('controller')[0], props.get('controller')[0].get('controller_vip'))
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/operational/lumina-flowmanager-openflow:nodes', status_code=200, json=get_test_of_fm())
    data = openflow.get_fm_openflow(new_controller)
    print data 
    assert 'nodes' in data  and 'node' in data['nodes']
"""


@requests_mock.Mocker()
def test_get_nodes(m):
    props = get_single_props()
    new_controller = Controller(props.get('controller')[0], props.get('controller')[0].get('controller_vip'))
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/operational/network-topology:network-topology/topology/flow:1:sr', status_code=200, json=get_test_topo())
    data = openflow.get_topology_nodes(new_controller, "flow:1:sr")
    print data
    assert data is not None


@requests_mock.Mocker()
def test_get_links(m):
    props = get_single_props()
    new_controller = Controller(props.get('controller')[0], props.get('controller')[0].get('controller_vip'))
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/operational/network-topology:network-topology/topology/flow:1:sr', status_code=200, json=get_test_topo())
    data = openflow.get_topology_links(new_controller, "flow:1:sr")
    print data
    assert data is not None


@requests_mock.Mocker()
def test_get_connected_nodes(m):
    props = get_single_props()
    new_controller = Controller(props.get('controller')[0], props.get('controller')[0].get('controller_vip'))
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/operational/opendaylight-inventory:nodes', status_code=200, json=get_test_of_opera())
    data = openflow.get_openflow_connected_nodes(new_controller)
    print data
    assert data is not None


@requests_mock.Mocker()
def test_get_paths(m):
    props = get_single_props()
    new_controller = Controller(props.get('controller')[0], props.get('controller')[0].get('controller_vip'))
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/config/lumina-flowmanager-path:paths', status_code=200, json=get_test_of_opera())
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/operational/lumina-flowmanager-path:paths', status_code=200, text=get_test_path())
    data = openflow.get_paths(new_controller)
    print data
    assert data is not None


