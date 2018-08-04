"""
Unit test controller functionality of fmcheck.
"""

import pytest
from fmcheck.controller import Controller
import requests
import requests_mock
#from unittest import mock
#from mock import patch
import logging
import os
import json



def read_json(filename):
    mock_response_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(mock_response_file, 'r') as f:
        return json.load(f)


def get_multi_props():
    return {'controller': [{'ip': '172.24.86.209', 'name': 'c0'}, {'ip': '127.0.0.1', 'name': 'c1'}], 'link': [{'source_port': 1, 'source': 'noviflow100', 'destination_port': 1, 'destination': 'noviflow200'}, {'source_port': 1, 'source': 'noviflow200', 'destination_port': 1, 'destination': 'noviflow100'}], 'switch': [{'name': 'noviflow100', 'dpid': '64', 'ip': '172.24.86.98', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}, {'name': 'noviflow200', 'dpid': 'C8', 'ip': '172.24.86.99', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}]} 


def get_single_props():
    return {'controller': [{'ip': '127.0.0.2', 'name': 'c2'}], 'link': [{'source_port': 1, 'source': 'noviflow100', 'destination_port': 1, 'destination': 'noviflow200'}, {'source_port': 1, 'source': 'noviflow200', 'destination_port': 1, 'destination': 'noviflow100'}], 'switch': [{'name': 'noviflow100', 'dpid': '64', 'ip': '172.24.86.98', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}, {'name': 'noviflow200', 'dpid': 'C8', 'ip': '172.24.86.99', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}]} 


def get_flow_dump():
    return read_json('./mock_responses/config_flows.json')


def get_shard_response():
    return read_json('./mock_responses/shard.json')


@requests_mock.Mocker()
def test_is_sync_true(m):
    m.register_uri('GET', 'http://172.24.86.209:8181/jolokia/read/org.opendaylight.controller:Category=ShardManager,name=shard-manager-operational,type=DistributedOperationalDatastore', json=get_shard_response(), status_code=200)
    m.register_uri('GET', 'http://127.0.0.1:8181/jolokia/read/org.opendaylight.controller:Category=ShardManager,name=shard-manager-operational,type=DistributedOperationalDatastore', json=get_shard_response(), status_code=200)
    props = get_multi_props()
    if props.get('controller'):
        for properties in props['controller']:
            new_controller = Controller(
                properties, props.get('controller_vip'))
            isSync = new_controller.is_sync()
            logging.debug("using is sync %v", isSync)
            assert isSync == True


@requests_mock.Mocker()
def test_is_sync_false(m):
    m.register_uri('GET', 'http://127.0.0.2:8181/jolokia/read/org.opendaylight.controller:Category=ShardManager,name=shard-manager-operational,type=DistributedOperationalDatastore', text='NotOkay', status_code=400)
    props = get_single_props()
    if props.get('controller'):
        for properties in props['controller']:
            new_controller = Controller(
                properties, props.get('controller_vip'))        
            isSync = new_controller.is_sync()
            logging.debug("using is sync %v", isSync)
            assert isSync == False


@requests_mock.Mocker()
def test_fm_prefix_lumina(m):
    m.register_uri('GET', 'http://172.24.86.209:8181/restconf/config/lumina-flowmanager-path:paths', text='Okay')
    m.register_uri('GET', 'http://127.0.0.1:8181/restconf/config/lumina-flowmanager-path:paths', text='Okay')
    props = get_multi_props()
    if props.get('controller'):
        for properties in props['controller']:
            new_controller = Controller(
                properties, props.get('controller_vip'))        
            prefix = new_controller.get_fm_prefix()
            logging.debug("using prefix %s", prefix)
            assert prefix == 'lumina-flowmanager-' 


@requests_mock.Mocker()
def test_fm_prefix_brocade(m):
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/config/lumina-flowmanager-path:paths', text='NotOkay', status_code=400)
    props = get_single_props()
    if props.get('controller'):
        for properties in props['controller']:
            new_controller = Controller(
                properties, props.get('controller_vip'))        
            prefix = new_controller.get_fm_prefix()
            logging.debug("using prefix %s", prefix)
            assert prefix == 'brocade-bsc-'


def test_base_url():
    props = get_single_props()
    if props.get('controller'):
        for properties in props['controller']:
            new_controller = Controller(
                properties, props.get('controller_vip'))        
            baseurl = new_controller.get_base_url()
            logging.debug("using base-url %s", baseurl)
            assert baseurl == 'http://127.0.0.2:8181'


@requests_mock.Mocker()
def test_flow_stats_full(m):
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/operational/opendaylight-inventory:nodes', status_code=200, json=get_flow_dump())
    props = get_single_props()
    bcnt = 'byte-count'
    pcnt = 'packet-count'
    if props.get('controller'):
       for properties in props['controller']:
           new_controller = Controller(
                properties, props.get('controller_vip'))
           fullstat = new_controller.get_flow_stats()
           logging.error("using full-stat %s", fullstat) 
           assert fullstat is None

"""
@requests_mock.Mocker()
def test_flow_stats_invalid(m):
    m.register_uri('GET', 'http://127.0.0.2:8181/restconf/operational/opendaylight-inventory:nodes', status_code=200, text=get_flow_dump())
    props = get_single_props()
    bcnt = 'byte-count'
    pcnt = 'packet-count'
    if props.get('controller'):
       for properties in props['controller']:
           new_controller = Controller(
                properties, props.get('controller_vip'))
           fullstat = new_controller.get_flow_stats()
           logging.error("using full-stat %s", fullstat) 
           assert fullstat is None
"""

