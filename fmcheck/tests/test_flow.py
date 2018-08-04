"""
Unit test flows functionality of fmcheck.
"""

import pytest
from fmcheck.flow import Flow
from fmcheck.flow import get_id as flow_get_id
from fmcheck.flow import get_version as flow_get_version
import requests
import requests_mock
#from unittest import mock
#from mock import patch
import logging
import re
import json
import os



def read_json(filename):
    mock_response_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(mock_response_file, 'r') as f:
        return json.load(f)


def get_raw_fm_data():
    return read_json('./mock_responses/config_fm_data.json') 


def get_raw_config_data():
    return  read_json('./mock_responses/config_of_conf.json')


def get_raw_operational_data():
    return read_json('./mock_responses/config_of_op.json')



def get_ovs_like_flows():
    output = """OFPST_FLOW reply (OF1.3) (xid=0x2):
 cookie=0x2b00000000000006, duration=81893.393s, table=0, n_packets=16380, n_bytes=1425060, priority=100,dl_type=0x88cc actions=CONTROLLER:65535
 cookie=0x1f0000010000000a, duration=81893.393s, table=0, n_packets=0, n_bytes=0, priority=99,dl_type=0x88cc actions=CONTROLLER:65535
 cookie=0x1f00000300000190, duration=81816.569s, table=0, n_packets=0, n_bytes=0, priority=1040,mpls actions=goto_table:1
 cookie=0x1f00000400000064, duration=81815.059s, table=0, n_packets=0, n_bytes=0, priority=1000,mpls actions=goto_table:1
 cookie=0x2b0000000000000e, duration=81889.395s, table=0, n_packets=104, n_bytes=8224, priority=2,in_port=2 actions=output:1
 cookie=0x2b0000000000000f, duration=81889.395s, table=0, n_packets=58, n_bytes=4540, priority=2,in_port=1 actions=output:2,CONTROLLER:65535
 cookie=0x1f00000600000190, duration=81816.562s, table=1, n_packets=0, n_bytes=0, priority=30311,mpls,in_port=2,mpls_label=18012 actions=group:2000000001
 cookie=0x1f00000500000190, duration=81816.061s, table=1, n_packets=0, n_bytes=0, priority=30310,mpls,mpls_label=18012 actions=group:2000000000
 cookie=0x1f00000200000190, duration=81815.560s, table=1, n_packets=0, n_bytes=0, priority=30310,mpls,mpls_label=15002 actions=pop_mpls:0x8847,output:2"""
    
    if not output:
        return None

    regex = re.compile(r'(cookie=.*)', re.IGNORECASE)
    regexvalues = re.compile(
        r'cookie=(0[xX][0-9a-fA-F]+),.*table=(\d+),.*n_packets=(\d+),.*n_bytes=(\d+)', re.IGNORECASE)

    flows = []
    flowid = None
    for linematch in regex.finditer(output):
        line = linematch.group(1)
        for match in regexvalues.finditer(line):
            flow = {'id': flowid, 'cookie': int(match.group(1), 16), 'table': match.group(2),
                    'packets': match.group(3), 'bytes': match.group(4)}
            flows.append(flow)
    logging.debug(flows)
    return flows


def create_flow(table=None, name=None, cookie=None):
    cookie = str(cookie) if cookie is not None else None
   
    current_flow = Flow(node='S11', node_of_name='openflow:11', cookie=cookie, table=table, name=name)    
    
    return current_flow

def test_flow_init():    
    flows = get_ovs_like_flows() 
    flow_count=0
    if flows:
        for flow in flows:
            new_flow = create_flow(cookie=flow['cookie'])
            if new_flow:
                flow_count = flow_count + 1
            attrs = vars(new_flow)        
            print ', '.join("%s: %s" % item for item in attrs.items())
        print flow_count, len(flows)
        #assert 0
        assert len(flows) == flow_count


def test_of_config():
    nodes = get_raw_config_data()
    #nodes = json.loads(get_raw_config_data())
    for node in nodes['nodes']['node']:
        name = node['id']

    tables = node.get('table') if 'table' in node else node.get(
            'flow-node-inventory:table')
    if tables:
        for table in tables:
            table_id = table['id']
            flows = table.get('flow') if 'flow' in table else table.get(
                'flow-node-inventory:flow')
            if flows:
                for flow in flows:
                    new_flow = create_flow(table=table_id, name=flow['id'], cookie=flow.get('cookie'))
                    new_flow.add_of_config(flow)
                    print new_flow.of_config_id, new_flow.of_config_version, new_flow.of_config
                    assert new_flow.of_config_id == flow_get_id(flow['cookie']) and new_flow.of_config_version == flow_get_version(flow['cookie'])  



def test_of_operational():
    nodes = get_raw_operational_data()
    #nodes = json.loads(get_raw_operational_data())
    if nodes is not None and 'nodes' in nodes and 'node' in nodes['nodes']:
        for node in nodes['nodes']['node']:
            tables = node.get('table') if 'table' in node else node.get(
                'flow-node-inventory:table')
            if tables:
                for table in tables:
                    table_id = table['id']
                    flows = table.get('flow') if 'flow' in table else table.get(
                        'flow-node-inventory:flow')
                    if flows:
                        for flow in flows:
                            new_flow = create_flow(table=table_id, name=flow['id'], cookie=flow.get('cookie'))
                            new_flow.add_of_operational(flow)
                            print new_flow.of_operational_id, new_flow.of_operational_version, new_flow.of_operational
                            assert new_flow.of_operational_id == flow_get_id(flow['cookie']) and new_flow.of_operational_version == flow_get_version(flow['cookie'])


def test_add_switch():
    flows = get_ovs_like_flows() 
    if flows:
        for flow in flows:
            new_flow = create_flow(cookie=flow['cookie'])
            if new_flow:
                new_flow.add_switch(flow)
            attrs = vars(new_flow)        
            print ', '.join("%s: %s" % item for item in attrs.items())
            #assert 0
            assert new_flow.switch_id == flow_get_id(flow['cookie']) and new_flow.switch_version == flow_get_version(flow['cookie'])

"""
def test_add_fm():
    nodes = get_raw_fm_data()
    #nodes = json.loads(get_raw_fm_data())
    if nodes is not None and 'nodes' in nodes and 'node' in nodes['nodes']:
        for node in nodes['nodes']['node']:
            tables = node.get('table') if 'table' in node else node.get(
                        'flow-node-inventory:table')
            if tables:
                for table in tables:
                    table_id = table['id']
                    flows = table.get('flow') if 'flow' in table else table.get(
                        'flow-node-inventory:flow')
                    if flows:
                        for flow in flows:
                            new_flow = create_flow(table=table_id, name=flow['id'], cookie=flow.get('cookie'))
                            new_flow.add_fm(flow)
                            assert flow in new_flow.fm 
"""

def test_calculated():
    flows = get_ovs_like_flows() 
    if flows:
        for flow in flows:
            new_flow = create_flow(cookie=flow['cookie'])
            if new_flow:
                new_flow.mark_as_calculated()
            assert new_flow.calculated == True 


def test_msgs_config():
    nodes = get_raw_config_data()
    #nodes = json.loads(get_raw_config_data())
    for node in nodes['nodes']['node']:
        name = node['id']

    tables = node.get('table') if 'table' in node else node.get(
            'flow-node-inventory:table')
    if tables:
        for table in tables:
            table_id = table['id']
            flows = table.get('flow') if 'flow' in table else table.get(
                'flow-node-inventory:flow')
            if flows:
                for flow in flows:
                    new_flow = create_flow(table=table_id, name=flow['id'], cookie=flow.get('cookie'))
                    new_flow.add_of_config(flow)
                    msg = "{}({})".format(new_flow.node, new_flow.node_of_name)
                    tflow = new_flow.of_config[0]
                    msg = msg + ", " + "config table/{}/name/{}/id/{}/version/{}".format(
                            tflow['table_id'], tflow['id'], flow_get_id(tflow['cookie']), flow_get_version(tflow['cookie']))
                    tmsg = new_flow._get_info_msg()
                    assert msg == tmsg



                        

#def test_msgs_operational():
    #TBD

#def test_msgs_fm():
    #TBD

